
function cleanDiacritics(word) {
    var charReplacementDict = {
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
        "ā": "an",
        "ē": "en",
        "ī": "in",
        "ō": "on",
        "ū": "un"
    }

    var cleanedWord = "";
    for (var i = 0; i < word.length; i++) {
        if (word[i] in charReplacementDict) {
            cleanedWord += charReplacementDict[word[i]];
        } else {
            cleanedWord += word[i];
        }
    }
    return cleanedWord;
}

function checkIfWordMatches(testWord, query, searchType, diacritics) {
    query = query.trim();
    query = query.toLowerCase();
    if (query == "" || testWord == "") {
        return false;
    }

    //testWord = wordDict["word"]
    if (diacritics == "lax") {
        testWord = cleanDiacritics(testWord);
        query = cleanDiacritics(query);
    }

    if (searchType == "contains") {
        return testWord.includes(query);
    }

    if (searchType == "starts") {
        return testWord.startsWith(query);
    }

    if (searchType == "ends") {
        return testWord.endsWith(query);
    }

    if (searchType == "exact") {
        return testWord == query;
    }
}

function getCiteString(wordVerses, wordCounts) {
    var citeStringDict = {};
    var citeCountDict = {};
    var editionDict = {};
    var allSubCites = [];
    var citeString = "";

    var finalDict = {};
    var bookCountDict = {}
    var allBooks = [];
    for (var i = 0; i < wordVerses.length; i++) {
        var cite = wordVerses[i];
        var count = wordCounts[i];

        let splitCite = cite.split(".");
        let edition = splitCite[0];
        let book = splitCite[1];
        if (!(book in finalDict)) {
            finalDict[book] = "";
            bookCountDict[book] = 0;
            allBooks.push(book);
        }
        let verseCiteString = cite.substring(2);
        if (!allSubCites.includes(verseCiteString)) {
            allSubCites.push(verseCiteString);
        }
        if ((verseCiteString) in citeStringDict) {
            citeStringDict[verseCiteString].push(cite);
            editionDict[verseCiteString].push(edition);
            citeCountDict[verseCiteString].push(wordCounts[i]);
        } else {
            citeStringDict[verseCiteString] = [cite];
            editionDict[verseCiteString] = [edition];
            citeCountDict[verseCiteString] = [wordCounts[i]];
        }
    }

    for (var i = 0; i < allSubCites.length; i++) {
        var subCite = allSubCites[i];
        var subCiteEditions = editionDict[subCite];
        var subCiteCounts = citeCountDict[subCite];
        var subCiteString = "<sup>";
        var splitCite = subCite.split(".");
        var whichBook = splitCite[0];
        var verseCite = splitCite[1] + "." + splitCite[2];

        var threeEditions = (whichBook == "Psalms (prose)" || whichBook == "John" || whichBook == "Genesis");
        var inAllEliot = "α" in subCiteEditions && "β" in subCiteEditions;
        if (whichBook == "Genesis" && inAllEliot) {
            inAllEliot = "א" in subCiteEditions
        }

        var couldHaveMayhew = (whichBook == "Psalms (prose)" || whichBook == "John");

        if (subCiteEditions.includes("α")) {
            subCiteString += "α";
        }
        if (subCiteEditions.includes("β")) {
            subCiteString += "β";
        }
        if (subCiteEditions.includes("א")) {
            subCiteString += "א";
        }
        if (subCiteEditions.includes("α") && subCiteEditions.includes("β") && couldHaveMayhew) {
            subCiteString = "<sup>E";
        }
        if (subCiteEditions.includes("M")) {
            subCiteString += "M";
        }
        subCiteString += "</sup>";

        if (threeEditions) {
            if (subCiteEditions.length == 3) {
                subCiteString = "";
            }
        } else {
            if (subCiteEditions.length == 2) {
                subCiteString = "";
            }
        }

        subCiteString += verseCite;

        var firstCount = subCiteCounts[0];
        var moreThanOneToken = false;
        var allCountsSame = true;
        var allCountList = []
        var allEditionList = []
        for (var j = 0; j < subCiteEditions.length; j++) {
            bookCountDict[whichBook] += subCiteCounts[j];
            allCountList.push(subCiteCounts[j]);
            allEditionList.push(subCiteEditions[j]);
            if (subCiteCounts[j] != firstCount) {
                allCountsSame = false;
            }
            if (subCiteCounts[j] > 1) {
                moreThanOneToken = true;
            }
        }

        if (allCountsSame) {
            if (moreThanOneToken) {
                subCiteString += " (" + firstCount + ")";
            }
        } else {
            subCiteString += " (";
            for (j = 0; j < allCountList.length; j++) {
                subCiteString += "<sup>" + allEditionList[j] + "</sup>" + allCountList[j] + "/";
            }
            subCiteString += ")";
        }
        subCiteString = subCiteString.replaceAll("/)", ")");
        finalDict[whichBook] += subCiteString + ", ";

    }
    return [finalDict, allBooks, bookCountDict];
}

function descendingFrequency(a, b) {
    return b - a;
}

function getInstances(dataJSON, query, searchType, useFirst, useSecond, useMayhew, diacritics, result_mode) {
    var matchingWords = [];
    var matchingWordCounts = {};
    var wordCiteDict = {};
    var wordBookDict = {};
    var matchingWordDicts = [];
    var bookWordCountDict = {};

    var allTokens = 0;
    var allKeyList = [];

    let sortedEntries = (result_mode === "frequency") ? dataJSON.toSorted((a, b) => {
        return b["wordCountDiacritics"] - a["wordCountDiacritics"];
    }) : dataJSON.toSorted(Intl.Collator().compare);

    for (wordDict of sortedEntries) {
        let testWord = wordDict["word"];
        let wordCount = wordDict["wordCountDiacritics"];
        if (checkIfWordMatches(testWord, query, searchType, diacritics) && wordCount > 0) {
            matchingWords.push(testWord.replaceAll("8", "ž"));
            matchingWordCounts[testWord] = wordCount;
            allCites = wordDict["allVersesDiacritics"];
            allCitecounts = wordDict["verseCountDiacritics"];
            var wordCiteString = getCiteString(allCites, allCitecounts);

            wordCiteDict[testWord] = wordCiteString[0];
            wordBookDict[testWord] = wordCiteString[1];
            bookWordCountDict[testWord] = wordCiteString[2];
            for (book in bookWordCountDict[testWord]) {
                allTokens += bookWordCountDict[testWord][book];
            }
        }
    }

    document.getElementById("results").innerHTML += "<h2><u>" + matchingWords.length.toString() + "</u> distinct strings found, representing <u>" + allTokens.toString() + "</u> distinct tokens<br>";

    for (let i = 0; i < matchingWords.length; i++) {
        let word = matchingWords[i].replaceAll("ž", "8");
        let count = "";
        try {
            count = " (" + matchingWordCounts[word].toString() + ")";
        } catch (error) {
            console.log(word);
            count = " (???)";
        }

        document.getElementById("results").innerHTML += "<i>" + word.replaceAll("8", "ꝏ̄") + "</i>" + count + ":<br>";
        let citeDict = wordCiteDict[word];
        let wordBookList = wordBookDict[word];

        for (let j = 0; j < wordBookList.length; j++) {
            let book = wordBookList[j];
            let bookWordCount = bookWordCountDict[word][book];
            let citeString = citeDict[book].slice(0, -2);
            var citeDiv = document.createElement("div");
            citeDiv.innerHTML = "\t<b>" + book + "</b> (" + bookWordCount.toString() + "): " + citeString;
            citeDiv.style.textIndent = "1em";
            document.getElementById("results").appendChild(citeDiv);

        }
        document.getElementById("results").innerHTML += "<br>";
    }
}

document.getElementById("submit").addEventListener("click", function () {
    var searchType = document.getElementById("searchWordDropdown").value;

    var diacriticMode = "";
    if (document.getElementById("diacritics_strict").checked) {
        diacriticMode = "strict";
    } else if (document.getElementById("diacritics_lax").checked) {
        diacriticMode = "lax";
    }

    var useFirst = document.getElementById("include_first_edition").checked;
    var useSecond = document.getElementById("include_second_edition").checked;
    var useMayhew = document.getElementById("include_mayhew").checked;
    //var useZeroth = document.getElementById("include_zeroth_edition").checked;

    var result_mode = "";
    if (document.getElementById("show_verses").checked) {
        result_mode = "verses";
    } else if (document.getElementById("alphabetical_list").checked) {
        result_mode = "alphabetical";
    } else if (document.getElementById("show_frequency").checked) {
        result_mode = "frequency";
    }

    var query = document.getElementById("search_bar").value;

    fetch('./wordcounts.json')
        .then(res => {
            return res.json();
        })
        .then((data) => {
            document.getElementById("results").innerHTML = "";
            getInstances(data, query, searchType, useFirst, useSecond, useMayhew, diacriticMode, result_mode);
        })
})