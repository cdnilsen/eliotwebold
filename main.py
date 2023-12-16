from flask import Flask, flash, request, jsonify, render_template, redirect, url_for, Blueprint, abort
from markupsafe import Markup
import os
from werkzeug.utils import secure_filename
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape

from textdisplayfunctions import charReplacementDict, cleanLineOfDiacritics, displayLine



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

    
