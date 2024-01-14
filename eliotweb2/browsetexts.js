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
        editionText = editionText.replace(/([A-Z])/g, '<span style="color: red;">$1</span>')
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
    if (editionText.includes("׃")) {
        editionCell.style.textAlign = "right";
        editionCell.style.direction = "rtl";
        editionCell.style.fontSize = "1.4em";
    }
    if (isVerseNumber) {
        editionCell.style.textAlign = "center";
        editionCell.style.fontWeight = "bold";
        editionCell.style.fontSize = "1.2em";
        editionCell.style.verticalAlign = "center";
    }
    return editionText;
}

function printVersesToColumn(myJSON, editionKey, tableRow, hapaxMode="none", isVerseNumber=false, ignoreCase=false) {
    var editionText = formatText(myJSON[editionKey], hapaxMode, isVerseNumber, ignoreCase);
    var editionCell = document.createElement("td");
    
    editionCell.innerHTML = editionText;
    tableRow.appendChild(editionCell);
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

    var buttonDivNames = ["firstChapterButtonDiv", "prevChapterButtonDiv", "nextChapterButtonDiv", "lastChapterButtonDiv"];

    var buttonDivList = []

    for (var i = 0; i < buttonDivNames.length; i++) {
        var thisDiv = document.createElement("div");
        thisDiv.id = buttonDivNames[i];
        thisDiv.style.gridRow = "1";
        thisDiv.style.gridColumn = (i + 1).toString();
        buttonDivList.append(thisDiv);
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

    allButtonList.append(firstChapterButton);
    allButtonList.append(prevChapterButton);

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

    allButtonList.append(nextChapterButton);
    allButtonList.append(lastChapterButton);

    for (var i = 0; i < allButtonList.length; i++) {
        buttonDivList[i].classList.add(allButtonList[i]);
        document.getElementById("navButtonGrid").appendChild(buttonDivList[i]);
        
    }
}

function printVerses(JSONBlob, chapter, useFirst, useSecond, useMayhew, useZeroth, useGrebrew, markTextDifferences, hapaxMode, isLastChapter) {

    var JSONKeys = populateJSONKeys(markTextDifferences);
    createNavButtons(chapter, isLastChapter);(markTextDifferences, useMayhew, useZeroth);

    mayhewOnLeft = useMayhew && useFirst && useSecond;
    zerothOnLeft = useZeroth && useFirst && useSecond;

    mayhewOnRight = useMayhew && (! mayhewOnLeft);
    zerothOnRight = useZeroth && (! zerothOnLeft);

    
    for (var i = 0; i < JSONBlob.length; i++) {
        var thisVerseDict = JSONBlob[i];
        if (thisVerseDict["chapter"] == chapter) {
            var thisVerse = thisVerseDict["verse"];
            
            document.getElementById("tableBody").appendChild(document.createElement("tr")).id = "row" + thisVerse;

            thisRow = document.getElementById("row" + thisVerse);
            
            if (useFirst) {
                printVersesToColumn(thisVerseDict, JSONKeys[0], thisRow, hapaxMode);
            }
            if (useSecond) {
                printVersesToColumn(thisVerseDict, JSONKeys[1], thisRow, hapaxMode);
            }
            if (mayhewOnRight) {
                printVersesToColumn(thisVerseDict, "rawMayhew", thisRow, hapaxMode);
            }
            if (zerothOnRight) {
                printVersesToColumn(thisVerseDict, "rawZeroth", thisRow, hapaxMode);
            }

            printVersesToColumn(thisVerseDict, "fullverse", thisRow, "none", true);

            if (mayhewOnLeft) {
                printVersesToColumn(thisVerseDict, "rawMayhew", thisRow, hapaxMode);
            }
            if (zerothOnLeft) {
                printVersesToColumn(thisVerseDict, "rawZeroth", thisRow, hapaxMode);
            }
            printVersesToColumn(thisVerseDict, "rawKJV", thisRow);

            if (useGrebrew) {
                printVersesToColumn(thisVerseDict, "grebrew", thisRow, hapaxMode);
            }
        }
    }
}

function populateVerseColumns(bookJSON, myChapter) {
    for (var i = 0; i < bookJSON.length; i++) {
        var thisVerseDict = bookJSON[i];
        if (thisVerseDict["chapter"] == myChapter) {
            var thisVerse = thisVerseDict["verse"];

        }
    }
}

function populateCell(cellCounter, cellText, parentDiv, isHeader=false, isVerseNumber=false) {
    var cellDiv = document.createElement("div");
    if (cellCounter > 1) {
        columnHead.classList.add("editionHeader");
    } else {
        columnHead.classList.add("firstColumnHeader");
    }

    columnHead.style.gridColumn = cellCounter.toString();
    cellCounter++;

    if (isHeader) {
        cellDiv.innerHTML = "<h1><u>" + cellText + "</u></h1>";
    } else if (isVerseNumber) {
        cellDiv.innerHTML = "<b>" + cellText + "</b>";
    } else {
        cellDiv.innerHTML = cellText;
    }
    parentDiv.appendChild(cellDiv);
    //document.getElementById("editionHeaders").appendChild(columnHead);

    // An ugly little hack to avoid dealing with global variables
    return cellCounter;
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

function pushEditionToColumn(searchDict, editionLabel, columnList, columnCounter) {
    let useEdition = searchDict[editionLabel];
    if (useEdition) {
        columnCounter ++;
        columnList.push(editionLabel);
    }
    return useEdition;
}

function columnListPopulator(searchDict) {
    let numLeftColumns = 0;
    let numRightColumns = 1; // KJV has to be included

    let leftColumnList = [];
    let rightColumnList = [];

    let checkFirst = pushEditionToColumn(searchDict, "useFirstEdition", leftColumnList, numLeftColumns);
    let checkSecond = pushEditionToColumn(searchDict, "useSecondEdition", leftColumnList, numLeftColumns);

    if (checkFirst && checkSecond) {
        pushEditionToColumn(searchDict, "useMayhew", rightColumnList, numRightColumns);
        pushEditionToColumn(searchDict, "useZeroth", rightColumnList, numRightColumns);
    } else {
        pushEditionToColumn(searchDict, "useMayhew", leftColumnList, numLeftColumns);
        pushEditionToColumn(searchDict, "useZeroth", leftColumnList, numLeftColumns);
    }

    rightColumnList.push("KJV");

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

function populateHeaders(leftColumnList, rightColumnList, allColumnMeasures) {
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

    
    /*if (window.location.href.includes("?")) {
        var url = window.location.href.split("?")[0];
    } else {
        var url = window.location.href;
    }
    */
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
    
    var useFirstEdition = searchInfo["useFirstEdition"];
    var useSecondEdition = searchInfo["useSecondEdition"];
    var useGrebrew = searchInfo["useGrebrew"];
    var useMayhew = searchInfo["useMayhew"];
    var useZerothEdition = searchInfo["useZeroth"];

    let columnInfoList = columnListPopulator(searchInfo);
    var numLeftColumns = columnInfoList[0]; 
    var numRightColumns = columnInfoList[1];

    var leftColumnList = columnInfoList[2];
    var rightColumnList = columnInfoList[3];

    var hapaxMode = getHapaxMode(params);
    
    var onLastChapter = (myChapter == lastChapter);

    //Highly inelegant, but works

    var allColumnMeasures = "";
    var verseColumnMeasure = "10%"

    if (leftColumns == 1) {
        allColumnMeasures += "45% ";
    } else if (leftColumns == 2) {
        allColumnMeasures += "22.5% ";
        allColumnMeasures += "22.5% ";
    }

    allColumnMeasures += verseColumnMeasure + " ";
    
    if (rightColumns == 3) {
        allColumnMeasures += "15% ";
        allColumnMeasures += "15% ";
        allColumnMeasures += "15% ";
    } else if (rightColumns == 2) {
        rightColumnMeasure = "22.5%";
        allColumnMeasures += "22.5% ";
        allColumnMeasures += "22.5% ";
    } else {
        rightColumnMeasure = "45%";
        allColumnMeasures += "45% ";
    }

    populateHeaders(leftColumnList, rightColumnList, allColumnMeasures);
    
    var markTextDifferences = textDifferenceHandler(params);

    url = url.split("?")[0] + "?" + params.toString();
    window.history.replaceState({}, '', url);

    fetch('./textJSON/' + myBook + '.json')
        .then(res =>  {
            return res.json();
        })
        .then((data) => {
            printVerses(data, whichChapter, useFirstEdition, useSecondEdition, useMayhew, useZerothEdition, useGrebrew, markTextDifferences, hapaxMode, onLastChapter);
        })
    });

