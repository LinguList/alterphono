/* require libraries */
var fs = require("fs");
var path = require("path");
var parser = require(path.join(__dirname, "phonogrammar"));

/**
 * Returns the contents of a file.
 * @param {string} filename - The filename to be read; the current
 *     path is automatically appended.
 * @returns {string} The contents of the file.
 */
function readFile(filename) {
    "use strict";

    var source = fs.readFileSync(path.join(__dirname, filename), {
        encoding: "utf8"
    });

    return source;
}

/**
 * Parses with pegjs the contents of a grammar, provided as a string,
 * and performs data manipulation for returning an object for textual
 * generation.
 * @param {string} source - A string the full source of the grammar.
 * @param {Object} A Grammar object for textual generation.
 */
function parsePhonoGrammar(source) {
    "use strict";

    /* the grammar object to be returned */
    var grammar = {};

    /* parses the source with pegjs */
    var parsedGrammar = parser.parse(source);

console.log(JSON.stringify(parsedGrammar, null, 2));

    return grammar;
}


/* program starts here */
//var filename = 'pie.phono';
//var grammar = parsePhonoGrammar(readFile(filename));

ipa = JSON.parse(readFile('ipa.json'));
cat = JSON.parse(readFile('categories.json'));

for (entry in ipa) {
console.log(entry + " " + ipa[entry].desc);
}

