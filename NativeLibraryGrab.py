import os
import zipfile
import json
import requests
import urllib.request as request

for bye in os.listdir(".sos"):
    os.remove(f'.sos/{bye}')

for files in os.listdir("json"):
    with open(f'json/{files}', mode="r", encoding="utf-8") as read_file:
        curLib = json.load(read_file)
    if curLib['mavenUrls']:
        mavenUrl = curLib['mavenUrls'][0] if curLib['mavenUrls'][0][-1] == '/' else curLib['mavenUrls'][0] + '/'
        for deps in curLib["jniDependencies"]:
            if (deps['isJar'] == False) and ("linuxathena" in deps["validPlatforms"]):
                loc = f".sos/{deps['artifactId']}-{deps['version']}-linuxathena.zip"
                r = requests.get(f"{mavenUrl}{deps['groupId'].replace('.', '/')}/{deps['artifactId']}/{deps['version']}/{deps['artifactId']}-{deps['version']}-linuxathena.zip", stream=True)
                with open (loc, "wb") as f:
                    f.write(r.content)
                with zipfile.ZipFile(loc) as zip_ref:
                    for possi in zip_ref.namelist():
                        if (".so" in possi) and (".so.debug" not in possi):
                            with open(f'.sos/{os.path.split(possi)[1]}', "wb") as file:
                                file.write(zip_ref.read(possi))
                os.remove(loc)
        for deps in curLib["cppDependencies"]:
            if ("linuxathena" in deps["binaryPlatforms"]):
                loc = f".sos/{deps['artifactId']}-{deps['version']}-linuxathena.zip"
                with requests.get(f"{mavenUrl}{deps['groupId'].replace('.', '/')}/{deps['artifactId']}/{deps['version']}/{deps['artifactId']}-{deps['version']}-linuxathena.zip") as r:
                    with open (loc, "wb") as f:
                        f.write(r.content)
                with zipfile.ZipFile(loc) as zip_ref:
                    for possi in zip_ref.namelist():
                        if (".so" in possi) and (".so.debug" not in possi):
                            with open(f'.sos/{os.path.split(possi)[1]}', "wb") as file:
                                file.write(zip_ref.read(possi))
                os.remove(loc)