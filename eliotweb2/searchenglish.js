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

function readTextFile(book, edition) {
    var lineArray = [];
    $.get("./texts/" + book + "." + edition + ".txt", function(data) {
    }).done(function(data) {
        console.log("Success");
        var splitLines = data.split("\n");
        for (let i = 0; i < splitLines.length; i++) {
            console.log(typeof splitLines[i]);
            lineArray.push(splitLines[i]);
        }
    }).fail(function() {
        console.log("Error");
    });
    return lineArray;
}


function seeIfBookHasJSON(book) {
    $(document).ready(function(){
        $.getJSON("./textJSON/" + book + ".json", function(data){
            console.log(book + ": true");
        }).fail(function(){
            console.log(book + ": false");
        });
    });
}

document.getElementById("submitBookQuery").addEventListener("click", function () {
    
    //var query = document.getElementById("search_bar").value;

    var exodusKJV = readTextFile("Exodus", "KJV");
    console.log(exodusKJV instanceof Array);

    exodusKJV = Array.from(exodusKJV);
    console.log(exodusKJV instanceof Array);
    
    console.log(exodusKJV.length)
    for (let i = 0; i < exodusKJV.length; i++) {
        console.log(exodusKJV[i]);
    }

    fetch('./wordcounts.json')
        .then(res => {
            return res.json();
        })
        .then((data) => {
            //document.getElementById("results").innerHTML = "";
            //getInstances(data, query, searchType, useFirst, useSecond, useMayhew, diacriticMode, result_mode);
        })
})