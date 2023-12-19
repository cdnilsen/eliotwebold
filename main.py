from flask import Flask, flash, request, jsonify, render_template, redirect, url_for, Blueprint, abort
from markupsafe import Markup
import os
from werkzeug.utils import secure_filename
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape

from textdisplayfunctions import charReplacementDict, cleanLineOfDiacritics, displayLine

from proofreadingfunctions import doVerseComparison, compareWords

allBookList = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1 Samuel",
    "2 Samuel",
    "1 Kings",
    "2 Kings",
    "1 Chronicles",
    "2 Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    "Psalms (prose)",
    "Psalms (metrical)",
    "Proverbs",
    "Ecclesiastes",
    "Song of Songs",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi", 
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

bookToChapterDictionary = {
    "Genesis": 50,
    "Exodus": 40,
    "Leviticus": 27,
    "Numbers": 36,
    "Deuteronomy": 34,
    "Joshua": 24,
    "Judges": 21,
    "Ruth": 4,
    "1 Samuel": 31,
    "2 Samuel": 24,
    "1 Kings": 22,
    "2 Kings": 25,
    "1 Chronicles": 29,
    "2 Chronicles": 36,
    "Ezra": 10,
    "Nehemiah": 13,
    "Esther": 10,
    "Job": 42,
    "Psalms (prose)": 150,
    "Psalms (metrical)": 150,
    "Proverbs": 31,
    "Ecclesiastes": 12,
    "Song of Songs": 8,
    "Isaiah": 66,
    "Jeremiah": 52,
    "Lamentations": 5,
    "Ezekiel": 48,
    "Daniel": 12,
    "Hosea": 14,
    "Joel": 3,
    "Amos": 9,
    "Obadiah": 1,
    "Jonah": 4,
    "Micah": 7,
    "Nahum": 3,
    "Habakkuk": 3,
    "Zephaniah": 3,
    "Haggai": 2,
    "Zechariah": 14,
    "Malachi": 4,
    "Matthew": 28,
    "Mark": 16,
    "Luke": 24,
    "John": 21,
    "Acts": 28,
    "Romans": 16,
    "1 Corinthians": 16,
    "2 Corinthians": 13,
    "Galatians": 6,
    "Ephesians": 6,
    "Philippians": 4,
    "Colossians": 4,
    "1 Thessalonians": 5,
    "2 Thessalonians": 3,
    "1 Timothy": 6,
    "2 Timothy": 4,
    "Titus": 3,
    "Philemon": 1,
    "Hebrews": 13,
    "James": 5,
    "1 Peter": 5,
    "2 Peter": 3,
    "1 John": 5,
    "2 John": 1,
    "3 John": 1,
    "Jude": 1,
    "Revelation": 22
}


UPLOAD_FOLDER = 'texts'
ALLOWED_EXTENTIONS = {'txt'}

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def mainPage():
    return render_template('index.html')

@app.route("/morphsearch", methods=['GET', 'POST'])
def morphsearch():
    if request.method == 'POST':
        return render_template(url_for('morphsearch.html'))

    return render_template('morphsearch.html')

@app.route("/searchenglish", methods=['GET', 'POST'])
def searchenglish():
    if request.method == 'POST':
        return render_template(url_for('searchenglish.html'))

    return render_template('searchenglish.html')

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

def cleanLineOfDiacritics(line):
    diacritics = ["á", "é", "í", "ó", "ú", "à", "è", "ì", "ò", "ù", "â", "ê", "î", "ô", "û", "ä", "ë", "ï", "ö", "ü", "ã", "õ", "ñ", "m̃", "ũ", "ẽ", "ĩ", "ā", "ē", "ī", "ō", "ū"]
    for diacritic in diacritics:
        line = line.replace(diacritic, charReplacementDict[diacritic])
    return line

def getMatchingLines(indexDict, book, edition, editionVerseList):

    textPath = './texts/' + book + '.' + edition + '.txt'
    if len(indexDict[book]) > 0 and os.path.exists(textPath):
                with open(textPath, 'r', encoding="utf-8") as f:
                    bookLines = f.readlines()
                    for i in indexDict[book]:
                        if i < len(bookLines):
                            verseText = " ".join(bookLines[i].split(" ")[1:])
                            editionVerseList.append(verseText.replace('8', 'ꝏ̄'))
                        else:
                            editionVerseList.append(" ")
                f.close()
    else:
        for i in indexDict[book]:
            editionVerseList.append(" ")
     
@app.route("/doenglishsearch", methods=['GET', 'POST'])
def doenglishsearch():
    word = request.form['search_query']

    includeKJV = True
    includeFirstEdition = request.form.get('include_first_edition') == 'on'
    includeSecondEdition = request.form.get('include_second_edition') == 'on'
    includeMayhew = request.form.get('include_mayhew') == 'on'
    includeZerothEdition = request.form.get('include_zeroth_edition') == 'on'

    anyWordsInGenesis = False
    anyWordsInPsalms = False
    anyWordsInJohn = False

    matchingBooks = []
    matchingIndices = []
    matchingVerses = []
    matchingKJV = []
    matchingFirstEdition = []
    matchingSecondEdition = []
    matchingMayhew = []
    matchingZerothEdition = []

    finalMatches = []
    finalKJVVerses = []
    bookIndexDictionary = {}

    verseIndexDictionary = {}

    numMatches = 0
    for book in allBookList:
        if book not in bookIndexDictionary:
            bookIndexDictionary[book] = []
        with open('./texts/' + book + '.KJV.txt', 'r', encoding="utf-8") as f:
            KJVbookLines = f.readlines()
            for i in range(len(KJVbookLines)):
                verse = KJVbookLines[i]
                if word in verse:
                    if book == "Genesis":
                        anyWordsInGenesis = True
                    if book == "Psalms (prose)" or book == "Psalms (metrical)":
                        anyWordsInPsalms = True
                    if book == "John":
                        anyWordsInJohn = True

                    matchingIndices.append(numMatches)
                    
                    bookIndexDictionary[book].append(i)

                    verseNum = "<b>" + book + " " + verse.split(" ")[0] + "</b>: "
                    matchingVerses.append(Markup(verseNum))

                    newVerse = " ".join(verse.split(" ")[1:])
                    newVerse = newVerse.replace(word, "<span style='color:red'><b>" + word + "</b></span>")
                    newVerse = verseNum + newVerse
                    MarkedVerse = Markup(newVerse)
                    finalKJVVerses.append(MarkedVerse)

                    numMatches += 1
        f.close()

    for book in bookIndexDictionary:
        getMatchingLines(bookIndexDictionary, book, 'First Edition', matchingFirstEdition)
        getMatchingLines(bookIndexDictionary, book, 'Second Edition', matchingSecondEdition)
        getMatchingLines(bookIndexDictionary, book, 'Mayhew', matchingMayhew)
        getMatchingLines(bookIndexDictionary, book, 'Zeroth Edition', matchingZerothEdition)

    for index in matchingIndices:

        verseIndexDictionary[index] = {}
        verseIndexDictionary[index]['Verse'] = matchingVerses[index]

        verseIndexDictionary[index]['KJV'] = finalKJVVerses[index]

        verseIndexDictionary[index]['FirstEdition'] = matchingFirstEdition[index]

        verseIndexDictionary[index]['SecondEdition'] = matchingSecondEdition[index]

        verseIndexDictionary[index]['Mayhew'] = matchingMayhew[index]

        verseIndexDictionary[index]['ZerothEdition'] = matchingZerothEdition[index]
    
    includeMayhew = includeMayhew and (anyWordsInJohn or anyWordsInPsalms)
    includeZerothEdition = includeZerothEdition and (anyWordsInGenesis)

    return render_template('searchenglish.html', verseIndices = matchingIndices, verseDictionary = verseIndexDictionary, KJVIncluded = includeKJV, firstEditionIncluded = includeFirstEdition, secondEditionIncluded = includeSecondEdition, mayhewIncluded = includeMayhew, zerothEditionIncluded = includeZerothEdition)


@app.route("/searchmass", methods=['GET', 'POST'])
def searchmass():
    if request.method == 'POST':
        return render_template(url_for('searchmass.html'))
    
    return render_template('searchmass.html')

def getMatchingLinesMass(indexDict, book, edition, editionVerseList, useStrictDiacritics):

    textPath = './texts/' + book + '.' + edition + '.txt'
    if len(indexDict[book]) > 0 and os.path.exists(textPath):
                with open(textPath, 'r', encoding="utf-8") as f:
                    bookLines = f.readlines()
                    for i in indexDict[book]:
                        if i < len(bookLines):
                            if useStrictDiacritics:
                                verseText = cleanLineOfDiacritics(bookLines[i])
                            else:
                                verseText = bookLines[i]
                            editionVerseList.append(verseText.replace('8', 'ꝏ̄'))
                        else:
                            editionVerseList.append(" ")
                f.close()
    else:
        for i in indexDict[book]:
            editionVerseList.append(" ")


@app.route("/domasssearch", methods=['GET', 'POST'])
def domasssearch():

    word = request.form['search_query']
    
    includeKJV = True
    includeFirstEdition = request.form.get('include_first_edition') == 'on'
    includeSecondEdition = request.form.get('include_second_edition') == 'on'
    includeMayhew = request.form.get('include_mayhew') == 'on'
    includeZerothEdition = request.form.get('include_zeroth_edition') == 'on'

    strictDiacritics = request.form['diacritic_strictness'] == 'strict'

    if not strictDiacritics:
        word = cleanLineOfDiacritics(word)

    matchingBooks = []
    matchingIndices = []
    matchingVerses = []
    matchingKJV = []
    matchingFirstEdition = []
    matchingSecondEdition = []
    matchingMayhew = []
    matchingZerothEdition = []


    includeKJV = True
    useFirstEdition = False
    useSecondEdition = False
    useMayhew = False
    useZerothEdition = False

    totalFirstEdition = 0
    totalSecondEdition = 0
    totalMayhew = 0
    totalZerothEdition = 0
    totalAll = 0

    finalMatches = []
    finalKJVVerses = []
    bookIndexDictionary = {}

    verseIndexDictionary = {}

    numMatches = 0

    for book in allBookList:
        if book not in bookIndexDictionary:
            bookIndexDictionary[book] = []

            allVersesList = []

            kjvLineDict = {}
            firstEditionLineDict = {}
            secondEditionLineDict = {}
            mayhewLineDict = {}
            zerothEditionLineDict = {}
            printWhichVersesDict = {}

            hasMayhew = (book == "Psalms (prose)" or book == "John") and includeMayhew
            hasZerothEdition = (book == "Genesis") and includeZerothEdition

            KJVF = open('./texts/' + book + '.KJV.txt', 'r', encoding="utf-8")
            for line in KJVF.readlines():
                verseNum = line.split(" ")[0].strip()
                verseText = " ".join(line.split(" ")[1:])
                kjvLineDict[verseNum] = verseText
                
                firstEditionLineDict[verseNum] = ""
                secondEditionLineDict[verseNum] = ""

                if hasMayhew:
                    mayhewLineDict[verseNum] = ""

                if hasZerothEdition:
                    zerothEditionLineDict[verseNum] = ""

                printWhichVersesDict[verseNum] = False
                allVersesList.append(verseNum)

                
            if includeFirstEdition and os.path.exists('./texts/' + book + '.First Edition.txt'):
                FirstEditionF = open('./texts/' + book + '.First Edition.txt', 'r', encoding="utf-8")
                for line in FirstEditionF.readlines():
                    
                    verseNum = line.split(" ")[0].strip()
                    verseAddress = "<b>" + book + " " + verseNum + "</b>: "
                    if verseAddress not in matchingVerses:
                        matchingVerses.append(Markup(verseAddress))

                    lineDataDict = displayLine(line, strictDiacritics, allVersesList, word, firstEditionLineDict, printWhichVersesDict)
                    
                    wordInLineFirstEd = lineDataDict["lineHasWord"]

                    if wordInLineFirstEd:
                        useFirstEdition = True
                        totalFirstEdition += lineDataDict["numTokens"]

                FirstEditionF.close()

            if includeSecondEdition and os.path.exists('./texts/' + book + '.Second Edition.txt'):
                SecondEditionF = open('./texts/' + book + '.Second Edition.txt', 'r', encoding="utf-8")
                for line in SecondEditionF.readlines():

                    verseNum = line.split(" ")[0].strip()
                    verseAddress = "<b>" + book + " " + verseNum + "</b>: "
                    if verseAddress not in matchingVerses:
                        matchingVerses.append(Markup(verseAddress))

                    lineDataDict = displayLine(line, strictDiacritics, allVersesList, word, secondEditionLineDict, printWhichVersesDict)

                    wordInLineSecondEd = lineDataDict["lineHasWord"]
                    
                    if wordInLineSecondEd:
                        useSecondEdition = True
                        totalSecondEdition += lineDataDict["numTokens"]

                SecondEditionF.close()

            if hasMayhew and os.path.exists('./texts/' + book + '.Mayhew.txt'):
                MayhewF = open('./texts/' + book + '.Mayhew.txt', 'r', encoding="utf-8")
                for line in MayhewF.readlines():
                    
                    lineDataDict = displayLine(line, strictDiacritics, allVersesList, word, mayhewLineDict, printWhichVersesDict)

                    verseNum = line.split(" ")[0].strip()
                    verseAddress = "<b>" + book + " " + verseNum + "</b>: "
                    if verseAddress not in matchingVerses:
                        matchingVerses.append(Markup(verseAddress))

                    wordInLineMayhew = lineDataDict["lineHasWord"]

                    if wordInLineMayhew:
                        useMayhew = True
                        totalMayhew += lineDataDict["numTokens"]
                        
                MayhewF.close()

            if hasZerothEdition and os.path.exists('./texts/' + book + '.Zeroth Edition.txt'):
                ZerothEditionF = open('./texts/' + book + '.Zeroth Edition.txt', 'r', encoding="utf-8")
                for line in ZerothEditionF.readlines():
                    lineDataDict = displayLine(line, strictDiacritics, allVersesList, word, zerothEditionLineDict, printWhichVersesDict)

                    verseNum = line.split(" ")[0].strip()
                    verseAddress = "<b>" + book + " " + verseNum + "</b>: "
                    if verseAddress not in matchingVerses:
                        matchingVerses.append(Markup(verseAddress))

                    wordInLineZerothEd = lineDataDict["lineHasWord"]

                    if wordInLineZerothEd:
                        useZerothEdition = True
                        totalZerothEdition += lineDataDict["numTokens"]

                ZerothEditionF.close()

            for verseNum in allVersesList:
                if printWhichVersesDict[verseNum]:
                    matchingIndices.append(numMatches)
                    verseIndexDictionary[numMatches] = Markup("<b>" + book + "</b> " + verseNum)
                    numMatches += 1
                    matchingKJV.append(kjvLineDict[verseNum])
                    matchingFirstEdition.append(firstEditionLineDict[verseNum])
                    matchingSecondEdition.append(secondEditionLineDict[verseNum])
                    if hasMayhew:
                        matchingMayhew.append(mayhewLineDict[verseNum])
                    else:
                        matchingMayhew.append("")
                    if hasZerothEdition:
                        matchingZerothEdition.append(zerothEditionLineDict[verseNum])
                    else:
                        matchingZerothEdition.append("")


    includeKJV = len(matchingKJV) > 0
    includeFirstEdition = includeFirstEdition and useFirstEdition and len(matchingFirstEdition) > 0
    includeSecondEdition = includeSecondEdition and useSecondEdition and len(matchingSecondEdition) > 0
    includeMayhew = includeMayhew and useMayhew and len(matchingMayhew) > 0
    includeZerothEdition = includeZerothEdition and useZerothEdition and len(matchingZerothEdition) > 0

    totalAll = str(totalFirstEdition + totalSecondEdition + totalMayhew + totalZerothEdition)

    totalVerseCount = len(matchingIndices)

    rightColumns = []
    if includeFirstEdition:
        rightColumns.append(1)
    if includeSecondEdition:
        rightColumns.append(1)

    if len(rightColumns) == 0:
        if includeMayhew:
            rightColumns.append(1)
        if includeZerothEdition:
            rightColumns.append(1)

    leftColumns = []
    if includeFirstEdition or includeSecondEdition:
        if includeMayhew:
            leftColumns.append(1)
        if includeZerothEdition:
            leftColumns.append(1)
    if includeKJV:
        leftColumns.append(1)

    rightColumnMeasure = ""
    if len(rightColumns) < 2:
        rightColumnMeasure = "42%"
    else:
        rightColumnMeasure = "21%"

    leftColumnMeasure = ""
    if len(leftColumns) < 2:
        leftColumnMeasure = "42%"
    elif len(leftColumns) == 2:
        leftColumnMeasure = "21%"
    else:
        leftColumnMeasure = "14%"


    return render_template('searchmass.html', verseIndices = matchingIndices, verseDictionary = verseIndexDictionary, KJVIncluded = includeKJV, firstEditionIncluded = includeFirstEdition, secondEditionIncluded = includeSecondEdition, mayhewIncluded = includeMayhew, zerothEditionIncluded = includeZerothEdition, printKJVLines = matchingKJV, printFirstEditionLines = matchingFirstEdition, printSecondEditionLines = matchingSecondEdition, printMayhewLines = matchingMayhew, printZerothEditionLines = matchingZerothEdition, firstEditionCount = totalFirstEdition, secondEditionCount = totalSecondEdition, mayhewCount = totalMayhew, zerothEditionCount = totalZerothEdition, matchingVerses = matchingVerses, totalAll = totalAll, totalVerseCount = totalVerseCount, numRightColumns = rightColumns, numLeftColumns = leftColumns, rightColumnMeasure = rightColumnMeasure, leftColumnMeasure = leftColumnMeasure)

@app.route('/proofreader', methods=['GET', 'POST'])
def proofreader():
    if request.method == 'POST':
        return render_template(url_for('proofreader.html'))
    
    allBooks = allBookList
    
    return render_template('proofreader.html', allBooks = allBooks)

@app.route("/doproofreading", methods=['GET', 'POST'])
def doproofreading():
    selectBook = request.form['bookSelectionDropdown']
    selectChapter = request.form['chapterSelectionDropdown']
    defaultBook =""
    defaultChapter = ""

    selectedBook = request.form.get('bookSelectionDropdown')
    selectedChapter = request.form.get('chapterSelectionDropdown')
    defaultBook = selectedBook
    defaultChapter = selectedChapter

    firstEditionSelected = request.form.get('include_first_edition') == 'on'
    secondEditionSelected = request.form.get('include_second_edition') == 'on'
    mayhewSelected = request.form.get('include_mayhew') == 'on'
    zerothEditionSelected = request.form.get('include_zeroth_edition') == 'on'
    showKJV = request.form.get('include_KJV') == 'on'

    hasMayhew = selectedBook == "Psalms (prose)" or selectedBook == "John"
    hasZerothEdition = selectedBook == "Genesis"

    useKJV = showKJV
    useFirstEdition = firstEditionSelected
    useSecondEdition = secondEditionSelected
    useMayhew = False #hasMayhew and mayhewSelected
    useZerothEdition = False #hasZerothEdition and zerothEditionSelected

    fileNamesList = []
    fileLinesList = []

    verseList = []
    firstEditionVerseDict = {}
    secondEditionVerseDict = {}
    mayhewVerseDict = {}
    zerothEditionVerseDict = {}
    KJVVerseDict = {}

    dictList = []

    if useFirstEdition:
        firstEditionPath = './texts/' + selectedBook + '.First Edition.txt'
        if os.path.exists(firstEditionPath):
            useFirstEdition = True
            firstEditionLines = open(firstEditionPath, 'r', encoding="utf-8").readlines()
            fileLinesList.append(firstEditionLines)
            fileNamesList.append("First Edition")
            dictList.append(firstEditionVerseDict)
        else:
            useFirstEdition = False

    if useSecondEdition:
        secondEditionPath = './texts/' + selectedBook + '.Second Edition.txt'
        if os.path.exists(secondEditionPath):
            useSecondEdition = True
            secondEditionLines = open(secondEditionPath, 'r', encoding="utf-8").readlines()
            fileLinesList.append(secondEditionLines)
            fileNamesList.append("Second Edition")
            dictList.append(secondEditionVerseDict)

        else:
            useSecondEdition = False

    if useMayhew:
        mayhewPath = './texts/' + selectedBook + '.Mayhew.txt'
        if os.path.exists(mayhewPath):
            useMayhew = True
            mayhewLines = open(mayhewPath, 'r', encoding="utf-8").readlines()
            fileLinesList.append(mayhewLines)
            fileNamesList.append("Mayhew")
            dictList.append(mayhewVerseDict)
        else:
            useMayhew = False

    if useZerothEdition:
        zerothEditionPath = './texts/' + selectedBook + '.Zeroth Edition.txt'
        if os.path.exists(zerothEditionPath):
            useZerothEdition = True
            zerothEditionLines = open(zerothEditionPath, 'r', encoding="utf-8").readlines()
            fileLinesList.append(zerothEditionLines)
            fileNamesList.append("Zeroth Edition")
            dictList.append(zerothEditionVerseDict)
        else:
            useZerothEdition = False

    if useKJV:
        KJVPath = './texts/' + selectedBook + '.KJV.txt'
        if os.path.exists(KJVPath):
            useKJV = True
            KJVLines = open(KJVPath, 'r', encoding="utf-8").readlines()
            fileLinesList.append(KJVLines)
            fileNamesList.append("KJV")
            dictList.append(KJVVerseDict)
        else:
            useKJV = False

    
    for line in fileLinesList[0]:
        chapterVerse = line.split(" ")[0].strip()
        if chapterVerse == "Epilogue":
            verseList.append("Epilogue")
        else:
            try:
                chapter = chapterVerse.split(".")[0]
                verse = chapterVerse.split(".")[1]
                if str(chapter) == str(selectedChapter):
                    verseList.append(verse)
            except:
                continue
                #print("Error in line: " + line)

    for verse in verseList:
        firstEditionVerseDict[verse] = ""
        secondEditionVerseDict[verse] = ""
        firstEditionLine = ""
        secondEditionLine = ""
        for line in fileLinesList[0]:
            chapterVerse = line.split(" ")[0].strip()
            verseText = " ".join(line.split(" ")[1:]).strip()
            print(verseText)
            if chapterVerse == selectedChapter + "." + verse:
                firstEditionLine = verseText
                break

        for line in fileLinesList[1]:
            chapterVerse = line.split(" ")[0].strip()
            verseText = " ".join(line.split(" ")[1:])
            if chapterVerse == selectedChapter + "." + verse:
                secondEditionLine = verseText
                break

        for line in fileLinesList[-1]:
            print(line)
            chapterVerse = line.split(" ")[0].strip()
            verseText = " ".join(line.split(" ")[1:])
            if chapterVerse == selectedChapter + "." + verse:
                KJVVerseDict[verse] = verseText
                break

        comparedLines = compareWords(firstEditionLine, secondEditionLine)
        firstEditionVerseDict[verse] = Markup(comparedLines[0].replace('8', 'ꝏ̄'))
        secondEditionVerseDict[verse] = Markup(comparedLines[1].replace('8', 'ꝏ̄'))

    useVerseNumber = useFirstEdition or useSecondEdition or useMayhew or useKJV or useZerothEdition

        
    
    
    return render_template('proofreader.html', selectedBook = selectedBook, selectedChapter = selectedChapter, hasMayhew = hasMayhew, hasZerothEdition = hasZerothEdition, defaultBook = defaultBook, defaultChapter = defaultChapter, useVerseNumber = useVerseNumber, useKJV = useKJV, useFirstEdition = useFirstEdition, useSecondEdition = useSecondEdition, useMayhew = useMayhew, useZerothEdition = useZerothEdition, verseList = verseList, fileNamesList = fileNamesList, firstEditionVerseDict = firstEditionVerseDict, secondEditionVerseDict = secondEditionVerseDict, mayhewVerseDict = mayhewVerseDict, zerothEditionVerseDict = zerothEditionVerseDict, KJVVerseDict = KJVVerseDict)
