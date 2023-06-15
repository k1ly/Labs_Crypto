codeRoutePermutationCipher = plaintext => {
    let width = Math.ceil(Math.sqrt(plaintext.length));
    let height = Math.round(Math.sqrt(plaintext.length));
    let matrix = [];
    for (let i = 0; i < height; i++) {
        matrix.push([]);
        for (let j = 0; j < width; j++) {
            matrix[i][j] = i * width + j < plaintext.length ? plaintext[i * width + j] : ' ';
        }
    }
    let ciphertext = '';
    for (let i = 0, x = 0, y = 0, round = 0, direction = 'down'; i < width * height; i++) {
        ciphertext += matrix[y][x];
        switch (direction) {
            case 'down':
                if (y + 1 === height - round) {
                    direction = 'right';
                    x++;
                } else
                    y++;
                break;
            case 'right':
                if (x + 1 === width - round) {
                    direction = 'up';
                    y--;
                } else
                    x++;
                break;
            case 'up':
                if (y === round) {
                    direction = 'left';
                    x--;
                } else
                    y--;
                break;
            case 'left':
                if (x - 1 === round) {
                    direction = 'down';
                    y++;
                    round++;
                } else
                    x--;
                break;
        }
    }
    return ciphertext;
}

decodeRoutePermutationCipher = ciphertext => {
    let width = Math.ceil(Math.sqrt(ciphertext.length));
    let height = Math.round(Math.sqrt(ciphertext.length));
    let matrix = [];
    for (let i = 0; i < height; i++) {
        matrix.push([]);
    }
    for (let i = 0, x = 0, y = 0, round = 0, direction = 'down'; i < ciphertext.length; i++) {
        matrix[y][x] = ciphertext[i];
        switch (direction) {
            case 'down':
                if (y + 1 === height - round) {
                    direction = 'right';
                    x++;
                } else
                    y++;
                break;
            case 'right':
                if (x + 1 === width - round) {
                    direction = 'up';
                    y--;
                } else
                    x++;
                break;
            case 'up':
                if (y === round) {
                    direction = 'left';
                    x--;
                } else
                    y--;
                break;
            case 'left':
                if (x - 1 === round) {
                    direction = 'down';
                    y++;
                    round++;
                } else
                    x--;
                break;
        }
    }
    let plaintext = '';
    for (let i = 0; i < height; i++) {
        for (let j = 0; j < width; j++) {
            plaintext += matrix[i][j];
        }
    }
    return plaintext;
}
// encrypt
// decrypt
codeMultiplePermutation = (plaintext, keyword1, keyword2) => {
    let ciphertext = '';
    for (let chunk = 0; chunk < plaintext.length / (keyword1.length * keyword2.length); chunk++) {
        let matrix = [];
        for (let i = 0; i < keyword2.length; i++) {
            matrix.push([]);
            for (let j = 0; j < keyword1.length; j++) {
                matrix[i][j] = i * keyword1.length + j < Math.min((keyword1.length * keyword2.length), plaintext.length - chunk * keyword1.length * keyword2.length) ?
                    plaintext[chunk * keyword1.length * keyword2.length + i * keyword1.length + j] : ' ';
            }
        }
        matrix = [...keyword2].map((value, index) => ({index: index, letter: value}))
            .sort((a, b) => a.letter === b.letter ? 0 : (a.letter < b.letter ? -1 : 1))
            .map((value, index) => ({index: value.index, array: matrix[index]}))
            .sort((a, b) => a.index === b.index ? 0 : (a.index < b.index ? -1 : 1))
            .map(value => value.array);
        matrix = [...keyword1].map((value, index) => ({index: index, letter: value}))
            .sort((a, b) => a.letter === b.letter ? 0 : (a.letter < b.letter ? -1 : 1))
            .map((value, index) => ({index: value.index, array: matrix.map(row => row[index])}))
            .sort((a, b) => a.index === b.index ? 0 : (a.index < b.index ? -1 : 1))
            .map(value => value.array);
        for (let i = 0; i < keyword2.length; i++) {
            for (let j = 0; j < keyword1.length; j++) {
                ciphertext += matrix[i][j];
            }
        }
    }
    return ciphertext;
}

decodeMultiplePermutation = (ciphertext, keyword1, keyword2) => {
    let plaintext = '';
    for (let chunk = 0; chunk < ciphertext.length / (keyword1.length * keyword2.length); chunk++) {
        let matrix = [];
        for (let i = 0; i < keyword2.length; i++) {
            matrix.push([]);
            for (let j = 0; j < keyword1.length; j++) {
                matrix[i][j] = ciphertext[chunk * keyword1.length * keyword2.length + i * keyword1.length + j]
            }
        }
        matrix = [...keyword1].map((value, index) => ({letter: value, index: index}))
            .map((value, index) => ({letter: value.letter, array: matrix[index]}))
            .sort((a, b) => a.letter === b.letter ? 0 : (a.letter < b.letter ? -1 : 1))
            .map(value => value.array);
        matrix = [...keyword2].map((value, index) => ({letter: value, index: index}))
            .map((value, index) => ({letter: value.letter, array: matrix.map(row => row[index])}))
            .sort((a, b) => a.letter === b.letter ? 0 : (a.letter < b.letter ? -1 : 1))
            .map(value => value.array);
        for (let i = 0; i < keyword2.length; i++) {
            for (let j = 0; j < keyword1.length; j++) {
                plaintext += matrix[i][j];
            }
        }
    }
    return plaintext;
}

module.exports = {
    codeRoutePermutationCipher,
    decodeRoutePermutationCipher,
    codeMultiplePermutation,
    decodeMultiplePermutation
}