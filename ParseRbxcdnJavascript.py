# ParseRbxcdnJavascript.py
# pos0#0998
# 12/13/2022
# Parses JavaScript packs from ROBLOX cdn servers

# https://web.archive.org/web/20150907171853id_/http://js.rbxcdn.com/22700e0941ec9dad21d89a040ff5ed77.js

import requests

examplePack = """;// bundle: page___test_m
;// files: Test/Test.js, ~/Test/Test.js

;// Test/Test.js
console.log("From Test/Test.js!");

;// ~/Test/Test.js
console.log("From ~/Test/Test.js");"""

def parseBundleName(pack: str = examplePack):
    bundleName = ""

    for packLine in pack.splitlines():
        if ";// bundle: " in packLine:
            bundleName = packLine[12:]

    return bundleName

def parseFilesInPack(pack: str = examplePack):
    filesInPack = []

    for packLine in pack.splitlines():
        if ";// files: " in packLine:
            filesInPack = packLine[11:].split(', ')

    return filesInPack

def findJavaScriptFileInPack(pack: str = examplePack, file: str = "Test/Test.js"):
    javaScriptFile = ""
    lines = pack.splitlines()
    iterator = iter(lines)

    for packLine in lines:
        next(iterator)
        if packLine.startswith(";// " + file):
            javaScriptFile = next(iterator).strip()

    return javaScriptFile

if __name__ == "__main__":
    javaScriptPack = requests.get(input("Paste the URL to the JavaScript pack here (ex: http://js.rbxcdn.com/pack.js): ")).text
    outputPath = input("Output path: ")

    bundleName = parseBundleName(javaScriptPack)

    filesInPack = parseFilesInPack(javaScriptPack)
    filesAsString = ", ".join(filesInPack)

    print("Parsing bundle " + bundleName + " with files " + filesAsString + "...")

    for file in filesInPack:
        findJavaScriptFileInPack(javaScriptPack, file)
else:
    exit()