# ParseRbxcdnJavascript.py
# pos0#0998
# 12/13/2022
# Parses JavaScript packs from ROBLOX cdn servers

import os
import requests

examplePack = """;// bundle: page___test_m
;// files: Test/Test.js, ~/Test/Test.js

;// Test/Test.js
console.log("From Test/Test.js!");

;// ~/Test/Test.js
console.log("From ~/Test/Test.js");""" # TODO: make this have an actual use

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
        next(iterator, None)
        if packLine.startswith(";// " + file):
            javaScriptFile = next(iterator, None).strip()

    return javaScriptFile

if __name__ == "__main__":
    javaScriptPack = requests.get(input("Paste the URL to the JavaScript pack here (ex: http://js.rbxcdn.com/pack.js): ")).text
    outputPath = input("Output path (ex: C:/parser/located/here/outputPath): ")

    if os.path.exists(outputPath):
        bundleName = parseBundleName(javaScriptPack)

        if bundleName != "":
            filesInPack = parseFilesInPack(javaScriptPack)
            
            if len(filesInPack) != 0:
                filesAsString = ", ".join(filesInPack)

                print("Parsing bundle " + bundleName + " with files " + filesAsString + "...")

                for file in filesInPack:
                    javaScriptFile = findJavaScriptFileInPack(javaScriptPack, file)

                    if javaScriptFile != "":
                        if file[:1] != "~":
                            os.makedirs(os.path.dirname(outputPath + "/js/" + file), exist_ok=True)

                            with open(outputPath + "/js/" + file, 'x') as outputFile:
                                outputFile.write(javaScriptFile)
                        else:
                            os.makedirs(os.path.dirname(outputPath + file[1:]), exist_ok=True)

                            with open(outputPath + file[1:], 'x') as outputFile:
                                outputFile.write(javaScriptFile)
                    else:
                        print("Couldn't find file " + file)

                print("Done!")
            else:
                print("Invalid bundle")
        else:
            print("Invalid bundle")
    else:
        print("Invalid output path")
else:
    exit()