const script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.7.1.min.js';
document.getElementsByTagName('head')[0].appendChild(script);


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

async function textFilePromise(fileName) {
    return fetch(fileName).then(response => response.text());
}

async function readTextFile(book, edition) {
    let fileName = "./texts/" + book + "." + edition + ".txt";
    let text = await textFilePromise(fileName);
    let lines = text.split("\n");
    return lines;
}

function jsonExists(fileName) {
    return fetch(fileName).then(response => response.ok);
}

async function hasJSON(book) {
    let fileName = "./textJSON/" + book + ".json";
    return await jsonExists(fileName);
}

function findWordInKJV(word, lines) {
    let wordCount = 0;
    let matchingVerses = [];
    for (let i = 0; i < lines.length; i++) {
        let verseWords = lines[i].split(" ");
        let verseAddress = verseWords[0];
        for (let j = 1; j < verseWords.length; j++) {
            if (verseWords[j] == word) {
                wordCount++;
                matchingVerses.push(verseAddress);
            }
        }
    }
    return matchingVerses;
}

async function getAllJSONs() {
    let bookJSONList = [];
    let bookNameList = [];
    for (let i = 0; i < allBookList.length; i++) {
        let hasJSONBool = await hasJSON(allBookList[i]);
        if (hasJSONBool && allBookList[i] != "Matthew") {
            console.log(allBookList[i]);
            bookNameList.push(allBookList[i]);
            let fileName = "./textJSON/" + allBookList[i] + ".json";
            let bookJSON = await fetch(fileName).then(response => response.json());
            if (bookJSON == null) {
                console.log("null json");
            } else {
                bookJSONList.push(bookJSON);
            }
        }
    }
    console.log(bookNameList);
    console.log(bookJSONList);
    return [bookNameList, bookJSONList];
}

async function findVersesWithWord(word) {
    let allMatchingBooks = await getAllJSONs();
    return allMatchingBooks[0];
    let matchingVerses = [];
    for (let i = 0; i < allMatchingBooks[0].length; i++) {
        let bookLines = await readTextFile(allMatchingBooks[0][i], "KJV");
        let matchingVersesForBook = findWordInKJV(word, bookLines);
        matchingVerses.push(matchingVersesForBook);
    }
    console.log(matchingVerses);
    
}

document.getElementById("submitBookQuery").addEventListener("click", async function () {
    
    document.getElementById("verseText").innerHTML = "";
    let searchWord = document.getElementById("search_bar").value;
    console.log(await findVersesWithWord(searchWord));
    /*
    for (i = 0; i < matchingVerses.length; i++) {
        for (j = 0; j < matchingVerses[i].length; j++) {
            let verseText = matchingVerses[i][j];
            let verseTextElement = document.createElement("p");
            verseTextElement.innerHTML = verseText;
            document.getElementById("verseText").appendChild(verseTextElement);
        }
    }
    */


    
    /*
    fetch('./wordcounts.json')
        .then(res => {
            return res.json();
        })
        .then((data) => {
            //document.getElementById("results").innerHTML = "";
            //getInstances(data, query, searchType, useFirst, useSecond, useMayhew, diacriticMode, result_mode);
        })
        */
})