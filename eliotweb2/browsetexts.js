/*
const http = require('http');
const host = 'localhost';
const port = 8000;

const fs = require('fs').promises;

const requestListener = function (req, res) {
    fs.readFile(__dirname + "/browsetexts.html")
    .then(contents => {
        res.setHeader("Content-Type", "text/html");
        res.writeHead(200);
        res.end(contents);
    })
    .catch(err => {
        res.writeHead(500);
        res.end(err);
        return;
    });
};
*/

const allBookList = [
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
    "Revelation"
];

const bookToChapterDict = {
    "": 0,
    "Genesis": 50,
    "Exodus": 40,
    "Leviticus": 27,
    "Numbers": 36,
    "Deuteronomy": 34,
    "Joshua": 24,
    "Judges": 21,
    "Ruth": 4,
    "1 Samuel": 31,
    "2 Samuel": 24,
    "1 Kings": 22,
    "2 Kings": 25,
    "1 Chronicles": 29,
    "2 Chronicles": 36,
    "Ezra": 10,
    "Nehemiah": 13,
    "Esther": 10,
    "Job": 42,
    "Psalms (prose)": 150,
    "Psalms (metrical)": 150,
    "Proverbs": 31,
    "Ecclesiastes": 12,
    "Song of Songs": 8,
    "Isaiah": 66,
    "Jeremiah": 52,
    "Lamentations": 5,
    "Ezekiel": 48,
    "Daniel": 12,
    "Hosea": 14,
    "Joel": 3,
    "Amos": 9,
    "Obadiah": 1,
    "Jonah": 4,
    "Micah": 7,
    "Nahum": 3,
    "Habakkuk": 3,
    "Zephaniah": 3,
    "Haggai": 2,
    "Zechariah": 14,
    "Malachi": 4,
    "Matthew": 28,
    "Mark": 16,
    "Luke": 24,
    "John": 21,
    "Acts": 28,
    "Romans": 16,
    "1 Corinthians": 16,
    "2 Corinthians": 13,
    "Galatians": 6,
    "Ephesians": 6,
    "Philippians": 4,
    "Colossians": 4,
    "1 Thessalonians": 5,
    "2 Thessalonians": 3,
    "1 Timothy": 6,
    "2 Timothy": 4,
    "Titus": 3,
    "Philemon": 1,
    "Hebrews": 13,
    "James": 5,
    "1 Peter": 5,
    "2 Peter": 3,
    "1 John": 5,
    "2 John": 1,
    "3 John": 1,
    "Jude": 1,
    "Revelation": 22
};

const OTBookList = [
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
    "Malachi"
];

const NTBookList = [
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
];

function updateChapterDropdown(whichBook) {
    var chapterDropdown = document.getElementById("chapterSelectionDropdown");
    chapterDropdown.innerHTML = "";
    for (var i = 1; i <= bookToChapterDict[whichBook]; i++) {
        var option = document.createElement("option");
        option.text = i;
        chapterDropdown.add(option);
    }
}

var bookDropdown = document.getElementById("bookSelectionDropdown");
for (var i = 0; i < allBookList.length; i++) {
    var option = document.createElement("option");
    option.text = allBookList[i];
    bookDropdown.add(option);
    updateChapterDropdown(option.text);
}

bookDropdown.addEventListener("change", function() {
    updateChapterDropdown(bookDropdown.value);
    if (bookDropdown.value == "Psalms (prose)" || bookDropdown.value == "John") {
        var useMayhew = document.createElement("input");
        const label = document.createElement("label");
        label.htmlFor = "useMayhew";
        label.innerHTML = "Mayhew (1709)";

        useMayhew.type = "checkbox";
        useMayhew.id = "useMayhew";
        useMayhew.value = "useMayhew";
        useMayhew.name = "useMayhew";

        useMayhew.checked = true;
        document.getElementById("otherEditions").appendChild(useMayhew);
        document.getElementById("otherEditions").appendChild(label);
    } 
    
    else if (bookDropdown.value == "Genesis") {
        var useZeroth = document.createElement("input");
        const label = document.createElement("label");
        label.htmlFor = "useZeroth";
        label.innerHTML = "Zeroth Edition (1655)";

        useZeroth.type = "checkbox";
        useZeroth.id = "useZeroth";
        useZeroth.value = "useZeroth";
        useZeroth.name = "useZeroth";

        useZeroth.checked = true;
        document.getElementById("otherEditions").appendChild(useZeroth);
        document.getElementById("otherEditions").appendChild(label);
    }
    else {
        document.getElementById("otherEditions").innerHTML = "";
    }
});

function formatText(editionText, hapaxMode="none", isVerseNumber=false, ignoreCase=false) {
    editionText = editionText.replaceAll('$', ' ');
    if (ignoreCase) {
        editionText = editionText.replace('<span style="color: blue">', '');
    }
    if (hapaxMode == "lax") {
        editionText = editionText.replaceAll('‹', '');
        editionText = editionText.replaceAll('›', '');
        editionText = editionText.replaceAll('«', '<u>');
        editionText = editionText.replaceAll('»', '</u>');
        editionText = editionText.replaceAll('<H>', '<span style="color: blue">');
        editionText = editionText.replaceAll('</H>', '</span>');
    } else if (hapaxMode == "strict") {
        editionText = editionText.replaceAll('‹', '<u>');
        editionText = editionText.replaceAll('›', '</u>');
        editionText = editionText.replaceAll('«', '<u>');
        editionText = editionText.replaceAll('»', '</u>');
        editionText = editionText.replaceAll('<H>', '<span style="color: blue">');
        editionText = editionText.replaceAll('</H>', '</span>');
    } else {
        editionText = editionText.replaceAll('‹', '');
        editionText = editionText.replaceAll('›', '');
        editionText = editionText.replaceAll('«', '');
        editionText = editionText.replaceAll('»', '');
        editionText = editionText.replaceAll('<u>', '');
        editionText = editionText.replaceAll('</u>', '');
        editionText = editionText.replaceAll('<H>', '');
        editionText = editionText.replaceAll('</H>', '');
    } 
    return editionText;
}

function populateJSONKeys(markTextDifferences)  {

    //Zeroth edition isn't compared yet, but should be compared vs. the 1st edition
    let JSONKeys = [];
    if (markTextDifferences == "none") {
        JSONKeys = ["rawFirstEdition", "rawSecondEdition", "rawZerothEdition"];
    } else if (markTextDifferences == "excludeCasing") {
        JSONKeys = ["caseInsensitiveFirst", "caseInsensitiveSecond", "caseInsensitiveZeroth"];
    } else {
        JSONKeys = ["comparedFirstEdition", "comparedSecondEdition", "comparedZerothEdition"];
    }
    // Will we ever do compared versions of Mayhew?
    return JSONKeys;
}

function createNavButtons(currentChapter, isLastChapter) {
    document.getElementById("navButtonGrid").innerHTML = "";
    document.getElementById("navButtonGrid").style.background = "white";

    var buttonDivNames = ["firstChapterButtonDiv", "prevChapterButtonDiv", "nextChapterButtonDiv", "lastChapterButtonDiv"];

    var buttonDivList = []

    for (var i = 0; i < buttonDivNames.length; i++) {
        var thisDiv = document.createElement("div");
        thisDiv.id = buttonDivNames[i];
        thisDiv.style.gridRow = "1";
        thisDiv.style.gridColumn = (i + 1).toString();
        buttonDivList.push(thisDiv);
    }
    
    let allButtonList = [];

    if (currentChapter > 1) {
        var firstChapterButton = document.createElement("button");
        firstChapterButton.innerHTML = "↞";
        firstChapterButton.id = "firstChapterButton";

        firstChapterButton.addEventListener("click", function() {
            document.getElementById("chapterSelectionDropdown").value = 1;
            document.getElementById("submitBookQuery").click();
        });

        var prevChapterButton = document.createElement("button");
        prevChapterButton.innerHTML = "←";
        prevChapterButton.id = "prevChapterButton";

        prevChapterButton.addEventListener("click", function() {
            document.getElementById("chapterSelectionDropdown").value = parseInt(currentChapter) - 1;
            document.getElementById("submitBookQuery").click();
        });

    } else {
        var firstChapterButton = document.createElement("span");
        var prevChapterButton = document.createElement("span");
    }

    allButtonList.push(firstChapterButton);
    allButtonList.push(prevChapterButton);

    if (! isLastChapter) {
        var nextChapterButton = document.createElement("button");
        nextChapterButton.innerHTML = "→";
        nextChapterButton.id = "nextChapterButton";

        nextChapterButton.addEventListener("click", function() {
            document.getElementById("chapterSelectionDropdown").value = parseInt(currentChapter) + 1;
            document.getElementById("submitBookQuery").click();
        });
        
        var lastChapterButton = document.createElement("button");
        lastChapterButton.innerHTML = "↠";
        lastChapterButton.id = "lastChapterButton";

        lastChapterButton.addEventListener("click", function() {
            document.getElementById("chapterSelectionDropdown").value = bookToChapterDict[document.getElementById("bookSelectionDropdown").value];
            document.getElementById("submitBookQuery").click();
        });
    } else {
        var nextChapterButton = document.createElement("span");
        var lastChapterButton = document.createElement("span");
    }

    allButtonList.push(nextChapterButton);
    allButtonList.push(lastChapterButton);

    for (var i = 0; i < allButtonList.length; i++) {
        buttonDivList[i].appendChild(allButtonList[i]);
        document.getElementById("navButtonGrid").appendChild(buttonDivList[i]);
    }
}

function populateVerseRow(verseDict, infoDict, hapaxMode, markTextDiffs) {
    var myKeys = populateJSONKeys(markTextDiffs);

    var ignoreCasing = false;
    if (markTextDiffs == "excludeCasing") {
        ignoreCasing = true;
    }

    allTextList = [];
    whichTextList = [];
    var hasAltEdition = infoDict["useMayhew"] || infoDict["useZeroth"];

    var whichAltEdition = "";

    //Won't always be raw
    if (hasAltEdition) {
        if (infoDict["useMayhew"]) {
            whichAltEdition = "rawMayhew";
        } else {
            whichAltEdition = "rawZeroth";
        }
    }

    var altEditionOnRight = hasAltEdition && infoDict["useFirstEdition"] && infoDict["useSecondEdition"];

    if (infoDict["useFirstEdition"]) {
        var firstEditionText = verseDict[myKeys[0]];
        allTextList.push(formatText(firstEditionText, hapaxMode, false, ignoreCasing));
        whichTextList.push("first");
    }
    if (infoDict["useSecondEdition"]) {
        var secondEditionText = verseDict[myKeys[1]];
        allTextList.push(formatText(secondEditionText, hapaxMode, false, ignoreCasing));
        whichTextList.push("second");
    }

    if (altEditionOnRight) {
        var altEditionText = verseDict[whichAltEdition];
        allTextList.push(formatText(altEditionText, hapaxMode, false, ignoreCasing));
        whichTextList.push("alt");
    }

    allTextList.push(formatText(verseDict["fullverse"], "none", true));
    whichTextList.push("verse");

    if (hasAltEdition && ! altEditionOnRight) {
        var altEditionText = verseDict[whichAltEdition];
        allTextList.push(formatText(altEditionText, hapaxMode, false, ignoreCasing));
        whichTextList.push("alt");
    }

    var KJVText = verseDict["rawKJV"];
    allTextList.push(formatText(KJVText, "none", false, false));
    whichTextList.push("KJV");

    if (infoDict["useGrebrew"]) {
        var grebrewText = verseDict["grebrew"];
        allTextList.push(formatText(grebrewText, hapaxMode, false, ignoreCasing));
        if (grebrewText.includes("׃")) {
            whichTextList.push("hebrew");
        } else {
            whichTextList.push("greek");
        }
    }
    return [allTextList, whichTextList];
}

function populateCell(cellCounter, cellText, parentDiv, isHeader=false, isVerseNumber=false) {
    var cellDiv = document.createElement("div");
    if (cellCounter > 1) {
        cellDiv.classList.add("editionHeader");
    } else {
        cellDiv.classList.add("firstColumnHeader");
    }

    cellDiv.style.gridColumn = cellCounter.toString();
    cellCounter++;

    if (isHeader) {
        cellDiv.innerHTML = "<h1><u>" + cellText + "</u></h1>";
    } else if (isVerseNumber) {
        cellDiv.innerHTML = "<b>" + cellText + "</b>";
    } else {
        cellDiv.innerHTML = cellText;
    }
    parentDiv.appendChild(cellDiv);

    // An ugly little hack to avoid dealing with global variables
    return cellCounter;
}

function populateVerseColumns(bookJSON, myChapter, columnMeasureString, searchInfo, hapaxMode, markTextDiffs) {
    var topDiv = document.getElementById("textColumns");
    topDiv.innerHTML = "";
    for (var i = 0; i < bookJSON.length; i++) {
        var thisVerseDict = bookJSON[i];
        if (thisVerseDict["chapter"] == myChapter) {
            var thisVerse = thisVerseDict["verse"];
            var verseDiv = document.createElement("div");
            verseDiv.classList.add("verseRow");
            verseDiv.id = "verse " + thisVerse;
            verseDiv.style.gridRow = (i + 1).toString();
            verseDiv.style.gridTemplateColumns = columnMeasureString;
            var allVerseTexts = populateVerseRow(thisVerseDict, searchInfo, hapaxMode, markTextDiffs);
            var allVerses = allVerseTexts[0];
            var allVerseTypes = allVerseTexts[1];

            for (var j = 0; j < allVerses.length; j++) {
                var verseColumn = document.createElement("div");
                if (j > 0) {
                    verseColumn.classList.add("verseColumn");
                } else {
                    verseColumn.classList.add("firstVerseColumn");
                }
                verseColumn.style.gridColumn = (j + 1).toString();
                verseColumn.innerHTML = allVerses[j];

                if (allVerseTypes[j] == "verse") {
                    verseColumn.style.textAlign = "center";
                    verseColumn.style.fontWeight = "bold";
                    verseColumn.style.fontSize = "1.2em";
                    verseColumn.style.verticalAlign = "center";
                }

                if (allVerseTypes[j] == "hebrew") {
                    verseColumn.style.textAlign = "right";
                    verseColumn.style.direction = "rtl";
                    verseColumn.style.fontSize = "1.4em";
                }

                verseDiv.appendChild(verseColumn);
            }
            topDiv.appendChild(verseDiv);
        }
    }
}

function getHapaxMode(myParams) {
    if (document.getElementById("hapaxes_lax").checked) {
        myParams.append("markHapaxes", "lax");
        return "lax";
    } else if (document.getElementById("hapaxes_strict").checked) {
        myParams.append("markHapaxes", "strict");
        return "strict";
    } else {
        return "none";
    }
}

function useEdition(editionLabel, myParams, paramLabel) {
    let useEdition = document.getElementById(editionLabel).checked;
    if (useEdition) {
        myParams.append(paramLabel, useEdition);
    }
    return useEdition;
}

function searchInfoGetter(myParams) {
    let searchDict = {};

    let bookPick = document.getElementById("bookSelectionDropdown").value;
    searchDict["book"] = bookPick;
    myParams.append("book", bookPick);

    let chapterList = document.getElementById("chapterSelectionDropdown");
    let lastChapter = chapterList[chapterList.length - 1].value; // Needed later for the side buttons
    searchDict["lastChapter"] = lastChapter;
    let chapterPick = chapterList.value;
    searchDict["chapter"] = chapterPick;
    myParams.append("chapter", chapterPick);

    searchDict["useFirstEdition"] = useEdition("useFirstEdition", myParams, "showFirstEd");
    searchDict["useSecondEdition"] = useEdition("useSecondEdition", myParams, "showSecondEd");
    searchDict["useGrebrew"] = useEdition("useGrebrew", myParams, "showGrebrew");

    if (bookPick == "Psalms (prose)" || bookPick == "John") {
        searchDict["useMayhew"] = useEdition(searchDict, "useMayhew", myParams, "showMayhew");
    } else {
        searchDict["useMayhew"] = false;
    }

    if (bookPick == "Genesis") {
        searchDict["useZeroth"] = useEdition(searchDict, "useZeroth", myParams, "showZerothEd");
    } else {
        searchDict["useZeroth"] = false;
    }

    return searchDict;
}

function pushEditionToColumn(name, searchDict, editionLabel, columnList, columnCounter) {
    let useEdition = searchDict[editionLabel];
    if (useEdition) {
        columnCounter++;
        columnList.push(name);
    }
    return columnCounter;
}

function columnListPopulator(searchDict) {
    var numLeftColumns = 0;
    var numRightColumns = 0;

    var leftColumnList = [];
    var rightColumnList = [];

    numLeftColumns = pushEditionToColumn("First Edition", searchDict, "useFirstEdition", leftColumnList, numLeftColumns);
    numLeftColumns = pushEditionToColumn("Second Edition", searchDict, "useSecondEdition", leftColumnList, numLeftColumns);


    if (numLeftColumns > 1) {
        numRightColumns = pushEditionToColumn("Mayhew", searchDict, "useMayhew", rightColumnList, numRightColumns);
        numRightColumns = pushEditionToColumn("Zeroth Edition", searchDict, "useZeroth", rightColumnList, numRightColumns);
    } else {
        numLeftColumns = pushEditionToColumn("Mayhew", searchDict, "useMayhew", leftColumnList, numLeftColumns);
        numLeftColumns = pushEditionToColumn("Zeroth Edition", searchDict, "useZeroth", leftColumnList, numLeftColumns);
    }

    rightColumnList.push("KJV");
    numRightColumns++;

    if (searchDict["useGrebrew"]) {
        nameString = ""
        if (NTBookList.includes(searchDict["book"])) {
            nameString = "Greek";
        } else {
            nameString = "Hebrew";
        }
        numRightColumns++;
        rightColumnList.push(nameString);
    }
    return [numLeftColumns, numRightColumns, leftColumnList, rightColumnList];
}

function columnMeasurePopulator(numLeftColumns, numRightColumns) {
    var allColumnMeasures = "";
    var verseColumnMeasure = "10%"
    if (numLeftColumns == 1) {
        allColumnMeasures += "45% ";
    } else if (numLeftColumns == 2) {
        allColumnMeasures += "22.5% ";
        allColumnMeasures += "22.5% ";
    }

    allColumnMeasures += verseColumnMeasure + " ";
    
    if (numRightColumns == 3) {
        allColumnMeasures += "15% ";
        allColumnMeasures += "15% ";
        allColumnMeasures += "15% ";
    } else if (numRightColumns == 2) {
        rightColumnMeasure = "22.5%";
        allColumnMeasures += "22.5% ";
        allColumnMeasures += "22.5% ";
    } else {
        rightColumnMeasure = "45%";
        allColumnMeasures += "45% ";
    }

    return allColumnMeasures.trim();
}

function populateHeaders(mySearchInfo) {
    let columnInfoList = columnListPopulator(mySearchInfo);
    let numLeftColumns = columnInfoList[0]; 
    let numRightColumns = columnInfoList[1];

    let leftColumnList = columnInfoList[2];
    let rightColumnList = columnInfoList[3];

    let allColumnMeasures = columnMeasurePopulator(numLeftColumns, numRightColumns);

    var whichColumnCounter = 1;
    var editionHeaders = document.getElementById("editionHeaders");
    editionHeaders.innerHTML = "";
    editionHeaders.style.textAlign = "center";
    editionHeaders.style.gridTemplateColumns = allColumnMeasures;
    for (var i = 0; i < leftColumnList.length; i++) {
        whichColumnCounter = populateCell(whichColumnCounter, leftColumnList[i], editionHeaders, true, false);
    }

    whichColumnCounter = populateCell(whichColumnCounter, "Verse", editionHeaders, true, false);
    
    for (var i = 0; i < rightColumnList.length; i++) {
        whichColumnCounter = populateCell(whichColumnCounter, rightColumnList[i], editionHeaders, true, false);
    }

    return allColumnMeasures;
}

function textDifferenceHandler(myParams) {
    if (document.getElementById("include_casing").checked) {
        myParams.append("markDiffs", "includeCasing");
        return "includeCasing";
    } else if (document.getElementById("exclude_casing").checked) {
        myParams.append("markDiffs", "excludeCasing");
        return "excludeCasing";
    } else {
        return "none";
    }
}

document.getElementById("submitBookQuery").addEventListener("click", function() {

    window.scrollTo(0, 0);
    var url = window.location.href;

    let params = new URLSearchParams(url.search);

    var myQueryOptions = document.getElementById("queryOptions");
    for (var i = 0; i < myQueryOptions.length; i++) {
        myQueryOptions[i].defaultChecked = myQueryOptions[i].checked; // Does this do anything?
        }

    var searchInfo = searchInfoGetter(params);
    var myBook = searchInfo["book"];
    var myChapter = searchInfo["chapter"];
    var lastChapter = searchInfo["lastChapter"];
    

    var allColumnMeasures = populateHeaders(searchInfo);
    
    var hapaxMode = getHapaxMode(params);
    
    var isLastChapter = (myChapter == lastChapter);
    
    var markTextDifferences = textDifferenceHandler(params);

    url = url.split("?")[0] + "?" + params.toString();
    window.history.replaceState({}, '', url);

    fetch('./textJSON/' + myBook + '.json')
        .then(res =>  {
            return res.json();
        })
        .then((data) => {
            createNavButtons(myChapter, isLastChapter);
            populateVerseColumns(data, myChapter, allColumnMeasures, searchInfo, hapaxMode, markTextDifferences);
        })
    });

