#This program takes text files of transcripts from the Massachusett Bible directory and copies them here.

import os
import re
import shutil

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
    "Revelation",
]


outputDirectory = "./texts/"

inputDirectory = "../massachusett stuff/"

for bookName in allBookList:
    for editionName in ["First Edition.txt", "Second Edition.txt", "KJV.txt"]:
        inputPath = inputDirectory + "/" + bookName + "/" + editionName
        outputPath = outputDirectory + bookName + "." + editionName
        if os.path.exists(inputPath):        
            shutil.copyfile(inputPath, outputPath)
        else:
            print("Could not find " + editionName[:-4] + " of " + bookName)

extraFileNames = ["../massachusett stuff/Genesis/Zeroth Edition.txt", "../massachusett stuff/Psalms (prose)/Mayhew.txt", "../massachusett stuff/John/Mayhew.txt"]

outputFileNames = ["./texts/Genesis.Zeroth Edition.txt", "./texts/Psalms (prose).Mayhew.txt", "./texts/John.Mayhew.txt"]

for i in range(len(extraFileNames)):
    shutil.copyfile(extraFileNames[i], outputFileNames[i])


checkForLigatures = False
if checkForLigatures:
    allfilesWithLigature = 0
    for textFile in os.listdir(outputDirectory):
        hasLigature = False
        if textFile.endswith(".txt"):
            with open(outputDirectory + textFile, "r", encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    if 'ꝏ̄' in line:
                        if hasLigature == False:
                            allfilesWithLigature += 1
                            hasLigature = True
                        print(textFile +  " has a ꝏ̄")
                else:
                    continue
            
        else:
            continue

    print("There are " + str(allfilesWithLigature) + " files with <ꝏ̄> in them.")