from wordfrequencymodule import populateHapaxes

showChars = input("Show all characters in hapaxes? (y/n) ")

populateHapaxes()

if showChars == "y":

    allHapaxes = open("hapaxLegomenaStrict.txt", "r", encoding="utf-8").readlines()

    allChars = []
    allCharCountDict = {}
    for line in allHapaxes:
        for char in line.strip():
            if char not in allChars:
                allChars.append(char)
                allCharCountDict[char] = 1
            else:
                allCharCountDict[char] += 1

    allChars.sort(key=lambda x: allCharCountDict[x], reverse=True)
    for char in allChars:
        print(char + ": " + str(allCharCountDict[char]))

else:
    quit()