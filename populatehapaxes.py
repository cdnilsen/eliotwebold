from wordfrequencymodule import populateHapaxes
import datetime

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


#print(str(datetime.datetime.now()) + " Number of strict hapaxes: " + str(len(allHapaxes)))

hapaxLog = open("hapaxLog.txt", "a", encoding="utf-8")
hapaxLog.write("[" + str(datetime.datetime.now()) + "]\n"  + "\tStrict hapaxes: " + str(len(allHapaxes)) + "\n\t" + "Lax hapaxes: " + str(len(allLaxHapaxes)) + "\n\n")
hapaxLog.close()

quit()