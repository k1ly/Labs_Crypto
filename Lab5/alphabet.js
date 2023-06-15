let excel = require('excel4node');

alphabet = text => {
    let alphabet = new Map();
    for (const a of text) {
        alphabet.set(a, alphabet.has(a) ? alphabet.get(a) + 1 : 1);
    }
    return alphabet;
}

entropy = (alphabet, p) => {
    let conditional;
    if (p) {
        let q = 1 - p;
        conditional = -p * Math.log2(p) - q * Math.log2(q);
        if (isNaN(conditional))
            return 0;
    }
    let sum = 0;
    let n = Array.from(alphabet.values()).reduce((x, y) => x + y, 0);
    for (const [a, f] of alphabet) {
        let c = f / n;
        sum += c * Math.log2(c);
        sum -= p ? conditional : 0;
    }
    return -sum;
}

saveAlphabetToExcel = (alphabets, filename) => {
    let wb = new excel.Workbook();
    let ws = wb.addWorksheet();
    for (let i = 0; i < alphabets.length; i++) {
        let alphabet = alphabets[i];
        Array.from(alphabet.entries())
            .forEach(([a, q], index) => {
                ws.cell(i * 3 + 1, index + 1).string(a);
                ws.cell(i * 3 + 2, index + 1).number(q);
            })
    }
    wb.write(filename);
}

module.exports = {alphabet, entropy, saveAlphabetToExcel};