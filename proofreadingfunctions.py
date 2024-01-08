import difflib
import re

# Various functions to help with proofreading by highlighting differences.

def killHTMLTags(word):
    word = word.replace('<span style="color: red"><b>', '')
    word = word.replace('</b></span>', '')

    return word

def boldyRed(word):
    return '<span style="color: red"><b>' + word + '</b></span>'

allPunctuationMarks =[".", "?", "," ":", ";", "!"]

def compareWordsSameLength(word1, word2, ignoreCasing):
    word1Copy = word1
    word2Copy = word2

    finalWord1 = ""
    finalWord2 = ""

    if ignoreCasing:
        compare = difflib.SequenceMatcher(None, word1Copy.lower(), word2Copy.lower(), autojunk=False).get_matching_blocks()[0:-1]

    else:
        compare = difflib.SequenceMatcher(None, word1Copy, word2Copy, autojunk=False).get_matching_blocks()[0:-1]
    
    for i in range(len(word1Copy)):
        charInTuple = False
        for tuple in compare:
            if i >= tuple[0] and i < tuple[0] + tuple[2]:
                charInTuple = True
        if charInTuple == True:
            finalWord1 += word1Copy[i]
        else:
            finalWord1 += '<span style="color: red"><b>' + word1Copy[i] + '</b></span>'

    for i in range(len(word2Copy)):
        charInTuple = False
        for tuple in compare:
            if i >= tuple[1] and i < tuple[1] + tuple[2]:
                charInTuple = True
        if charInTuple == True:
            finalWord2 += word2Copy[i]
        else:
            finalWord2 += '<span style="color: red"><b>' + word2Copy[i] + '</b></span>'

    return [finalWord1, finalWord2]

def compareWordsDifferentLength(word1, word2, ignoreCasing):
    longerWord = max(word1, word2, key=len)
    shorterWord = min(word1, word2, key=len)

    firstWordIsLonger = (longerWord == word1)

    finalLongerChars = []
    finalShorterChars = []
        
    if ignoreCasing:
        compare = difflib.SequenceMatcher(None, longerWord.lower(), shorterWord.lower(), autojunk=False).get_matching_blocks()[0:-1]
        
    else:
        compare = difflib.SequenceMatcher(None, longerWord, shorterWord, autojunk=False).get_matching_blocks()[0:-1]

    for i in range(len(longerWord)):
        charInTuple = False
        for tuple in compare:
            if i >= tuple[0] and i < tuple[0] + tuple[2]:
                charInTuple = True

        if charInTuple == True:
            finalLongerChars.append(longerWord[i])
        
        else:
            finalLongerChars.append('<span style="color: red"><b>' + longerWord[i] + '</b></span>')  

    for i in range(len(shorterWord)):
        charInTuple = False
        for tuple in compare:
            if i >= tuple[1] and i < tuple[1] + tuple[2]:
                charInTuple = True

        if charInTuple == True:
            finalShorterChars.append(shorterWord[i])
        
        else:
            finalShorterChars.append('<span style="color: red"><b>' + shorterWord[i] + '</b></span>')  
            
    finalLongerWord = re.sub('</u></b></span><span style="color: red"><b>', '', "".join(finalLongerChars))
    finalShorterWord = re.sub('</u></b></span><span style="color: red"><b>', '', "".join(finalShorterChars))

    if firstWordIsLonger:
        return [finalLongerWord, finalShorterWord]
    else:
        return [finalShorterWord, finalLongerWord]

def compareWords(word1, word2, ignoreCasing, markSpaces = True):

    newWord1 = word1.strip().replace(" ", "·")
    newWord2 = word2.strip().replace(" ", "·")

    if len(newWord1) == len(newWord2):
        finalWords = compareWordsSameLength(newWord1, newWord2, ignoreCasing)
    else:
        finalWords = compareWordsDifferentLength(newWord1, newWord2, ignoreCasing)

    newWord1 = finalWords[0]
    newWord2 = finalWords[1]

    finalList = []
    for newWord in [newWord1, newWord2]:
        newWord = newWord.replace('</b></span><span style="color: red"><b>', '')
        newWord = newWord.replace('<span style="color: red"><b>·</b></span>', '<span style="color: red"><b>˙</b></span>')
        newWord = newWord.replace('<span style="color: red"><b>$</b></span>', '<span style="color: red"><b>˙</b></span>')

        newWord = newWord.replace('·', ' ')
        newWord = newWord.replace('$', ' ')


        if markSpaces == False:
            newWord = newWord.replace('˙', ' ')
        
        finalList.append(newWord)

    return finalList
