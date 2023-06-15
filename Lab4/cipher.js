codeRussianPortaCipher = plaintext => {
    let alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя';
    if (plaintext !== (plaintext = [...plaintext.toLowerCase()].filter(value => value.match(`[${alphabet}]`))).join(''))
        throw 'Wrong plaintext';
    let map = new Map();
    for (let i = 0; i < alphabet.length; i++) {
        for (let j = 0; j < alphabet.length; j++) {
            let code = `${i * alphabet.length + j + 1}`;
            for (let k = code.length; k < 3; k++) {
                code = `0${code}`;
            }
            map.set(`${alphabet[i]}${alphabet[j]}`, code);
        }
    }
    if (plaintext.length % 2 === 1)
        plaintext.push(alphabet[0]);
    let ciphertext = '';
    for (let i = 0; i < plaintext.length; i += 2) {
        ciphertext += `${map.get(`${plaintext[i]}${plaintext[i + 1]}`)} `;
    }
    return ciphertext;
}

decodeRussianPortaCipher = ciphertext => {
    let alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя';
    let map = new Map();
    for (let i = 0; i < alphabet.length; i++) {
        for (let j = 0; j < alphabet.length; j++) {
            let code = `${i * alphabet.length + j + 1}`;
            for (let k = code.length; k < 3; k++) {
                code = `0${code}`;
            }
            map.set(code, `${alphabet[i]}${alphabet[j]}`);
        }
    }
    let plaintext = '';
    for (let i = 0, code = ''; i < ciphertext.length; i++) {
        if (ciphertext[i] === ' ') {
            plaintext += map.get(code);
            code = '';
        } else
            code += ciphertext[i];
    }
    return plaintext;
}

codeRussianKeywordCesarCipher = (plaintext, keyword) => {
    let alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя';
    if (plaintext !== (plaintext = [...plaintext.toLowerCase()].filter(value => value.match(`[${alphabet}]`))).join(''))
        throw 'Wrong plaintext';
    if (keyword !== (keyword = [...keyword.toLowerCase()].filter((value, index, array) =>
        value.match(`[${alphabet}]`) && array.indexOf(value) === index)).join(''))
        throw 'Wrong keyword';
    let map = new Map();
    for (let i = 0, j = 0; i < alphabet.length;) {
        if (i < keyword.length)
            map.set(alphabet[i], keyword[i++]);
        else {
            if (![...map.values()].includes(alphabet[j]))
                map.set(alphabet[i++], alphabet[j]);
            j++;
        }
    }
    return [...plaintext].map(value => map.get(value)).join('');
}

decodeRussianKeywordCesarCipher = (ciphertext, keyword) => {
    let alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя';
    if (keyword !== (keyword = [...keyword.toLowerCase()].filter((value, index, array) =>
        value.match(`[${alphabet}]`) && array.indexOf(value) === index)).join(''))
        throw 'Wrong keyword';
    let map = new Map();
    for (let i = 0, j = 0; i < alphabet.length;) {
        if (i < keyword.length)
            map.set(keyword[i], alphabet[i++]);
        else {
            if (![...map.keys()].includes(alphabet[j]))
                map.set(alphabet[j], alphabet[i++]);
            j++;
        }
    }
    return [...ciphertext].map(value => map.get(value)).join('');
}

module.exports = {
    codeRussianPortaCipher,
    decodeRussianPortaCipher,
    codeRussianKeywordCesarCipher,
    decodeRussianKeywordCesarCipher
}