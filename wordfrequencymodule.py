import os
import re
import pyuca
from textdisplayfunctions import charReplacementDict, cleanLineOfDiacritics, displayLine

myCollator = pyuca.Collator()

#NT only, for now
allBookList = [
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1 Corinthians",
    "2 Corinthians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1 Thessalonians",
    "2 Thessalonians",
    "1 Timothy",
    "2 Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1 Peter",
    "2 Peter",
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation"
]

def stripIrrelevantChars(word):
    irrelevantChars = ["{", "(", ")", "}", ":", ".", ",", "?", "[", "]", "–", "-", "/", "⸮", ";", "|", "¶"]
    returnedWord = ""
    followingChars = ""

    charReplacementDict = {
        "ᴏ": "o",
        "ʀ": "r",
        "ᴅ": "d",
        "ɴ": "n",
        "$": " "
    }
    for char in word:
        if char not in irrelevantChars:
            returnedWord += char
        elif char in charReplacementDict:
            returnedWord += charReplacementDict[char]
        else:
            followingChars += char
    return returnedWord.lower().strip()

def getHapaxes(strictDiacritics):
    #hapaxFile = open("hapaxLegomena.txt", "w", encoding="utf-8")

    allWordDictionary = {}
    allWordList = []
    allHapaxList = []
    for book in allBookList:
        firstEditionFile = open("./texts/" + book + ".First Edition.txt", "r", encoding="utf-8")
        firstEditionLines = firstEditionFile.readlines()

        for line in firstEditionLines:
            lineText = line.split(" ")[1:]
            for word in lineText:
                if strictDiacritics:
                    word = stripIrrelevantChars(word).lower()
                else:
                    word = cleanLineOfDiacritics(stripIrrelevantChars(word)).lower()
                if word in allWordDictionary:
                    allWordDictionary[word] += 1
                else:
                    allWordList.append(word)
                    allWordDictionary[word] = 1

        secondEditionFile = open("./texts/" + book + ".Second Edition.txt", "r", encoding="utf-8")
        secondEditionLines = secondEditionFile.readlines()

        for line in secondEditionLines:
            lineText = line.split(" ")[1:]
            for word in lineText:
                if strictDiacritics:
                    word = stripIrrelevantChars(word).lower()
                else:
                    word = cleanLineOfDiacritics(stripIrrelevantChars(word)).lower()
                if word in allWordDictionary:
                    allWordDictionary[word] += 1
                else:
                    allWordList.append(word)
                    allWordDictionary[word] = 1

        if book == "John":
            mayhewFile = open("./texts/" + book + ".Mayhew.txt", "r", encoding="utf-8")
            mayhewLines = mayhewFile.readlines()
            for line in mayhewLines:
                lineText = line.split(" ")[1:]
                for word in lineText:
                    if strictDiacritics:
                        word = stripIrrelevantChars(word).lower()
                    else:
                        word = cleanLineOfDiacritics(stripIrrelevantChars(word)).lower()
                    if word in allWordDictionary:
                        allWordDictionary[word] += 1
                    else:
                        allWordList.append(word)
                        allWordDictionary[word] = 1

    print("unnunog: " + str(allWordDictionary["unnunog"]))
    allWordList.sort(key=myCollator.sort_key)
    for word in allWordList:
        if allWordDictionary[word] == 1:
            allHapaxList.append(word)

    return allHapaxList

    
def populateHapaxes():
    hapaxStrictFile = open("hapaxLegomenaStrict.txt", "w", encoding="utf-8")
    hapaxLaxFile = open("hapaxLegomenaLax.txt", "w", encoding="utf-8")

    allStrictHapaxes = getHapaxes(True)
    strictHapaxList = []
    for hapax in allStrictHapaxes:
        strictHapaxList.append(hapax)

    strictHapaxList.sort(key=myCollator.sort_key)
    for hapax in strictHapaxList:
        hapaxStrictFile.write(hapax + "\n")

    hapaxStrictFile.close()

    allLaxHapaxes = getHapaxes(False)
    laxHapaxCountDict = {}
    laxHapaxList = []
    for hapax in allLaxHapaxes:
        if cleanLineOfDiacritics(hapax) not in laxHapaxCountDict:
            laxHapaxCountDict[cleanLineOfDiacritics(hapax)] = 1
            laxHapaxList.append(cleanLineOfDiacritics(hapax))
        else:
            laxHapaxCountDict[cleanLineOfDiacritics(hapax)] += 1

    laxHapaxList.sort(key=myCollator.sort_key)
    for hapax in laxHapaxList:
        if laxHapaxCountDict[hapax] == 1:
            hapaxLaxFile.write(hapax + "\n")

#populateHapaxes()

def fetchHapaxes(normalizeDiacritics):
    if normalizeDiacritics:
        hapaxFile = open("hapaxLegomenaLax.txt", "r", encoding="utf-8")
    else:
        hapaxFile = open("hapaxLegomenaStrict.txt", "r", encoding="utf-8")

    hapaxLines = hapaxFile.readlines()
    hapaxList = []
    for line in hapaxLines:
            hapaxList.append(line.strip())

    return hapaxList

def processWordForHapax(word, normalizeDiacritics=False):
    word = stripIrrelevantChars((word.replace("<red><b>", "").replace("</b></span>", "").lower()))

    if normalizeDiacritics:
        word = cleanLineOfDiacritics(word)

    return word

def hapaxUnderlining(word, hapaxList, diacriticsLax):
    irrelevantChars = ["{", "(", ")", "}", ":", ".", ",", "?", "[", "]", "–", "-", "/", "⸮", ";", "|", "¶"]
    finalString = ""
    
    wordIsAHapax = processWordForHapax(word, diacriticsLax) in hapaxList
    if not wordIsAHapax:
        finalString = word + " "
    else:
        deHighlightedWord = word.replace("<red><b>", "«").replace("</b></span>", "»")
        hasFinalPunctuation = deHighlightedWord[-1] in irrelevantChars
        hasPenultimatePunctuation = deHighlightedWord[-2] in irrelevantChars

        if hasFinalPunctuation:
            finalString = ("<u>" + deHighlightedWord[:-1] + "</u>" + deHighlightedWord[-1]).replace("«", "<red><b>").replace("»", "</b></span>") + " "
        elif hasPenultimatePunctuation:
            finalString = ("<u>" + deHighlightedWord[:-2] + "</u>" + deHighlightedWord[-2:]).replace("«", "<red><b>").replace("»", "</b></span>") + " "
        else:
            finalString = ("<u>" + deHighlightedWord + "</u>").replace("«", "<red><b>").replace("»", "</b></span>") + " "

    return finalString

        
