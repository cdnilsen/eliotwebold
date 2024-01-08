import os
from sortingdata import allOTBookListPsalmsNormal
import unicodedata
import re
import json

from bs4 import BeautifulSoup as bs
tanakhFolder = "./hebrewXML/"

def getTanakh():
    tanakh = []
    for filename in os.listdir(tanakhFolder):
        if filename.endswith(".xml"):
            tanakh.append(filename)
    return tanakh

allChapters = 0
def compareChapters(tanakhFile):
    mismatchedChapterList = []
    numVersesHebrew = []
    numVersesKJV = []
    global allChapters

    if tanakhFile == "Psalms (metrical)":
        return
    
    if tanakhFile == "Psalms (prose)":
        hebrewText = open(tanakhFolder + "Psalms.xml", "r", encoding="utf-8")
    else:
        hebrewText = open(tanakhFolder + tanakhFile + ".xml", "r", encoding="utf-8")
    hebrewLines = hebrewText.readlines()
    hebrewText.close()

    if tanakhFile == "Psalms":
        kjvText = open('./texts/Psalms (prose).KJV.txt', "r", encoding="utf-8")

    else:
        kjvText = open('./texts/' + tanakhFile + '.KJV.txt', "r", encoding="utf-8")

    kjvLines = kjvText.readlines()
    kjvText.close()

    numChaptersHebrew = []
    HebrewChapterVerseNumDict = {}
    currentHebrewChapter = ""
    verseCountHebrew = 0
    for line in hebrewLines:
        line = line.strip()
        if line.startswith("<c n="):
            allChapters += 1
            currentHebrewChapter = line.split('"')[1]
            if currentHebrewChapter != "":
                currentChapter = currentHebrewChapter
                numChaptersHebrew.append(currentHebrewChapter)
        if line.startswith("<v n="):
            verseCountHebrew += 1
            verseNumber = line.split('"')[1]
            HebrewChapterVerseNumDict[currentChapter] = verseNumber
    
    numChaptersKJV = []
    KJVchapterVerseNumDict = {}
    verseCountKJV = 0
    for line in kjvLines:
        line = line.split(" ")
        verseAddress = line[0].split(".")
        chapter = verseAddress[0]
        verseCountKJV += 1
        if chapter == "":
            continue
        if chapter not in numChaptersKJV and chapter != "":
            numChaptersKJV.append(chapter)
        if chapter != "":
            KJVchapterVerseNumDict[chapter] = verseAddress[1]


    if numChaptersHebrew[-1] != numChaptersKJV[-1]:
        mismatchedChapterList.append(tanakhFile)
    
    totalMismatchedChapters = 0
    for chapter in HebrewChapterVerseNumDict:
        if chapter in KJVchapterVerseNumDict:
            if HebrewChapterVerseNumDict[chapter] != KJVchapterVerseNumDict[chapter]:
                mismatchedChapterList.append(chapter)
                numVersesHebrew.append(HebrewChapterVerseNumDict[chapter])
                numVersesKJV.append(KJVchapterVerseNumDict[chapter])
                totalMismatchedChapters += 1
                print("Mismatched chapter: " + tanakhFile + " " + chapter + " (Hebrew: " + HebrewChapterVerseNumDict[chapter] + "/ KJV: " + KJVchapterVerseNumDict[chapter] + ")")

    if verseCountHebrew != verseCountKJV:
        print(tanakhFile + ": " + str(verseCountHebrew) + " in Hebrew, " + str(verseCountKJV) + " in KJV")
        
    return mismatchedChapterList, numVersesHebrew, numVersesKJV, totalMismatchedChapters > 0


allMismatchedChaptersDict = {}
totalMismatchedChapters = 0
'''
for book in allOTBookListPsalmsNormal:
    allMismatchedChaptersDict[book] = compareChapters(book)
    try:
        if allMismatchedChaptersDict[book][3]:
            mismatchedChapterString = ""
            for mismatchedChapter in allMismatchedChaptersDict[book][0]:
                totalMismatchedChapters += 1
                mismatchedChapterString += mismatchedChapter + " (" + allMismatchedChaptersDict[book][1][allMismatchedChaptersDict[book][0].index(mismatchedChapter)] + "/" + allMismatchedChaptersDict[book][2][allMismatchedChaptersDict[book][0].index(mismatchedChapter)] + "), "
    except:
        continue
'''

cantillationMarksCodePoints = [
    "u0591",
    "u0592",
    "u0593",
    "u0594",
    "u0595",
    "u0596",
    "u0597",
    "u0598",
    "u0599",
    "u059a",
    "u059b",
    "u059c",
    "u059d",
    "u059e",
    "u059f",
    "u05a0",
    "u05a1",
    "u05a2",
    "u05a3",
    "u05a4",
    "u05a5",
    "u05a6",
    "u05a7",
    "u05a8",
    "u05a9",
    "u05aa",
    "u05ab",
    "u05ac",
    "u05ad",
    "u05ae",
    "u05af"
]

def killCantillationMarks(word):
    newWord = ""
    for char in word:
        unicodeChar = char.encode("unicode_escape").decode("utf-8")[1:]
        if unicodeChar not in cantillationMarksCodePoints:
            newWord += char
    return newWord

def processOneHebrewWord(line, wordTag):
    line = killCantillationMarks(line).strip().replace("׃", "")

    if wordTag == "k":
        output = '<span class="ketiv" style="color: red; border-bottom: 1px dotted #000;">' + line
    elif wordTag == "q":
        output = '<span class="hover-tooltip">' + line.strip().replace("׃", "") + '</span></span>'
        #output = '<span class="hover-tooltip" title="' + line.strip().replace("׃", "") + '"' + '>'
    elif wordTag == "h":
        output = '<H>' + line + "</H>"
    else:
        output = line

    return (output)


otHapaxFile = open("./OT hapaxes (messy).txt", "r", encoding="utf-8")
currentBook = ""
bookToHapaxDict = {}
for line in otHapaxFile:
    splitLine = line.split("\t")
    if len(splitLine) == 1 and len(splitLine[0]) > 1:
        currentBook = splitLine[0].strip()
    elif len(splitLine) > 1:
        verseAddress = splitLine[0].split(" ")[-1][0:-1]
        book = " ".join(splitLine[0].split(" ")[0:-1])[1:]

        if book not in bookToHapaxDict:
            bookToHapaxDict[book] = {}
            bookToHapaxDict[book]["hapaxes"] = []
            bookToHapaxDict[book]["addresses"] = []

        hapax = killCantillationMarks(splitLine[1]).strip()
        if len(hapax) > 0:
            bookToHapaxDict[book]["hapaxes"].append(unicodedata.normalize('NFC', hapax))
            bookToHapaxDict[book]["addresses"].append(verseAddress)

def processBookXML(bookName):
    originalName = bookName
    if bookName == "Psalms (metrical)":
        return
    if bookName == "Psalms (prose)":
        bookName = "Psalms"
    
    myXML = open("./hebrewXML/" + bookName + ".xml", "r", encoding="utf-8")

    finalJSONDict = {}
    mySoup = bs(myXML, features="xml")
    for tag in mySoup('x'):
        tag.decompose()
    allChapters = mySoup.find_all('c')
    for chapter in allChapters:
        currentChapter = chapter['n']
        for verse in chapter.find_all('v'):
            currentVerseDict = {}
            processedHapaxes = ""
            currentVerse = verse['n']
            for word in verse:
                try:
                    wordTag = word.name
                    if wordTag in ["w", "k", "q"]:
                        if (currentChapter + ":" + currentVerse) in bookToHapaxDict[bookName]["addresses"]:
                            for i in range(len(bookToHapaxDict[bookName]["addresses"])):
                                if bookToHapaxDict[bookName]["addresses"][i] == (currentChapter + ":" + currentVerse):
                                    myText = unicodedata.normalize('NFC', killCantillationMarks(word.text))

                                    #Fixes, e.g., different ordering of a dagesh and niqqud
                                    myHapax = bookToHapaxDict[bookName]["hapaxes"][i]

                                    # This has already undergone normalization
                                    if myHapax in myText:
                                            wordTag = "h"
                                            
                                    
                        processedHapaxes += processOneHebrewWord(word.text, wordTag)
                        processedHapaxes = processedHapaxes.replace("־ ", "־")
                        processedHapaxes = processedHapaxes.replace("> <", "><")
                        processedHapaxes = processedHapaxes + " "

            
                except:
                    continue

            processedHapaxes = processedHapaxes.replace("><H>", "> <H>")

            currentVerseDict["chapter"] = int(currentChapter)
            currentVerseDict["verse"] = int(currentVerse)
            currentVerseDict["textHapaxes"] = processedHapaxes.strip() + "׃"
            verseAddress = currentChapter + ":" + currentVerse
            finalJSONDict[verseAddress] = currentVerseDict

    openedJSON = open("./textJSON/" + originalName + ".json", "r", encoding="utf-8")
    openedJSONDict = json.load(openedJSON)
    openedJSON.close()

    existingJSONDict = {}
    for dict in openedJSONDict:
        existingJSONDict[str(dict["chapter"]) + ":" + str(dict["verse"])] = dict
    
    for dictAddress in existingJSONDict:
        if not dictAddress in finalJSONDict:
            print(bookName + " " + dictAddress)
            print(dictAddress in finalJSONDict)
        else:
            existingJSONDict[dictAddress]["grebrew"] = finalJSONDict[dictAddress]["textHapaxes"]

    allVerses = []
    for verse in existingJSONDict:
        allVerses.append(existingJSONDict[verse])

    newJSON = open("./textJSON/" + originalName + ".json", "w", encoding="utf-8")
    newJSON.write(json.dumps(allVerses, indent=2))
    newJSON.close()

    



def swapQereKetiv(bookName):
    myXML = open("./hebrewXML/" + bookName + ".xml", "r", encoding="utf-8")
    XMLLines = myXML.readlines()

    allLines = []
    for i in range(len(XMLLines) - 1):
        line = XMLLines[i].strip()
        nextLine = XMLLines[i+1].strip()
        if line.startswith("<k") and nextLine.startswith("<q"):
            allLines.append(XMLLines[i+1])
            allLines.append(XMLLines[i])
            i += 1
        elif not line.startswith("<q") and not line.startswith("<k"):
            allLines.append(XMLLines[i])
    allLines.append(XMLLines[-1])
    myXML.close()
    newFile = open("./hebrewXML/" + bookName + ".xml", "w", encoding="utf-8")
    for line in allLines:
        newFile.write(line)
    newFile.close()


processBookXML("Leviticus")
processBookXML("Exodus")