const cipher = require('./cipher.js');
const alphabet = require('./alphabet.js');
const fs = require('fs');

let plainText = fs.readFileSync('./plainText.txt').toString();

let start = new Date();
let codedRoutePermutationCipherText = cipher.codeRoutePermutationCipher(plainText);
console.log('Время выполнения зашифрования (шифр маршрутной перестановки):', new Date() - start);
start = new Date();
let decodedRoutePermutationCipherText = cipher.decodeRoutePermutationCipher(codedRoutePermutationCipherText);
console.log('Время выполнения расшифрования (шифр маршрутной перестановки):', new Date() - start);
console.log('Расшифрованный текст совпадает с исходным (шифр маршрутной перестановки):', plainText.trimEnd() === decodedRoutePermutationCipherText.trimEnd() ? 'да' : 'нет');

start = new Date();
let codedMultiplePermutationCipherText = cipher.codeMultiplePermutation(plainText, 'кирилл', 'лысков');
console.log('Время выполнения зашифрования (шифр множественной перестановки):', new Date() - start);
start = new Date();
let decodedMultiplePermutationCipherText = cipher.decodeMultiplePermutation(codedMultiplePermutationCipherText, 'кирилл', 'лысков');
console.log('Время выполнения расшифрования (шифр множественной перестановки):', new Date() - start);
console.log('Расшифрованный текст совпадает с исходным (шифр множественной перестановки):', plainText.trimEnd() === decodedMultiplePermutationCipherText.trimEnd() ? 'да' : 'нет');

let plainTextAlphabet = alphabet.alphabet(plainText);
let RoutePermutationCipherTextAlphabet = alphabet.alphabet(codedRoutePermutationCipherText);
let MultiplePermutationCipherTextAlphabet = alphabet.alphabet(codedMultiplePermutationCipherText);

// alphabet.saveAlphabetToExcel([plainTextAlphabet, RoutePermutationCipherTextAlphabet, MultiplePermutationCipherTextAlphabet], 'report.xlsx');