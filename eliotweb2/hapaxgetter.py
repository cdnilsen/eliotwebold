import pyuca
import json
myCollator = pyuca.Collator()

def cleanLineOfDiacritics(line):
    charReplacementDict = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "à": "a",
        "è": "e",
        "ì": "i",
        "ò": "o",
        "ù": "u",
        "â": "a",
        "ê": "e",
        "î": "i",
        "ô": "o",
        "û": "u",
        "ä": "a",
        "ë": "e",
        "ï": "i",
        "ö": "o",
        "ü": "u",
        "ã": "a",
        "õ": "o",
        "ñ": "nn",
        "m̃": "mm",
        "ũ": "u",
        "ẽ": "e",
        "ĩ": "i",
        "ā": "a",
        "ē": "e",
        "ī": "i",
        "ō": "o",
        "ū": "u"
    }
    diacritics = ["á", "é", "í", "ó", "ú", "à", "è", "ì", "ò", "ù", "â", "ê", "î", "ô", "û", "ä", "ë", "ï", "ö", "ü", "ã", "õ", "ñ", "m̃", "ũ", "ẽ", "ĩ", "ā", "ē", "ī", "ō", "ū"]
    for diacritic in diacritics:
        line = line.replace(diacritic, charReplacementDict[diacritic])
    return line

def stripIrrelevantChars(word):
    word = word.strip()
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
        if char not in irrelevantChars and char not in charReplacementDict:
            returnedWord += char
        elif char in charReplacementDict:
            returnedWord += charReplacementDict[char]
        else:
            followingChars += char

    return returnedWord.lower().strip()

def wordCountChecker(verseAddress, verseArray, wordCountDict, verseCountDict, allWordsList, wordEditionDict, editionLetter, editionCountDict):
    wordCountInVerseDict = {}
    cleanedWordArray = []
    for word in verseArray:
        cleanedWordArray.append(stripIrrelevantChars(word))

    for word in cleanedWordArray:
        if word not in wordCountInVerseDict:
            wordCountInVerseDict[word] = 1
        else:
            wordCountInVerseDict[word] += 1
    
    for word in cleanedWordArray:
        if word not in wordEditionDict:
            wordEditionDict[word] = [editionLetter]
            editionCountDict[word] = 1
        
        elif editionLetter not in wordEditionDict[word]:
            wordEditionDict[word].append(editionLetter)
            editionCountDict[word] += 1

        if word not in allWordsList:
            allWordsList.append(word)

        if word not in wordCountDict:
            wordCountDict[word] = 1
            verseCountDict[word] = [verseAddress]
        else:
            wordCountDict[word] += 1
            if verseAddress not in verseCountDict[word]:
                verseCountDict[word].append(verseAddress)

def getHapaxes(bookList):
    finalWordCountDictDiacritics = {} # e.g.: "kah", "1000"
    finalVerseCountDictDiacritics = {} # e.g.: ["Exodus.1.1", "Exodus.1.2"]
    wordEditionDictDiacritics = {} # e.g.: ["α", "β"]
    editionCountDictDiacritics = {}

    finalWordCountDictNoDiacritics = {}
    finalVerseCountDictNoDiacritics = {}
    wordEditionDictNoDiacritics = {}
    editionCountDictNoDiacritics = {}

    allWordsList = []

    for book in bookList:

        firstEditionFile = open("./texts/" + book + ".First Edition.txt", "r", encoding="utf-8")
        firstEditionLines = firstEditionFile.readlines()
        secondEditionFile = open("./texts/" + book + ".Second Edition.txt", "r", encoding="utf-8")
        secondEditionLines = secondEditionFile.readlines()

        allLinesList = [firstEditionLines, secondEditionLines]
        editionLetterList = ["α", "β"]

        if book == "John" or book == "Psalms (prose)":
            mayhewFile = open("./texts/" + book + ".Mayhew.txt", "r", encoding="utf-8")
            mayhewLines = mayhewFile.readlines()
            allLinesList.append(mayhewLines)
            editionLetterList.append("γ")
        
        if book == "Genesis":
            zerothEditionFile = open("./texts/" + book + ".Zeroth Edition.txt", "r", encoding="utf-8")
            zerothEditionLines = zerothEditionFile.readlines()
            allLinesList.append(zerothEditionLines)
            editionLetterList.append("א")

        for i in range(len(allLinesList)):
            editionLetter = editionLetterList[i]
            for line in allLinesList[i]:
                verseAddress = editionLetter + "." + book + "." + line.split(" ")[0]
                lineDiacritics = line.split(" ")[1:]
                lineNoDiacritics = cleanLineOfDiacritics(line).split(" ")[1:]

                # This is ugly, but consult the function above

                wordCountChecker(verseAddress, lineDiacritics, finalWordCountDictDiacritics, finalVerseCountDictDiacritics, allWordsList, wordEditionDictDiacritics, editionLetter, editionCountDictDiacritics)

                wordCountChecker(verseAddress, lineNoDiacritics, finalWordCountDictNoDiacritics, finalVerseCountDictNoDiacritics, allWordsList, wordEditionDictNoDiacritics, editionLetter, editionCountDictNoDiacritics)

    
    if "" in allWordsList:
        allWordsList.remove("")

    allWordsList.sort(key=myCollator.sort_key)
    allJSONDicts = []

    for word in allWordsList:
        wordDictionary = {}
        wordDictionary["word"] = word

        functionDictionaryList = [finalWordCountDictDiacritics, finalVerseCountDictDiacritics, editionCountDictDiacritics, wordEditionDictDiacritics, finalWordCountDictNoDiacritics, finalVerseCountDictNoDiacritics, editionCountDictNoDiacritics, wordEditionDictNoDiacritics]

        wordDictionaryKeys = ["wordCountDiacritics", "allVersesDiacritics", "editionCountDiacritics",  "allEditionsDiacritics", "wordCountNoDiacritics", "allVersesNoDiacritics", "editionCountNoDiacritics", "allEditionsNoDiacritics"]

        for i in range(len(functionDictionaryList)):
            if word in functionDictionaryList[i]:
                wordDictionary[wordDictionaryKeys[i]] = functionDictionaryList[i][word]
            else:
                if i % 2 == 0:
                    wordDictionary[wordDictionaryKeys[i]] = 0
                else:
                    wordDictionary[wordDictionaryKeys[i]] = []

        allJSONDicts.append(wordDictionary)

    finalJSONFile = open("./wordcounts.json", "w", encoding="utf-8")

    finalJSONFile.write(json.dumps(allJSONDicts, indent=4, ensure_ascii=False))
    finalJSONFile.close()


