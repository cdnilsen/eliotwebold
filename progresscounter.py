import datetime
bookAllVerseCount = { 
    "Genesis": 1533,
    "Exodus": 1213,
    "Leviticus": 859,
    "Numbers": 1288,
    "Deuteronomy": 959,
    "Joshua": 658,
    "Judges": 618,
    "Ruth": 85,
    "1 Samuel": 810,
    "2 Samuel": 695,
    "1 Kings": 816,
    "2 Kings": 719,
    "1 Chronicles": 942,
    "2 Chronicles": 822,
    "Ezra": 280,
    "Nehemiah": 406,
    "Esther": 167,
    "Job": 1070,
    "Psalms": 2461,
    "Metrical Psalms": 2461,
    "Proverbs": 915,
    "Ecclesiastes": 222,
    "Song of Songs": 117,
    "Isaiah": 1292,
    "Jeremiah": 1364,
    "Lamentations": 154,
    "Ezekiel": 1273,
    "Daniel": 357,
    "Hosea": 197,
    "Joel": 73,
    "Amos": 146,
    "Obadiah": 21,
    "Jonah": 48,
    "Micah": 105,
    "Nahum": 47,
    "Habakkuk": 56,
    "Zephaniah": 53,
    "Haggai": 38,
    "Zechariah": 211,
    "Malachi": 55,
    "Matthew": 1071,
    "Mark": 678,
    "Luke": 1151,
    "John": 879,
    "Acts": 1007,
    "Romans": 433,
    "1 Corinthians": 437,
    "2 Corinthians": 257,
    "Galatians": 149,
    "Ephesians": 155,
    "Philippians": 104,
    "Colossians": 95,
    "1 Thessalonians": 89,
    "2 Thessalonians": 47,
    "1 Timothy": 113,
    "2 Timothy": 83,
    "Titus": 46,
    "Philemon": 25,
    "Hebrews": 303,
    "James": 108,
    "1 Peter": 105,
    "2 Peter": 61,
    "1 John": 105,
    "2 John": 13,
    "3 John": 14,
    "Jude": 25,
    "Revelation": 404
}


firstEditionCopyDict = {
    "Genesis": False,
    "Exodus": True,
    "Leviticus": False,
    "Numbers": False,
    "Deuteronomy": False,
    "Joshua": False,
    "Judges": False,
    "Ruth": True,
    "1 Samuel": False,
    "2 Samuel": False,
    "1 Kings": False,
    "2 Kings": False,
    "1 Chronicles": False,
    "2 Chronicles": False,
    "Ezra": False,
    "Nehemiah": False,
    "Esther": False,
    "Job": True,
    "Psalms": True,
    "Metrical Psalms": False,
    "Proverbs": True,
    "Ecclesiastes": True,
    "Song of Songs": True,
    "Isaiah": False,
    "Jeremiah": False,
    "Lamentations": True,
    "Ezekiel": False,
    "Daniel": False,
    "Hosea": False,
    "Joel": False,
    "Amos": False,
    "Obadiah": True,
    "Jonah": True,
    "Micah": False,
    "Nahum": True,
    "Habakkuk": False,
    "Zephaniah": False,
    "Haggai": True,
    "Zechariah": False,
    "Malachi": False,
    "Matthew": True,
    "Mark": True,
    "Luke": True,
    "John": True,
    "Acts": True,
    "Romans": True,
    "1 Corinthians": True,
    "2 Corinthians": True,
    "Galatians": True,
    "Ephesians": True,
    "Philippians": True,
    "Colossians": True,
    "1 Thessalonians": True,
    "2 Thessalonians": True,
    "1 Timothy": True,
    "2 Timothy": True,
    "Titus": True,
    "Philemon": True,
    "Hebrews": True,
    "James": True,
    "1 Peter": True,
    "2 Peter": True,
    "1 John": True,
    "2 John": True,
    "3 John": True,
    "Jude": True,
    "Revelation": True
}

secondEditionCopyDict = {
    "Genesis": True,
    "Exodus": True,
    "Leviticus": True,
    "Numbers": True,
    "Deuteronomy": True,
    "Joshua": True,
    "Judges": False,
    "Ruth": True,
    "1 Samuel": False,
    "2 Samuel": False,
    "1 Kings": False,
    "2 Kings": True,
    "1 Chronicles": False,
    "2 Chronicles": False,
    "Ezra": False,
    "Nehemiah": False,
    "Esther": False,
    "Job": False,
    "Psalms": False,
    "Metrical Psalms": False,
    "Proverbs": False,
    "Ecclesiastes": False,
    "Song of Songs": True,
    "Isaiah": False,
    "Jeremiah": False,
    "Lamentations": True,
    "Ezekiel": False,
    "Daniel": False,
    "Hosea": False,
    "Joel": False,
    "Amos": False,
    "Obadiah": True,
    "Jonah": True,
    "Micah": False,
    "Nahum": False,
    "Habakkuk": False,
    "Zephaniah": False,
    "Haggai": True,
    "Zechariah": False,
    "Malachi": False,
    "Matthew": True,
    "Mark": True,
    "Luke": True,
    "John": True,
    "Acts": True,
    "Romans": True,
    "1 Corinthians": True,
    "2 Corinthians": True,
    "Galatians": True,
    "Ephesians": True,
    "Philippians": True,
    "Colossians": True,
    "1 Thessalonians": True,
    "2 Thessalonians": True,
    "1 Timothy": True,
    "2 Timothy": True,
    "Titus": True,
    "Philemon": True,
    "Hebrews": True,
    "James": True,
    "1 Peter": True,
    "2 Peter": True,
    "1 John": True,
    "2 John": True,
    "3 John": True,
    "Jude": True,
    "Revelation": True
}


allNTBookList = [
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

allOTBookList = [
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
    "Psalms",
    "Metrical Psalms",
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
    "Malachi"
]

partialVerseCountListFirstEd = { 
    "Genesis": 0,
    "Exodus": 1072,
    "Leviticus": 108,
    "Numbers": 0,
    "Deuteronomy": 33,
    "Joshua": 0,
    "Judges": 0,
    "Ruth": 0,
    "1 Samuel": 0,
    "2 Samuel": 0,
    "1 Kings": 0,
    "2 Kings": 0,
    "1 Chronicles": 0,
    "2 Chronicles": 0,
    "Ezra": 1,
    "Nehemiah": 0,
    "Esther": 0,
    "Job": 0,
    "Psalms": 0,
    "Metrical Psalms": 0,
    "Proverbs": 0,
    "Ecclesiastes": 0,
    "Song of Songs": 0,
    "Isaiah": 0,
    "Jeremiah": 0,
    "Lamentations": 0,
    "Ezekiel": 0,
    "Daniel": 0,
    "Hosea": 0,
    "Joel": 0,
    "Amos": 0,
    "Obadiah": 0,
    "Jonah": 0,
    "Micah": 0,
    "Nahum": 0,
    "Habakkuk": 0,
    "Zephaniah": 0,
    "Haggai": 0,
    "Zechariah": 0,
    "Malachi": 0,
    "Matthew": 0,
    "Mark": 0,
    "Luke": 0,
    "John": 0,
    "Acts": 0,
    "Romans": 0,
    "1 Corinthians": 0,
    "2 Corinthians": 0,
    "Galatians": 0,
    "Ephesians": 0,
    "Philippians": 33,
    "Colossians": 29,
    "1 Thessalonians": 10,
    "2 Thessalonians": 0,
    "1 Timothy": 20,
    "2 Timothy": 21,
    "Titus": 16,
    "Philemon": 0,
    "Hebrews": 233,
    "James": 16,
    "1 Peter": 19,
    "2 Peter": 41,
    "1 John": 5,
    "2 John": 0,
    "3 John": 0,
    "Jude": 0,
    "Revelation": 304
}

partialVerseCountListSecondEd = { 
    "Genesis": 0,
    "Exodus": 0,
    "Leviticus": 0,
    "Numbers": 0,
    "Deuteronomy": 0,
    "Joshua": 0,
    "Judges": 0,
    "Ruth": 0,
    "1 Samuel": 0,
    "2 Samuel": 0,
    "1 Kings": 0,
    "2 Kings": 0,
    "1 Chronicles": 0,
    "2 Chronicles": 0,
    "Ezra": 0,
    "Nehemiah": 0,
    "Esther": 0,
    "Job": 0,
    "Psalms": 0,
    "Metrical Psalms": 0,
    "Proverbs": 0,
    "Ecclesiastes": 0,
    "Song of Songs": 0,
    "Isaiah": 0,
    "Jeremiah": 0,
    "Lamentations": 0,
    "Ezekiel": 0,
    "Daniel": 0,
    "Hosea": 0,
    "Joel": 0,
    "Amos": 0,
    "Obadiah": 0,
    "Jonah": 0,
    "Micah": 0,
    "Nahum": 0,
    "Habakkuk": 0,
    "Zephaniah": 0,
    "Haggai": 0,
    "Zechariah": 0,
    "Malachi": 0,
    "Matthew": 0,
    "Mark": 0,
    "Luke": 0,
    "John": 0,
    "Acts": 0,
    "Romans": 0,
    "1 Corinthians": 0,
    "2 Corinthians": 0,
    "Galatians": 0,
    "Ephesians": 0,
    "Philippians": 0,
    "Colossians": 0,
    "1 Thessalonians": 0,
    "2 Thessalonians": 0,
    "1 Timothy": 0,
    "2 Timothy": 0,
    "Titus": 0,
    "Philemon": 0,
    "Hebrews": 0,
    "James": 0,
    "1 Peter": 0,
    "2 Peter": 0,
    "1 John": 0,
    "2 John": 0,
    "3 John": 0,
    "Jude": 0,
    "Revelation": 0
}

allVersesOT = 0
versesToGoCounterOT = 0

allVersesNT = 0
versesToGoCounterNT = 0


for book in allOTBookList:
    allVersesOT += bookAllVerseCount[book]
    if firstEditionCopyDict[book] == False:
        versesToGoCounterOT += (bookAllVerseCount[book] - partialVerseCountListFirstEd[book])

for book in allNTBookList:
    allVersesNT += bookAllVerseCount[book]
    if firstEditionCopyDict[book] == False:
        versesToGoCounterNT += (bookAllVerseCount[book] - partialVerseCountListFirstEd[book])

secondEditionOTCounter = 0
for book in allOTBookList:
    if secondEditionCopyDict[book] == False:
        secondEditionOTCounter += (bookAllVerseCount[book] - partialVerseCountListSecondEd[book])

print(" ")
print(str(versesToGoCounterOT + versesToGoCounterNT) + "/" + str(allVersesOT + allVersesNT) + " verses to go in the first edition (" + str(round((versesToGoCounterOT + versesToGoCounterNT) / (allVersesOT + allVersesNT) * 100, 2)) + "%)")

print(" ")
print(str(secondEditionOTCounter) + "/" + str(allVersesOT + 7957) + " verses to go in the second edition (" + str(round((secondEditionOTCounter) / (allVersesOT + 7957) * 100, 2)) + "%)")
print(" ")


open("CopyProgress.txt", "a", encoding="utf-8").write("[" + str(datetime.datetime.now()) + "]\n"  + "\tFirst edition: " + str(versesToGoCounterOT + versesToGoCounterNT) + "/" + str(allVersesOT + allVersesNT) + " (" + str(round((versesToGoCounterOT + versesToGoCounterNT) / (allVersesOT + allVersesNT) * 100, 2)) + "%)\n\t" + "Second edition: " + str(secondEditionOTCounter) + "/" + str(allVersesOT + 7957) + " (" + str(round((secondEditionOTCounter) / (allVersesOT + 7957) * 100, 2)) + "%)\n\n")