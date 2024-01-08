from markupsafe import Markup
import re

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

def replace_keep_case(match, replacement, text):
    def func(match):
        g = match.group()
        if g.islower():
            return replacement.lower()
        if g.istitle():
            return replacement.title()
        if g.isupper():
            return replacement.upper()
        return replacement
    return re.sub(re.escape(match), func, text, flags=re.I)

def displayLine(line, strictDiacritics, allVersesList, targetString, versePrintDict, editionLineDict, condition="contains"):
    finalDict = {
        "lineHasWord": False,
        "numTokens": 0,
        "verseText": ""
    }
    
    howManyTokens = 0
    lineHasWord = False
    verseNum = line.split(" ")[0].strip()

    if verseNum not in allVersesList:
        editionLineDict[verseNum] = ""
        return finalDict
    
    else:
        verseText = line.split(" ")[1:]

        verseCheck = ""
        if strictDiacritics:
            verseCheck = verseText
        else:
            newVerseText = []
            for word in verseText:
                newVerseText.append(cleanLineOfDiacritics(word))
            verseCheck = newVerseText


        if condition == "contains":
            verseCheck = " ".join(verseText)
            if strictDiacritics:
                if targetString.lower() in verseCheck.lower():
                    lineHasWord = True
                    howManyTokens = verseCheck.lower().count(targetString.lower())
                    verseCheck = replace_keep_case(targetString, "<span style='color:red'><b>" + targetString + "</b></span>", verseCheck)
                
            else:
                if cleanLineOfDiacritics(targetString).lower() in cleanLineOfDiacritics(verseCheck).lower():
                    lineHasWord = True
                    howManyTokens = cleanLineOfDiacritics(verseCheck).lower().count(cleanLineOfDiacritics(targetString).lower())

                    for i in range(len(verseCheck)):
                        if cleanLineOfDiacritics(verseCheck[i:i+len(targetString)]).lower() == cleanLineOfDiacritics(targetString).lower():
                            verseCheck = verseCheck[:i] + "<span style='color:red'><b>" + verseCheck[i:i+len(targetString)] + "</b></span>" + verseCheck[i+len(targetString):]

        elif condition == "exact":
            newVerseCheck = []
            if strictDiacritics:
                for word in verseCheck:       
                    if word.lower() == stripIrrelevantChars(targetString.lower()):
                        lineHasWord = True
                        howManyTokens += 1
                        word = replace_keep_case(targetString, "<span style='color:red'><b>" + targetString + "</b></span>", word)
                    newVerseCheck.append(word)
            else:
                for word in verseCheck:
                    if cleanLineOfDiacritics(word).lower() == stripIrrelevantChars(cleanLineOfDiacritics(targetString).lower()):
                        lineHasWord = True
                        howManyTokens += 1
                        for i in range(len(word)):
                            if cleanLineOfDiacritics(word[i:i+len(targetString)]).lower() == cleanLineOfDiacritics(targetString).lower():
                                word = word[:i] + "<span style='color:red'><b>" + word[i:i+len(targetString)] + "</b></span>" + word[i+len(targetString):]
                    newVerseCheck.append(word)
            verseCheck = " ".join(newVerseCheck)

        elif condition == "starts":
            newVerseCheck = []
            if strictDiacritics:
                for word in verseCheck:
                    if word.lower().startswith(targetString.lower()):
                        lineHasWord = True
                        howManyTokens += 1
                        word = "<span style='color:red'><b>" + targetString + "</b></span>" + word[len(targetString):]
                    newVerseCheck.append(word)
            else:
                for word in verseCheck:
                    if cleanLineOfDiacritics(word[0:len(targetString)]).lower() == cleanLineOfDiacritics(targetString).lower():
                        lineHasWord = True
                        howManyTokens += 1
                        word = "<span style='color:red'><b>" + word[0:len(targetString)] + "</b></span>" + word[len(targetString):]

                    newVerseCheck.append(word)

            verseCheck = " ".join(newVerseCheck)

        elif condition == "ends":
            newVerseCheck = []
            if strictDiacritics:
                for word in verseCheck:
                    if word.lower().endswith(targetString.lower()):
                        lineHasWord = True
                        howManyTokens += 1
                        word = word[:-len(targetString)] + "<span style='color:red'><b>" + targetString + "</b></span>"
                    newVerseCheck.append(word)
            else:
                for word in verseCheck:
                    if cleanLineOfDiacritics(word[-len(targetString):]).lower() == cleanLineOfDiacritics(targetString).lower():
                        lineHasWord = True
                        howManyTokens += 1
                        word = word[:-len(targetString)] + "<span style='color:red'><b>" + word[-len(targetString):] + "</b></span>"
                    newVerseCheck.append(word)

            verseCheck = " ".join(newVerseCheck)

        verseText = Markup(verseCheck.replace("8", "ꝏ̄").replace("$", " "))

        if lineHasWord:
            editionLineDict[verseNum] = True
            versePrintDict[verseNum] = verseText
        else:
            editionLineDict[verseNum] = False or editionLineDict[verseNum]
            versePrintDict[verseNum] = verseText

        finalDict = {
            "lineHasWord": lineHasWord,
            "numTokens": howManyTokens,
            "verseText": verseText
        }

        return finalDict