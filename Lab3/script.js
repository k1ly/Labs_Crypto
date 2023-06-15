greatestCommonDivider = (a, b) => {
    while (true) {
        let mod = a % b;
        if (mod === 0)
            break;
        a = b;
        b = mod;
    }
    return b;
}

isPrimeNumber = x => {
    for (let i = 2; i < Math.sqrt(x); i++) {
        if (x % i === 0)
            return false;
    }
    return true;
}

findPrimeNumbers = (m, n) => {
    if (m > n || n < 2)
        throw 'Wrong bounds';
    let primeNumbers = [];
    for (let i = 2; i <= n; i++) {
        let isPrime = true;
        for (let primeNumber of primeNumbers) {
            if (i % primeNumber === 0)
                isPrime = false;
        }
        if (isPrime)
            primeNumbers.push(i);
    }
    return primeNumbers.filter(p => p >= m);
}