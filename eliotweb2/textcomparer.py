import difflib
import re
import json
import os
from hapaxgetter import getHapaxes, stripIrrelevantChars, cleanLineOfDiacritics
from trfiler import fileGreekLines
from sortingdata import allBookList
import pyuca

myCollator = pyuca.Collator()

def killHTMLTags(word):
    word = word.replace('<span style="color: red"><b>', '')
    word = word.replace('<span style="color: blue"><b>', '')
    word = word.replace('</b></span>', '')

    word = word.replace('<i>', '')
    word = word.replace('</i>', '')
    return word

def boldyRed(word):
    return '<span style="color: red"><b>' + word + '</b></span>'

def boldyBlue(word):
    return '<span style="color: blue"><b>' + word + '</b></span>'

def scrapFinalTaggedChar(word):
    irrelevantChars = ["{", "(", ")", "}", ":", ".", ",", "?", "[", "]", "–", "-", "/", "⸮", ";", "|", "¶"]
    cleanedWord = killHTMLTags(word)
    finalChar = ""
    if len(cleanedWord) > 0:
        if cleanedWord[-1] in irrelevantChars:
            finalChar = cleanedWord[-1]

        if cleanedWord[-1] in irrelevantChars and cleanedWord[-1] == word[-1]:
            return [word[0:-1], word[-1]]
        
        elif word.endswith('<span style="color: red"><b>' + finalChar + '</b></span>'):
            return [word[0:-len('<span style="color: red"><b>' + finalChar + '</b></span>')], '<span style="color: red"><b>' + finalChar + '</b></span>']
        
        elif word.endswith(finalChar + '</b></span>'):
            return [word[0:-len(finalChar + '</b></span>')], finalChar + '</b></span>']
        
        else:
            print('Error: ' + word)
        

def checkHapaxes(taggedWord, laxHapaxList, strictHapaxList):

    deHTMLedWord = killHTMLTags(taggedWord) 

    cleanWordStrict = cleanLineOfDiacritics(stripIrrelevantChars(deHTMLedWord))

    cleanWordLax = stripIrrelevantChars(deHTMLedWord)

    if cleanWordStrict in strictHapaxList:
        return '«' + taggedWord + '»'
    
    elif cleanWordLax in laxHapaxList:
        return "‹" + taggedWord + "›"
    
    else:
        return taggedWord

def compareWordsSameLength(word1, word2, ignoreCasing):

    word1Copy = word1
    word2Copy = word2

    finalWord1 = ""
    finalWord2 = ""

    compare = difflib.SequenceMatcher(None, word1Copy, word2Copy, autojunk=False).get_matching_blocks()[0:-1]

    caseInsensitiveCompare = difflib.SequenceMatcher(None, word1Copy.lower(), word2Copy.lower(), autojunk=False).get_matching_blocks()[0:-1]

    caseSensitiveCompare = difflib.SequenceMatcher(None, word1Copy, word2Copy, autojunk=False).get_matching_blocks()[0:-1]
    

    for i in range(len(word1Copy)):
        matchOnCase = False
        matchExceptOnCase = False

        for tuple in caseSensitiveCompare:
            if i >= tuple[0] and i < tuple[0] + tuple[2]:
                matchOnCase = True
                matchExceptOnCase = True
        
        if not matchOnCase:
            for tuple in caseInsensitiveCompare:
                if i >= tuple[0] and i < tuple[0] + tuple[2]:
                    matchExceptOnCase = True

        if matchOnCase or (matchExceptOnCase and ignoreCasing):
            finalWord1 += word1Copy[i]

        elif matchExceptOnCase:
            finalWord1 += '<span style="color: blue"><b>' + word1Copy[i] + '</b></span>'
        else:
            finalWord1 += '<span style="color: red"><b>' + word1Copy[i] + '</b></span>'

    for i in range(len(word2Copy)):
        matchOnCase = False
        matchExceptOnCase = False
        for tuple in caseSensitiveCompare:
            if i >= tuple[1] and i < tuple[1] + tuple[2]:
                matchOnCase = True
                matchExceptOnCase = True

        if not matchOnCase:
            for tuple in caseInsensitiveCompare:
                if i >= tuple[1] and i < tuple[1] + tuple[2]:
                    matchExceptOnCase = True

        if matchOnCase or (matchExceptOnCase and ignoreCasing):
            finalWord2 += word2Copy[i]

        elif matchExceptOnCase:
            finalWord2 += '<span style="color: blue"><b>' + word2Copy[i] + '</b></span>'

        else:
            finalWord2 += '<span style="color: red"><b>' + word2Copy[i] + '</b></span>'

    return [finalWord1, finalWord2]

def compareWordsDifferentLength(word1, word2, ignoreCasing):
    longerWord = max(word1, word2, key=len)
    shorterWord = min(word1, word2, key=len)

    firstWordIsLonger = (longerWord == word1)

    finalLongerChars = []
    finalShorterChars = []
        
    caseInsensitiveCompare = difflib.SequenceMatcher(None, longerWord.lower(), shorterWord.lower(), autojunk=False).get_matching_blocks()[0:-1]

    caseSensitiveCompare = difflib.SequenceMatcher(None, longerWord, shorterWord, autojunk=False).get_matching_blocks()[0:-1]
    
    for i in range(len(longerWord)):
        matchOnCase = False
        matchExceptOnCase = False
        for tuple in caseSensitiveCompare:
            if i >= tuple[0] and i < tuple[0] + tuple[2]:
                matchOnCase = True
                matchExceptOnCase = True
        
        if not matchOnCase:
            for tuple in caseInsensitiveCompare:
                if i >= tuple[0] and i < tuple[0] + tuple[2]:
                    matchExceptOnCase = True

        if matchOnCase or (matchExceptOnCase and ignoreCasing):
            finalLongerChars.append(longerWord[i])
        
        elif matchExceptOnCase:
            finalLongerChars.append('<span style="color: blue"><b>' + longerWord[i] + '</b></span>')

        else:
            finalLongerChars.append('<span style="color: red"><b>' + longerWord[i] + '</b></span>')

    for i in range(len(shorterWord)):
        
        matchOnCase = False
        matchExceptOnCase = False
        for tuple in caseSensitiveCompare:
            if i >= tuple[1] and i < tuple[1] + tuple[2]:
                matchOnCase = True
                matchExceptOnCase = True

        if not matchOnCase:
            for tuple in caseInsensitiveCompare:
                if i >= tuple[1] and i < tuple[1] + tuple[2]:
                    matchExceptOnCase = True

        if matchOnCase or (matchExceptOnCase and ignoreCasing):
            finalShorterChars.append(shorterWord[i])

        elif matchExceptOnCase:
            finalShorterChars.append('<span style="color: blue"><b>' + shorterWord[i] + '</b></span>')
        
        else:
            finalShorterChars.append('<span style="color: red"><b>' + shorterWord[i] + '</b></span>')

            
    finalLongerWord = re.sub('</u></b></span><span style="color: red"><b>', '', "".join(finalLongerChars))
    finalShorterWord = re.sub('</u></b></span><span style="color: red"><b>', '', "".join(finalShorterChars))

    if firstWordIsLonger:
        return [finalLongerWord, finalShorterWord]
    else:
        return [finalShorterWord, finalLongerWord]

def compareWords(word1, word2, ignoreCasing, laxHapaxList, strictHapaxList):
    newWord1 = word1.strip().replace(" ", "·")
    newWord2 = word2.strip().replace(" ", "·")

    if len(newWord1) == len(newWord2):
        finalWords = compareWordsSameLength(newWord1, newWord2, ignoreCasing)

    else:
        finalWords = compareWordsDifferentLength(newWord1, newWord2, ignoreCasing)

    word1CheckHapaxList = finalWords[0].split("·")
    word2CheckHapaxList = finalWords[1].split("·")

    newWord1 = ""
    newWord2 = ""

    irrelevantChars = ["{", "(", ")", "}", ":", ".", ",", "?", "[", "]", "–", "-", "/", "⸮", ";", "|", "¶"]

    for word in word1CheckHapaxList:
        if len(killHTMLTags(word)) > 0:
            finalChar = killHTMLTags(word)[-1]
            if finalChar in irrelevantChars:
                finalCharIndex = str.index(word, finalChar)
                wordPrefix = word[0:finalCharIndex]
                wordSuffix = word[finalCharIndex:]

                newWord1 += checkHapaxes(wordPrefix, laxHapaxList, strictHapaxList) + wordSuffix + "·"
            else:
                newWord1 += checkHapaxes(word, laxHapaxList, strictHapaxList) + "·"
    
    for word in word2CheckHapaxList:
        if len(killHTMLTags(word)) > 0:
            finalChar = killHTMLTags(word)[-1]
            if finalChar in irrelevantChars:
                finalCharIndex = str.index(word, finalChar)
                wordPrefix = word[0:finalCharIndex]
                wordSuffix = word[finalCharIndex:]

                newWord2 += checkHapaxes(wordPrefix, laxHapaxList, strictHapaxList) + wordSuffix + "·"
            else:
                newWord2 += checkHapaxes(word, laxHapaxList, strictHapaxList) + "·"

    newWord1 = newWord1.strip()
    newWord2 = newWord2.strip()

    finalList = []
    for newWord in [newWord1, newWord2]:

        newWord = newWord.replace('</b></span><span style="color: red"><b>', '')
        newWord = newWord.replace('<span style="color: red"><b>·</b></span>', '<span style="color: red"><b>˙</b></span>')
        newWord = newWord.replace('<span style="color: red"><b>$</b></span>', '<span style="color: red"><b>˙</b></span>')

        newWord = newWord.replace('·', ' ')
        newWord = newWord.replace('$', ' ')
        
        finalList.append(newWord)

    return finalList

def compareTexts(myBook, laxHapaxList, strictHapaxList):
    bookJSON = open("./textJSON/" + myBook + ".json", "w", encoding="utf-8")
    firstEditionLines = open("./texts/" + myBook + ".First Edition.txt", "r", encoding="utf-8").readlines()
    secondEditionLines = open("./texts/" + myBook + ".Second Edition.txt", "r", encoding="utf-8").readlines()
    
    firstEditionVerseDict = {}
    secondEditionVerseDict = {}
    allBooks = [firstEditionLines, secondEditionLines]
    allVerseDicts = [firstEditionVerseDict, secondEditionVerseDict]

    if myBook == "Psalms (prose)" or myBook == "John":
        mayhewLines = open("./texts/" + myBook + ".Mayhew.txt", "r", encoding="utf-8").readlines()
        allBooks.append(mayhewLines)
        mayhewVerseDict = {}
        allVerseDicts.append(mayhewVerseDict)

    if myBook == "Genesis":
        zerothEditionLines = open("./texts/" + myBook + ".Zeroth Edition.txt", "r", encoding="utf-8").readlines()
        allBooks.append(zerothEditionLines)
        zerothEditionVerseDict = {}
        allVerseDicts.append(zerothEditionVerseDict)
    
    KJVLines = open("./texts/" + myBook + ".KJV.txt", "r", encoding="utf-8").readlines()
    allBooks.append(KJVLines)
    KJVVerseDict = {}
    allVerseDicts.append(KJVVerseDict)

    allVerseList = []
    for i in range(len(allBooks)):
        numLines = 0
        for line in allBooks[i]:
            numLines += 1
            verse = line.split(" ")[0]
            if verse not in allVerseList:
                allVerseList.append(verse)


            lineText = line.split(" ")[1:]
            lineTextChecked = []
            for word in lineText:
                if len(word) > 0:
                    finalChar = word[-1]
                    irrelevantChars = ["{", "(", ")", "}", ":", ".", ",", "?", "[", "]", "–", "-", "/", "⸮", ";", "|", "¶"]
                    if finalChar in irrelevantChars:
                        finalCharIndex = str.index(word, finalChar)
                        wordPrefix = word[0:finalCharIndex]

                        wordSuffix = word[finalCharIndex:]

                        word = checkHapaxes(wordPrefix, laxHapaxList, strictHapaxList) + wordSuffix
                        lineTextChecked.append(word)
                    
                    else:
                        word = checkHapaxes(word, laxHapaxList, strictHapaxList)
                        lineTextChecked.append(word)

            if len(lineTextChecked) == 0:
                text = " "
            
            else:
                text = " ".join(lineTextChecked).strip()

            allVerseDicts[i][verse] = text
    
    
    allNTBooks = [
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
    if myBook in allNTBooks:
        grebrew = fileGreekLines(myBook)

    allJSONDicts = []
    for verseAddress in allVerseList:
        if verseAddress == "Epilogue\n" or verseAddress == "Epilogue":
            # fix this later
            continue

        try:
            chapter = verseAddress.split(".")[0]
            verse = verseAddress.split(".")[1]
        except:
            print(myBook + " " + verseAddress)

        finalDictionary = {}

        finalDictionary["fullverse"] = verseAddress
        finalDictionary["chapter"] = chapter
        finalDictionary["verse"] = verse

        finalDictionary["rawFirstEdition"] = allVerseDicts[0][verseAddress].replace('8', 'ꝏ̄').replace('{', '<i>').replace('}', '</i>')
        finalDictionary["rawSecondEdition"] = allVerseDicts[1][verseAddress].replace('8', 'ꝏ̄').replace('{', '<i>').replace('}', '</i>')

        comparedFirstAndSecondEdition = compareWords(allVerseDicts[0][verseAddress], allVerseDicts[1][verseAddress], False, laxHapaxList, strictHapaxList)
        comparedFirstEdition = comparedFirstAndSecondEdition[0].replace('8', 'ꝏ̄').replace('{', '<i>').replace('}', '</i>')
        comparedSecondEdition = comparedFirstAndSecondEdition[1].replace('8', 'ꝏ̄').replace('{', '<i>').replace('}', '</i>')
        finalDictionary["comparedFirstEdition"] = comparedFirstEdition
        finalDictionary["comparedSecondEdition"] = comparedSecondEdition

        caseInsensitiveFirstAndSecond = compareWords(allVerseDicts[0][verseAddress], allVerseDicts[1][verseAddress], True, laxHapaxList, strictHapaxList)

        caseInsensitiveFirst = caseInsensitiveFirstAndSecond[0].replace('8', 'ꝏ̄').replace('{', '<i>').replace('}', '</i>')
        caseInsensitiveSecond = caseInsensitiveFirstAndSecond[1].replace('8', 'ꝏ̄').replace('{', '<i>').replace('}', '</i>')

        finalDictionary["caseInsensitiveFirst"] = caseInsensitiveFirst
        finalDictionary["caseInsensitiveSecond"] = caseInsensitiveSecond

        if myBook == "Psalms (prose)" or myBook == "John":
            finalDictionary["rawMayhew"] = allVerseDicts[2][verseAddress].replace('8', 'ꝏ̄').replace('{', '<i>').replace('}', '</i>')

        if myBook == "Genesis":
            finalDictionary["rawZerothEdition"] = allVerseDicts[2][verseAddress].replace('8', 'ꝏ̄').replace('{', '<i>').replace('}', '</i>')

        finalDictionary["rawKJV"] = allVerseDicts[-1][verseAddress]

        if myBook in allNTBooks:
            if verseAddress in grebrew:
                finalDictionary["grebrew"] = grebrew[verseAddress]
            else:
                finalDictionary["grebrew"] = " "

        allJSONDicts.append(finalDictionary)
        
    bookJSON.write(json.dumps(allJSONDicts, indent=4))
    bookJSON.close()


myBookList = [
    "Exodus", 
    "Leviticus", 
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
    "Revelation"]

def addNewWordJSON(word, dictOfDicts):
    newDict = {}
    newDict["word"] = word
    newDict["wordCountDiacritics"] = 0
    newDict["allVersesDiacritics"] = []
    newDict["verseCountDiacritics"] = []
    newDict["editionCountDiacritics"] = 0
    newDict["allEditionsDiacritics"] = []
    newDict["allEditionsCountDiacritics"] = []
    
    if word == cleanLineOfDiacritics(word):
        newDict["wordCountNoDiacritics"] = 0
        newDict["allVersesNoDiacritics"] = []
        newDict["verseCountNoDiacritics"] = []
        newDict["editionCountNoDiacritics"] = 0
        newDict["allEditionsNoDiacritics"] = []
        newDict["allEditionsCountNoDiacritics"] = []

    dictOfDicts[word] = newDict

def splitOccurrences(verseCite):
    splitList = verseCite.split(" ")
    if len(splitList) == 1:
        return [splitList[0], 1]
    else:
        verse = splitList[0]
        occurrences = splitList[1][1:-1]
        return [verse, int(occurrences)]

def updateWordJSONCounts(word, diacriticStrictness, dictOfDicts, verseAddress, editionLetter, wordCount):

    if diacriticStrictness == "strict":
        fieldsDict = {
            "totalCount": "wordCountDiacritics",
            "verseList": "allVersesDiacritics",
            "verseCounts": "verseCountDiacritics",
            "editionTotalCount": "editionCountDiacritics",
            "editionList": "allEditionsDiacritics",
            "editionCounts": "allEditionsCountDiacritics",
        }

    elif diacriticStrictness == "lax":
        fieldsDict = {       
            "totalCount": "wordCountNoDiacritics",
            "verseList": "allVersesNoDiacritics",
            "verseCounts": "verseCountNoDiacritics",
            "editionTotalCount": "editionCountNoDiacritics",
            "editionList": "allEditionsNoDiacritics",
            "editionCounts": "allEditionsCountNoDiacritics"
        }

    if word not in dictOfDicts:
        addNewWordJSON(word, dictOfDicts)

    totalCount = fieldsDict["totalCount"]
    verseList = fieldsDict["verseList"]
    verseCounts = fieldsDict["verseCounts"]
    editionTotalCount = fieldsDict["editionTotalCount"]
    editionList = fieldsDict["editionList"]
    editionCounts = fieldsDict["editionCounts"]

    wordDict = dictOfDicts[word]

    if verseAddress not in wordDict[verseList]:
        wordDict[verseList].append(verseAddress)
        wordDict[verseCounts].append(wordCount)
        wordDict[totalCount] += wordCount

        if editionLetter in wordDict[editionList]:
            editionIndex = wordDict[editionList].index(editionLetter)
            wordDict[editionCounts][editionIndex] += wordCount

        else:
            wordDict[editionList].append(editionLetter)
            wordDict[editionCounts].append(wordCount)
            wordDict[editionTotalCount] += 1

    else:
        verseIndex = wordDict[verseList].index(verseAddress)
        previousCount = wordDict[verseCounts][verseIndex]
        wordDict[totalCount] -= previousCount        
        wordDict[verseCounts][verseIndex] = wordCount
        wordDict[totalCount] += wordCount

        if editionLetter in wordDict[editionList]:
            editionIndex = wordDict[editionList].index(editionLetter)
            wordDict[editionCounts][editionIndex] -= previousCount
            wordDict[editionCounts][editionIndex] += wordCount

        else:
            wordDict[editionList].append(editionLetter)
            wordDict[editionCounts].append(wordCount)
            wordDict[editionTotalCount] += 1

def updateVerseJSONS(editionLetter, book, verseLine, dictOfDicts):
    splitVerse = verseLine.split(" ")
    if splitVerse[0] == "Epilogue":
        verseAddress = editionLetter + "." + book + "." + "1000.0"
    else:
        verseAddress = editionLetter + "." + book + "." + splitVerse[0]
    #print("updateVerseJSONS works!" + splitVerse[0])
    wordCountDict = {}
    noDiacriticsCountDict = {}
    allWordList = []
    noDiacriticsWordList = []
    for word in splitVerse[1:]:
        word = stripIrrelevantChars(word)
        noDiacriticsWord = cleanLineOfDiacritics(word)

        if word not in wordCountDict:
            allWordList.append(word)
            wordCountDict[word] = 1
        else:
            wordCountDict[word] += 1

        if noDiacriticsWord not in noDiacriticsCountDict:
            noDiacriticsWordList.append(noDiacriticsWord)
            noDiacriticsCountDict[noDiacriticsWord] = 1

        else:
            noDiacriticsCountDict[noDiacriticsWord] += 1

    for word in allWordList:
        wordCount = wordCountDict[word]
        updateWordJSONCounts(word, "strict", dictOfDicts, verseAddress, editionLetter, wordCount)
    
    for word in noDiacriticsWordList:
        wordCount = noDiacriticsCountDict[word]
        updateWordJSONCounts(word, "lax", dictOfDicts, verseAddress, editionLetter, wordCount)
    
    affectedWords = allWordList + noDiacriticsWordList
    return(affectedWords)

def updateJSONSFromBook(bookName, bookLines, editionLetter, dictOfDicts):
    affectedWords = []
    for line in bookLines:
        affectedWords += updateVerseJSONS(editionLetter, bookName, line, dictOfDicts)

    return affectedWords

def updateJSONSAllBookEditions(bookName, dictOfDicts):
    affectedWords = []

    firstEditionLines = open("./texts/" + bookName + ".First Edition.txt", "r", encoding="utf-8").readlines()
    secondEditionLines = open("./texts/" + bookName + ".Second Edition.txt", "r", encoding="utf-8").readlines()
    affectedWords += updateJSONSFromBook(bookName, firstEditionLines, "α", dictOfDicts)
    affectedWords += updateJSONSFromBook(bookName, secondEditionLines, "β", dictOfDicts)

    if bookName == "Psalms (prose)" or bookName == "John":
        mayhewLines = open("./texts/" + bookName + ".Mayhew.txt", "r", encoding="utf-8").readlines()
        affectedWords += updateJSONSFromBook(bookName, mayhewLines, "M", dictOfDicts)

    if bookName == "Genesis":
        zerothEditionLines = open("./texts/" + bookName + ".Zeroth Edition.txt", "r", encoding="utf-8").readlines()
        affectedWords += updateJSONSFromBook(bookName, zerothEditionLines, "א", dictOfDicts)

    #print(affectedWords)
    newAffectedWords = []
    for word in affectedWords:
        if word not in newAffectedWords:
            newAffectedWords.append(word)
    newAffectedWords.sort(key=myCollator.sort_key)
    
    return [dictOfDicts, newAffectedWords]

def sortVerseAddresses(verseAddressList, verseCountList):
    addressToCountDict = {}
    for i in range(len(verseAddressList)):
        addressToCountDict[verseAddressList[i]] = verseCountList[i]
    
    editionLetterList = ["א", "α", "β", "M"]
    
    tupleList = []

    finalAddressList = []
    finalCountList = []
    for address in verseAddressList:
        verseCount = addressToCountDict[address]
        editionLetter = address[0]
        book = address.split(".")[1]
        editionIndex = editionLetterList.index(editionLetter)
        bookIndex = allBookList.index(book)
        chapter = int(address.split(".")[2])
        verse = int(address.split(".")[3])

        finalTuple = (bookIndex, chapter, verse, editionIndex, address, verseCount)

        tupleList.append(finalTuple)
    tupleList.sort()
    for tuple in tupleList:
        finalAddressList.append(tuple[4])
        finalCountList.append(tuple[5])

    return [finalAddressList, finalCountList]

def selectBookToUpdateJSONS(jsonAddress, bookName=""):
    if bookName == "":
        bookName = input("What book do you want to update? ").strip()
    else:
        bookName = bookName.strip()

    dictOfDicts = {}
    with (open(jsonAddress, "r", encoding="utf-8")) as jsonFile:
        try:
            jsonDicts = json.load(jsonFile)
            jsonFile.close()
            for dict in jsonDicts:
                dictOfDicts[dict["word"]] = dict
        except:
            pass
        
        jsonDicts = {}

        try:
            dictOfDicts = updateJSONSAllBookEditions(bookName, dictOfDicts)[0]
            affectedWords = updateJSONSAllBookEditions(bookName, dictOfDicts)[1]

            for word in affectedWords:
                sortedVerseCounts = sortVerseAddresses(dictOfDicts[word]["allVersesDiacritics"], dictOfDicts[word]["verseCountDiacritics"])

                dictOfDicts[word]["allVersesDiacritics"] = sortedVerseCounts[0]
                dictOfDicts[word]["verseCountDiacritics"] = sortedVerseCounts[1]

                if "wordCountNoDiacritics" in dictOfDicts[word]:
                    sortedVerseCounts = sortVerseAddresses(dictOfDicts[word]["allVersesNoDiacritics"], dictOfDicts[word]["verseCountNoDiacritics"])

                    dictOfDicts[word]["allVersesNoDiacritics"] = sortedVerseCounts[0]
                    dictOfDicts[word]["verseCountNoDiacritics"] = sortedVerseCounts[1]
            
            allHeadwords = list(dictOfDicts)
            print("There are " + str(len(allHeadwords)) + " headwords in the corpus (so far)")
            finalDictList = []
            for word in allHeadwords:
                finalDictList.append(dictOfDicts[word])
            with (open(jsonAddress, "w", encoding="utf-8")) as jsonFile:
                jsonFile.write(json.dumps(finalDictList, indent=4))
                jsonFile.close()
        except:
            print("Error updating " + bookName)

'''
for book in myBookList:
    selectBookToUpdateJSONS("./wordcounts.json", book)
    print(book + " done.")
'''

selectBookToUpdateJSONS("./wordcounts.json")