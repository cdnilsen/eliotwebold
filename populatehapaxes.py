from wordfrequencymodule import populateHapaxes

showChars = input("Show all characters in hapaxes? (y/n) ")

populateHapaxes()

allHapaxes = open("hapaxLegomenaStrict.txt", "r", encoding="utf-8").readlines()
allLaxHapaxes = open("hapaxLegomenaLax.txt", "r", encoding="utf-8").readlines()

if showChars == "y":
    allChars = []
    allCharCountDict = {}
    allCharVerseDict: {}
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

print("Number of strict hapaxes: " + str(len(allHapaxes)))
print("Number of lax hapaxes: " + str(len(allLaxHapaxes)))

quit()