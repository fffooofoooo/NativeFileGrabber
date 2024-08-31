import io
import os
import zipfile
import json
import requests

if not os.path.isdir(".sos"):
    os.mkdir(".sos")
for bye in os.listdir(".sos"):
    os.remove(f'.sos/{bye}')

def pullDep(mUrl, groupId, artifactId, ver):
    r = requests.get(f"{mUrl}{groupId.replace('.', '/')}/{artifactId}/{ver}/{artifactId}-{ver}-linuxathena.zip", stream=True)
    with zipfile.ZipFile(io.BytesIO(r.content)) as zip_ref:
        for possi in zip_ref.namelist():
            if (".so" in possi) and (".so.debug" not in possi):
                with open(f'.sos/{os.path.split(possi)[1]}', "wb") as file:
                    file.write(zip_ref.read(possi))

for files in os.listdir("vendorJson"):
    with open(f'vendorJson/{files}', mode="r", encoding="utf-8") as read_file:
        curLib = json.load(read_file)
    if curLib['mavenUrls']:
        mavenUrl = curLib['mavenUrls'][0] if curLib['mavenUrls'][0][-1] == '/' else curLib['mavenUrls'][0] + '/'
        for deps in curLib["jniDependencies"]:
            if (deps['isJar'] == False) and ("linuxathena" in deps["validPlatforms"]):
                pullDep(mavenUrl, deps['groupId'], deps['artifactId'], deps['version'])

artifactlist = ["apriltag", "cscore", "ntcore", "hal", "wpimath", "wpinet", "wpiutil"]
wpiVersion = "2024.3.2"
opencvVersion = "4.8.0-4"
wpiUrl = "https://frcmaven.wpi.edu/artifactory/release/"

for deps in artifactlist:
    pullDep(wpiUrl, f'edu.wpi.first.{deps}', f'{deps}-cpp', wpiVersion)

pullDep(wpiUrl, 'edu.wpi.first.thirdparty.frc2024.opencv', 'opencv-cpp', opencvVersion)