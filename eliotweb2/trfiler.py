def fileGreekLines(book):
    prefixToFileDict = {
        'Mat': 'Matthew',
        'Mark': 'Mark',
        'Luke': 'Luke',
        'John': 'John',
        'Acts': 'Acts',
        'Rom': 'Romans',
        '1Cor': '1 Corinthians',
        '2Cor': '2 Corinthians',
        'Gal': 'Galatians',
        'Eph': 'Ephesians',
        'Philippians': 'Philippians',
        'Col': 'Colossians',
        '1Thes': '1 Thessalonians',
        '2Thes': '2 Thessalonians',
        '1Tim': '1 Timothy',
        '2Tim': '2 Timothy',
        'Titus': 'Titus',
        'Philemon': 'Philemon',
        'Heb': 'Hebrews',
        'James': 'James',
        '1Pet': '1 Peter',
        '2Pet': '2 Peter',
        '1John': '1 John',
        '2John': '2 John',
        '3John': '3 John',
        'Jude': 'Jude',
        'Rev': 'Revelation'
    }

    textusReceptusLines = open('./Textus Receptus Parsed.txt', 'r', encoding='utf-8').readlines()

    allVerseDict = {}
    for line in textusReceptusLines[3:]:
        lineAddress = line.split(' ')[0]
        if prefixToFileDict[lineAddress.split('.')[0]] == book:
            verseAddress = lineAddress.split('.')[1] + '.' + lineAddress.split('.')[2]
            lineText = ' '.join(line.split(' ')[1:])
            allVerseDict[verseAddress] = lineText.strip()
    
    return(allVerseDict)


