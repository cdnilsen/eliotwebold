from markupsafe import Markup

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

def cleanLineOfDiacritics(line):
    diacritics = ["á", "é", "í", "ó", "ú", "à", "è", "ì", "ò", "ù", "â", "ê", "î", "ô", "û", "ä", "ë", "ï", "ö", "ü", "ã", "õ", "ñ", "m̃", "ũ", "ẽ", "ĩ", "ā", "ē", "ī", "ō", "ū"]
    for diacritic in diacritics:
        line = line.replace(diacritic, charReplacementDict[diacritic])
    return line

def displayLine(line, strictDiacritics, allVersesList, word, editionLineDict, versePrintDict):
    
    howManyTokens = 0

    lineHasWord = False
    verseNum = line.split(" ")[0].strip()
    verseText = " ".join(line.split(" ")[1:])

    verseCheck = ""
    if strictDiacritics:
        verseCheck = verseText
    else:
        verseCheck = cleanLineOfDiacritics(verseText)

    if verseNum in allVersesList:
        if word in verseCheck:
            howManyTokens = verseCheck.count(word)
            newVerseText = ""
            if strictDiacritics:
                newVerseText = verseText.replace(word, "<span style='color:red'><b>" + word + "</b></span>")

            else:
                i = len(word)
                for j in range(len(verseText)):
                    if cleanLineOfDiacritics(verseText[j:j+i]) == word:
                        newVerseText += "<span style='color:red'><b>" + verseText[j:j+i] + "</b></span>"
                        j += i
                    else:
                        newVerseText += verseText[j]

            newVerseText = Markup(newVerseText.replace('8', 'ꝏ̄'))
            editionLineDict[verseNum] = newVerseText
            

            lineHasWord = True
            versePrintDict[verseNum] = True
        else:
            editionLineDict[verseNum] = ""
    
    finalDict = {
        "lineHasWord": lineHasWord,
        "numTokens": howManyTokens,
    }
    
    return finalDict