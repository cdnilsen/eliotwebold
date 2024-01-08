#Example JSON entry:
'''
{
        "word": "nuttahshinnumunk",
        "wordCountDiacritics": 1,
        "allVersesDiacritics": [
            "John.13.18"
        ],
        "editionCountDiacritics": 1,
        "allEditionsDiacritics": [
            "β"
        ],
        "wordCountNoDiacritics": 2,
        "allVersesNoDiacritics": [
            "John.13.18"
        ],
        "editionCountNoDiacritics": 2,
        "allEditionsNoDiacritics": [
            "α",
            "β"
        ]
    },
'''

import json
from hapaxgetter import getHapaxes, stripIrrelevantChars

JSONFile = open("./wordcounts.json", "r", encoding="utf-8")


allMayhewWordsJSON = []
onlyMayhewWordsJSON = []

allWordCountDicts = json.load(JSONFile)
allWordCounter = 0
trueHapaxCounter = 0
oneVerseCounter = 0
allMayhew = 0
mayhewOnly = 0
for dict in allWordCountDicts:
    allWordCounter += 1
    if "γ" in dict["allEditionsDiacritics"]:
        allMayhewWordsJSON.append(dict["word"])
        allMayhew += 1
        if len(dict["allEditionsDiacritics"]) == 1:
            onlyMayhewWordsJSON.append(dict["word"])
            mayhewOnly += 1
    if len(dict["allVersesDiacritics"]) == 1:
        if dict["editionCountDiacritics"] == 1:
            trueHapaxCounter += 1
        else:
            oneVerseCounter += 1

print("Total words: " + str(allWordCounter))
print("True hapax legomena: " + str(trueHapaxCounter))
print("Words appearing in only one verse: " + str(oneVerseCounter))
print("Mayhew words: " + str(allMayhew))
print("Mayhew-only words: " + str(mayhewOnly))



print(len(allMayhewWordsJSON))
allWordsList = []
allWordCount = 0

mayhewJohn = open("./texts/John.Mayhew.txt", "r", encoding="utf-8").readlines()

for line in mayhewJohn:
    strippedLine = stripIrrelevantChars(line).split(" ")[1:]
    for word in strippedLine:
        if word not in allWordsList:
            allWordsList.append(word)
            allWordCount += 1
        if word == "":
            print(line)

for word in onlyMayhewWordsJSON:
    print(word)


