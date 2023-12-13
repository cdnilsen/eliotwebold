from flask import Flask, flash, request, jsonify, render_template, redirect, url_for, Blueprint, abort
from markupsafe import Markup
import os
from werkzeug.utils import secure_filename
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape

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


        #random change
        
        verseIndexDictionary[index]['FirstEdition'] = matchingFirstEdition[index]

        verseIndexDictionary[index]['SecondEdition'] = matchingSecondEdition[index]

        verseIndexDictionary[index]['Mayhew'] = matchingMayhew[index]

        verseIndexDictionary[index]['ZerothEdition'] = matchingZerothEdition[index]
    
    includeMayhew = includeMayhew and (anyWordsInJohn or anyWordsInPsalms)
    includeZerothEdition = includeZerothEdition and (anyWordsInGenesis)

    return render_template('searchenglish.html', verseIndices = matchingIndices, verseDictionary = verseIndexDictionary, KJVIncluded = includeKJV, firstEditionIncluded = includeFirstEdition, secondEditionIncluded = includeSecondEdition, mayhewIncluded = includeMayhew, zerothEditionIncluded = includeZerothEdition)



    
