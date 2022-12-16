# ParseRbxcdnJavascript.py
# pos0#0998
# 12/13/2022
# Parses JavaScript and CSS packs from ROBLOX cdn servers

import os
import requests

# JavaScript

exampleJavaScriptPack = """;// bundle: page___test_m
;// files: Test/Test.js, ~/Test/Test.js

;// Test/Test.js
console.log("From Test/Test.js!");

;// ~/Test/Test.js
console.log("From ~/Test/Test.js");""" # TODO: make this have an actual use

def parseJavaScriptBundleName(pack: str = exampleJavaScriptPack):
    bundleName = ""

    for packLine in pack.splitlines():
        if ";// bundle: " in packLine:
            bundleName = packLine[12:]

    return bundleName

def parseFilesInJavaScriptPack(pack: str = exampleJavaScriptPack):
    filesInPack = []

    for packLine in pack.splitlines():
        if ";// files: " in packLine:
            filesInPack = packLine[11:].split(', ')

    return filesInPack

def findJavaScriptFileInPack(pack: str = exampleJavaScriptPack, file: str = "Test/Test.js"):
    javaScriptFile = ""
    lines = pack.splitlines()
    iterator = iter(lines)

    for packLine in lines:
        next(iterator, None)
        if packLine.startswith(";// " + file):
            javaScriptFile = next(iterator, None).strip()

    return javaScriptFile

# CSS

exampleCSSBundleURL = "http://www.roblox.com/CSS/Base/CSS/FetchCSS?path=main___23e1cfc4f7f34bdc2ff4f3c2d637a122_m.css"
exampleCSSBundle = """/* ~/CSS/Test.css */
.testClass\{float\:left\}""" # TODO: make this have an actual use

def parseCSSBundleName(url: str = exampleCSSBundleURL):
    return url.split("?path=")[1]

def parseFilesInCSSBundle(bundle: str = exampleCSSBundle):
    filesInBundle = []

    for bundleLine in bundle.splitlines():
        if bundleLine.startswith("/* ") and bundleLine.endswith(".css */"):
            # i hate this So much
            filesInBundle.append(bundleLine[3:].split(" */")[0])

    return filesInBundle

def findCSSFileInBundle(bundle: str = exampleCSSBundle, file: str = "~/CSS/Test.css"):
    lines = bundle.splitlines()
    iterator = iter(lines)

    for bundleLine in lines:
        next(iterator, None)
        if bundleLine == "/* " + file + " */":
            return next(iterator, None).strip()

# Runner

if __name__ == "__main__":
    outputPath = input("Output path (ex: C:/parser/located/here/outputPath): ")
    bundleType = int(input("CSS (0) or JavaScript (1)?: "))

    if bundleType == 0: # CSS
        cssBundleURL = input("Paste the URL to the CSS bundle here (ex: http://www.roblox.com/CSS/Base/CSS/FetchCSS?path=page___bundle_m.css): ")
        cssBundle = requests.get(cssBundleURL).text

        if os.path.exists(outputPath):
            bundleName = parseCSSBundleName(cssBundleURL)

            if bundleName != "":
                filesInBundle = parseFilesInCSSBundle(cssBundle)

                if len(filesInBundle) != 0:
                    filesAsString = ", ".join(filesInBundle)

                    print("Parsing bundle " + bundleName + " with files " + filesAsString + "...")

                    for file in filesInBundle:
                        cssFile = findCSSFileInBundle(cssBundle, file)

                        if cssFile != "":
                            os.makedirs(os.path.dirname(outputPath + file[1:]), exist_ok=True)

                            with open(outputPath + file[1:], 'x') as outputFile:
                                outputFile.write(cssFile)
        else:
            print("Invalid output path")
    elif bundleType == 1: # JavaScript
        javaScriptPack = requests.get(input("Paste the URL to the JavaScript pack here (ex: http://js.rbxcdn.com/pack.js): ")).text

        if os.path.exists(outputPath):
            bundleName = parseJavaScriptBundleName(javaScriptPack)

            if bundleName != "":
                filesInPack = parseFilesInJavaScriptPack(javaScriptPack)
                
                if len(filesInPack) != 0:
                    filesAsString = ", ".join(filesInPack)

                    print("Parsing pack " + bundleName + " with files " + filesAsString + "...")

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