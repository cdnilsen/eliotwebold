import os
from textdisplayfunctions import stripIrrelevantChars, replace_keep_case, cleanLineOfDiacritics
import re

def tagWordsInLine(line, taggedWordList, gloss, ignoreDiacritics = False):
    irrelevantChars = ["{", "(", ")", "}", ":", ".", ",", "?", "[", "]", "–", "-", "/", "⸮", ";", "|", "¶"]
    lineList = line.split(" ")
    newLineList = []
    if ignoreDiacritics:
        newTestWordList = []
        for word in taggedWordList:
            newTestWordList.append(cleanLineOfDiacritics(stripIrrelevantChars(word).lower()))
        taggedWordList = newTestWordList
    for word in lineList:
        newLineList.append(word.strip())
    lineList = newLineList
    totalTokenCount = 0
    totalWordCount = 0
    totalGlossed = 0
    wordInLine = False
    for word in lineList:
        totalWordCount += 1
        punctuation = ""
        wordToAdd = word
        try:
            if word[-1] in irrelevantChars:
                punctuation = word[-1]
                wordToAdd = word[:-1]
        except:
            print("!!ERROR: " + word)
            punctuation = ""
            wordToAdd = word
        if ignoreDiacritics:
            testWord = cleanLineOfDiacritics(stripIrrelevantChars(word).lower())
        else:
            testWord = stripIrrelevantChars(word).lower()
        if testWord in taggedWordList:
            try:
                wordInLine = True
                lineList[lineList.index(word)] = wordToAdd + "«" + gloss + "»" + punctuation
            except:
                print("??ERROR: " + word)
                print(lineList)
            totalTokenCount += 1
            totalGlossed += 1
        elif "«" + gloss + "»" in word:
            totalTokenCount += 1
            totalGlossed += 1
        elif "«" in word:
            totalGlossed += 1
    returnedLine =  " ".join(lineList).strip() + "\n"
    return (returnedLine, totalTokenCount, totalWordCount, totalGlossed, wordInLine)


def getKJVWordCount(line, gloss):
    lineList = line.split(" ")
    totalCount = 0
    for word in lineList:
        if stripIrrelevantChars(word).lower() == gloss:
            totalCount += 1
    return totalCount

removeKJVFromTagged = False
if removeKJVFromTagged:
    taggedTexts = os.listdir("./texts/tagged/")
    for text in taggedTexts:
        if text.endswith("KJV.txt"):
            os.remove("./texts/tagged/" + text)
    quit()

completedTexts = ["1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude"]
useListOfCompletedTexts = True

if not useListOfCompletedTexts:
    completedText = input("Enter the name of an entirely proofread text: ").strip()
    completedTexts = [completedText]

massWordsToTag = input("Enter words to tag (separated by commas): ").strip()
allMassWords = []
for word in massWordsToTag.split(","):
    allMassWords.append(word.strip().lower())

englishHeadword = input("Enter the English headword: ").strip()

ignoreDiacritics = input("Ignore diacritics? (y/n): ").strip()
if ignoreDiacritics == "y":
    ignoreDiacritics = True
else:
    ignoreDiacritics = False

totalErrorCount = 0

allFirstEditionTotalCounts = []
allFirstEditionTaggedCounts = []
allFirstEditionTotalTagged = []

allSecondEditionTotalCounts = []
allSecondEditionTaggedCounts = []
allSecondEditionTotalTagged = []

checkErrors = True

for completeBook in completedTexts:
    firstEdition = open("./texts/tagged/" + completeBook + ".First Edition.txt", "r", encoding="utf-8")
    secondEdition = open("./texts/tagged/" + completeBook + ".Second Edition.txt", "r", encoding="utf-8")
    KJV = open("./texts/" + completeBook + ".KJV.txt", "r", encoding="utf-8")
    firstEditionLines = firstEdition.readlines()
    secondEditionLines = secondEdition.readlines()
    KJVLines = KJV.readlines()

    firstEditionFinishedLines = []
    secondEditionFinishedLines = []

    firstEditionTotalWordCount = 0
    firstEditionTaggedWordCount = 0
    firstEditionTotalTagged = 0

    secondEditionTotalWordCount = 0
    secondEditionTaggedWordCount = 0
    secondEditionTotalTagged = 0

    for i in range(min(len(firstEditionLines), len(secondEditionLines), len(KJVLines))):
        
        firstEditionTuple = tagWordsInLine(firstEditionLines[i], allMassWords, englishHeadword, ignoreDiacritics)
        secondEditionTuple = tagWordsInLine(secondEditionLines[i], allMassWords, englishHeadword, ignoreDiacritics)
        kjvCount = getKJVWordCount(KJVLines[i], englishHeadword)

        firstEditionFinishedLines.append(firstEditionTuple[0])
        secondEditionFinishedLines.append(secondEditionTuple[0])
        
        firstEditionTaggedWordCount += firstEditionTuple[1]
        firstEditionTotalWordCount += firstEditionTuple[2]
        firstEditionTotalTagged += firstEditionTuple[3]

        secondEditionTaggedWordCount += secondEditionTuple[1]
        secondEditionTotalWordCount += secondEditionTuple[2]
        secondEditionTotalTagged += secondEditionTuple[3]
        
        
        if checkErrors:
            countsAreOff = firstEditionTuple[1] != secondEditionTuple[1] or firstEditionTuple[1] != kjvCount or secondEditionTuple[1] != kjvCount
            wordInLine = firstEditionTuple[4] or secondEditionTuple[4]
            if wordInLine and countsAreOff:
                totalErrorCount += 1
                print("ERROR AT: " + completeBook + " " + firstEditionLines[i].split(' ')[0] + ":")
                print("First Edition: " + firstEditionTuple[0] + "(" + str(firstEditionTuple[1]) + ")" )
                print("Second Edition: " + secondEditionTuple[0] + "(" + str(secondEditionTuple[1]) + ")" )
                print("KJV: " + KJVLines[i] + "(" + str(kjvCount) + ")" )

    allFirstEditionTotalCounts.append(firstEditionTotalWordCount)
    allFirstEditionTaggedCounts.append(firstEditionTaggedWordCount)
    allFirstEditionTotalTagged.append(firstEditionTotalTagged)

    allSecondEditionTotalCounts.append(secondEditionTotalWordCount)
    allSecondEditionTaggedCounts.append(secondEditionTaggedWordCount)
    allSecondEditionTotalTagged.append(secondEditionTotalTagged)

    
    firstEditionFinal = open("./texts/tagged/" + completeBook + ".First Edition.txt", "w", encoding="utf-8")
    secondEditionFinal = open("./texts/tagged/" + completeBook + ".Second Edition.txt", "w", encoding="utf-8")

    firstEditionFinal.writelines(firstEditionFinishedLines)
    secondEditionFinal.writelines(secondEditionFinishedLines)
    firstEditionFinal.close()
    secondEditionFinal.close()
    

if checkErrors:
    print("Total error count: " + str(totalErrorCount))


for i in range(len(completedTexts)):
    print("Tokens of «" + englishHeadword + "» in " + completedTexts[i] + " α: " + str(allFirstEditionTaggedCounts[i]) + " (" + str(allFirstEditionTotalTagged[i]) + "/" + str(allFirstEditionTotalCounts[i]) + " total tagged)")
    print("Tokens of «" + englishHeadword + "» in " + completedTexts[i] + " β: " + str(allSecondEditionTaggedCounts[i]) + " (" + str(allSecondEditionTotalTagged[i]) + "/" + str(allSecondEditionTotalCounts[i]) + " total tagged)")