const alphabet = require('./alphabet.js');
const fs = require('fs');

transform = (data, radix) => {
    let binary = '';
    for (let i = 0; i < data.length; i++) {
        binary += data.charCodeAt(i).toString(radix);
    }
    return binary;
}

let latinText = (fs.readFileSync('./latinText.txt')).toString().toLowerCase();
let latinTextAlphabet = alphabet.alphabet(latinText);
let latinEntropy = alphabet.entropy(latinTextAlphabet);
console.log('Энтропия алфавита латинского текста:', latinEntropy);

let cyrilText = (fs.readFileSync('./cyrilText.txt')).toString().toLowerCase();
let cyrilTextAlphabet = alphabet.alphabet(cyrilText);
let cyrilEntropy = alphabet.entropy(cyrilTextAlphabet);
console.log('Энтропия алфавита текста кириллицы:', cyrilEntropy);

// alphabet.saveAlphabetToExcel([latinTextAlphabet, cyrilTextAlphabet], 'report.xlsx');


const binData = fs.readFileSync('./main.js');
let binary = alphabet.alphabet(transform(binData.toString(), 2));
let binaryEntropy = alphabet.entropy(binary);
console.log('Энтропия алфавита бинарных данных:', binaryEntropy);


let nameText = 'кирилл лысков евгеньевич';
let name = alphabet.alphabet(nameText);
let nameEntropy = alphabet.entropy(name);
console.log('Энтропия алфавита ФИО:', nameEntropy);
console.log('Количество информации ФИО:', nameEntropy * nameText.length);

let binNameText = transform(nameText, 2);
let binName = alphabet.alphabet(binNameText);
let binNameEntropy = alphabet.entropy(binName);
console.log('Энтропия алфавита ФИО (ASCII):', binNameEntropy);
console.log('Количество информации ФИО (ASCII):', binNameEntropy * binNameText.length);


binNameEntropy = alphabet.entropy(binName, 0.1);
console.log('Энтропия алфавита ФИО, p = 0.1:', binNameEntropy);
console.log('Количество информации ФИО:', binNameEntropy * binNameText.length);

binNameEntropy = alphabet.entropy(binName, 0.5);
console.log('Энтропия алфавита ФИО, p = 0.5:', binNameEntropy);
console.log('Количество информации ФИО:', binNameEntropy * binNameText.length);

binNameEntropy = alphabet.entropy(binName, 1.0);
console.log('Энтропия алфавита ФИО, p = 1.0:', binNameEntropy);
console.log('Количество информации ФИО:', binNameEntropy * binNameText.length);