import bisect

def power(x, y, m = None):
    if y < 0 or (m and m < 1):
        raise ValueError
    v = 1
    while y:
        if y & 1:
            v = v * x if not m else (v * x) % m
        y >>= 1
        x = x * x if not m else (x * x) % m
    return v

def MillerRabin(n):
    if MillerRabin.maxn <= n:
        raise ValueError
    if n <= 1:
        return False
    a = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    m = n - 1
    s = 0
    while m & (1 << s) == 0:
        s += 1
    for i in a:
        if n <= i:
            break
        if power(i, m >> s, n) == 1:
            continue
        for j in xrange(1, s + 1):
            if power(i, m >> j, n) == m:
                break
        else:
            return False
    return True

MillerRabin.maxn = 3825123056546413051

def prange(*args):
    if len(args) == 0:
        s, e = 0, -1
    elif len(args) == 1:
        s, e = 0, args[0]
    elif len(args) == 2:
        s, e = args[0], args[1]
    else:
        raise TypeError
    i = bisect.bisect_left(prange.primes, s)
    while i < len(prange.primes) and (prange.primes[i] < e or e < 0):
        yield prange.primes[i]
        i += 1
    while prange.last < MillerRabin.maxn and (prange.last < e or e < 0):
        if MillerRabin(prange.last):
            prange.primes.append(prange.last)
            if s <= prange.last:
                yield prange.last
        prange.last += 1
    while prange.last < e or e < 0:
        i = 0
        while i < len(prange.primes) and power(prange.primes[i], 2) <= prange.last:
            if prange.last % prange.primes[i] == 0:
                break
            i += 1
        else:
            prange.primes.append(prange.last)
            if s <= prange.last:
                yield prange.last
        prange.last += 1

prange.last = 2
prange.primes = []

def prime(n):
    if n < prange.last:
        i = bisect.bisect_left(prange.primes, n)
        return prange.primes[i] == n
    elif n < MillerRabin.maxn:
        return MillerRabin(n)
    else:
        return bool(list(prange(n, n + 1)))

def gcd(a, b):
    while a:
        a, b = b % a, a
    return b

def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    return b, x, y

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    return x % m

def ChineseRemainderTheorem(q, r):
    m = zip(q, r)
    n = len(m)
    for i in xrange(n):
        if m[i][1] <= 0:
            raise ValueError
        for j in xrange(i):
            g = gcd(m[i][1], m[j][1])
            x, y = m[i][1] / g, m[j][1] / g
            m[i] = (m[i][0] % x, x)
            m[j] = (m[j][0] % y, y)
    c = 1
    for i in xrange(n):
        c *= m[i][1]
    x = 0
    for q, r in m:
        a = q * modinv(c / r, r)
        x += a * (c / r)
    return x % c