import difflib

def killHTMLTags(word):
    word = word.replace('<span style="color: red"><b>', '')
    word = word.replace('</b></span>', '')

    return word

def boldyRed(word):
    return '<span style="color: red"><b>' + word + '</b></span>'

def getLargestMatchingSubstring(word1, word2, isLastBlock = False):

    word1Copy = word1
    word2Copy = word2

    keepGoing = True
    while keepGoing:
        
        mySequenceMatcher = difflib.SequenceMatcher(None, word1Copy, word2Copy, autojunk=False)
        
        longestMatch = mySequenceMatcher.find_longest_match(0, len(word1Copy), 0, len(word2Copy))
        
        originalMatchString = word1Copy[longestMatch.a:longestMatch.a + longestMatch.size]

        if len(originalMatchString) < 3 and isLastBlock == False:
            keepGoing = False
            break

        word1Match = "«"

        word2Match = "«"

        for char in word1Copy[longestMatch.a:longestMatch.a + longestMatch.size]:
            word1Match += char + "ϣ"

        word1Match = word1Match[:-1] + "»"
       
        for char in word2Copy[longestMatch.b:longestMatch.b + longestMatch.size]:
            word2Match += char + "ϫ"

        word2Match = word2Match[:-1] + "»"

        word1Copy = word1Copy.replace(originalMatchString, word1Match)
        word2Copy = word2Copy.replace(originalMatchString, word2Match)
        
        if len(originalMatchString) == 1 and isLastBlock == True:
            keepGoing = False
            break

    word1Copy = boldyRed(word1Copy)
    word2Copy = boldyRed(word2Copy)

    word1Copy = word1Copy.replace("«", '</b></span>')
    word1Copy = word1Copy.replace("»", '<span style="color: red"><b>')
    word1Copy = word1Copy.replace('<span style="color: red"><b></b></span>', "")
    word1Copy = word1Copy.replace("ϣ", "")

    word2Copy = word2Copy.replace("«", '</b></span>')
    word2Copy = word2Copy.replace("»", '<span style="color: red"><b>')
    word2Copy = word2Copy.replace('<span style="color: red"><b></b></span>', "")
    word2Copy = word2Copy.replace("ϫ", "")

    if isLastBlock:
        return [word1Copy, word2Copy]

    word1LastBlockSplit = word1Copy.replace('<span style="color: red">', 'ϫ<span style="color: red">').split("ϫ")
    word2LastBlockSplit = word2Copy.replace('<span style="color: red">', 'ϣ<span style="color: red">').split("ϣ")

    if word1LastBlockSplit[0] == "":
        word1LastBlockSplit = word1LastBlockSplit[1:]
    if word2LastBlockSplit[0] == "":
        word2LastBlockSplit = word2LastBlockSplit[1:]

    if word1LastBlockSplit[0][0] == "<" and killHTMLTags(word1LastBlockSplit[0]) != killHTMLTags(word2LastBlockSplit[0]):
        firstBlocks1 = word1LastBlockSplit[0].split("</b></span>")
        firstBlocks2 = word2LastBlockSplit[0].split("</b></span>")

        word1LastBlockSplit = [firstBlocks1[1]] + word1LastBlockSplit[1:]
        word2LastBlockSplit = [firstBlocks2[1]] + word2LastBlockSplit[1:]

        newFirstBlocks = getLargestMatchingSubstring("ϫ" + killHTMLTags(firstBlocks1[0]) + "ϫ", "ϫ" + killHTMLTags(firstBlocks2[0]) + "ϫ", False)

        def initialBlockCleaner(block):
            block += '</b></span>'
            
            block = block.replace('<span style="color: red"><b></b></span>', '</b></span>')
            
            if '<span style="color: red"><b>' not in block:
                block = block.replace("</b></span>", "")
            return(block)

        newFirstBlock1 = initialBlockCleaner(newFirstBlocks[0])
        newFirstBlock2 = initialBlockCleaner(newFirstBlocks[1])

        
        word1LastBlockSplit = [newFirstBlock1] + [firstBlocks1[1]] + word1LastBlockSplit
        word2LastBlockSplit = [newFirstBlock2] + [firstBlocks2[1]] + word2LastBlockSplit

    word1Copy = "".join(word1LastBlockSplit[0:-1])
    word2Copy = "".join(word2LastBlockSplit[0:-1])
    
    word1LastBlock = killHTMLTags(word1LastBlockSplit[-1])
    word2LastBlock = killHTMLTags(word2LastBlockSplit[-1])

    lastBlockMatch = getLargestMatchingSubstring(word1LastBlock, word2LastBlock, True)
    word1Copy = word1Copy + lastBlockMatch[0]
    word2Copy = word2Copy + lastBlockMatch[1]

    return [word1Copy, word2Copy]

def doVerseComparison(word1, word2, markSpaces=True):
    newWord1 = word1.strip().replace(" ", "·")
    newWord2 = word2.strip().replace(" ", "·")

    finalWords = getLargestMatchingSubstring(newWord1, newWord2)

    newWord1 = finalWords[0]
    newWord2 = finalWords[1]

    newWord1 = newWord1.replace('<span style="color: red"><b>·</b></span>', '<span style="color: red"><b>˙</b></span>')
    newWord2 = newWord2.replace('<span style="color: red"><b>·</b></span>', '<span style="color: red"><b>˙</b></span>')
    newWord1 = newWord1.replace('·', ' ')
    newWord2 = newWord2.replace('·', ' ')
    newWord1 = newWord1.replace('$', '˙')
    newWord2 = newWord2.replace('$', '˙')

    if markSpaces == False:
        newWord1 = newWord1.replace('˙', ' ')
        newWord2 = newWord2.replace('˙', ' ')

    return [newWord1, newWord2]
