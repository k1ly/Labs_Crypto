const cipher = require('./cipher.js');
const alphabet = require('./alphabet.js');
const fs = require('fs');

let plainText = [...fs.readFileSync('./plainText.txt').toString().toLowerCase()]
    .filter(value => value.match('[абвгдеёжзийклмнопрстуфхцчшщъыьэюя]')).join('');

let start = new Date();
let codedPortaCipherText = cipher.codeRussianPortaCipher(plainText);
console.log('Время выполнения зашифрования (шифр Порты):', new Date() - start);
start = new Date();
let decodedPortaCipherText = cipher.decodeRussianPortaCipher(codedPortaCipherText);
console.log('Время выполнения расшифрования (шифр Порты):', new Date() - start);
if (plainText.length % 2 === 1)
    decodedPortaCipherText = decodedPortaCipherText.substring(0, decodedPortaCipherText.length - 1);
console.log('Расшифрованный текст совпадает с исходным (шифр Порты):', plainText === decodedPortaCipherText ? 'да' : 'нет');

start = new Date();
let codedKeywordCesarCipherText = cipher.codeRussianKeywordCesarCipher(plainText, 'лысков');
console.log('Время выполнения зашифрования (шифр Цезаря с ключевым словом):', new Date() - start);
start = new Date();
let decodedKeywordCesarCipherText = cipher.decodeRussianKeywordCesarCipher(codedKeywordCesarCipherText, 'лысков');
console.log('Время выполнения расшифрования (шифр Цезаря с ключевым словом):', new Date() - start);
console.log('Расшифрованный текст совпадает с исходным (шифр Цезаря с ключевым словом):', plainText === decodedKeywordCesarCipherText ? 'да' : 'нет');

let plainTextAlphabet = alphabet.alphabet(plainText);
let PortaCipherTextAlphabet = alphabet.alphabet(codedPortaCipherText);
let KeywordCesarCipherTextAlphabet = alphabet.alphabet(codedKeywordCesarCipherText);

// alphabet.saveAlphabetToExcel([plainTextAlphabet, PortaCipherTextAlphabet, KeywordCesarCipherTextAlphabet], 'report.xlsx');