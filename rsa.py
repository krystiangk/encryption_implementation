import random


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x-u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcdf = b
    return gcdf, x, y


def modular_inverse(a, b):
    gcdf, x, y = egcd(a, b)

    if x < 0:
        x += b
    return x


def get_p_q():
    rand1, rand2 = random.sample(range(100, 1000), 2)

    with open('prime_numbers.txt', 'r') as f:
        all_lines = f.readlines()
        p = int(all_lines[rand1])
        q = int(all_lines[rand2])

    return p, q


def generate_key_pair(p, q):
    n = p * q
    phi = (p-1) * (q-1)
    e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = modular_inverse(e, phi)

    return ((e, n), (d, n))


def encrypt(public_key, message):
    e, n = public_key
    encr_msg = [pow(ord(i), e, n) for i in message]
    return encr_msg


def decrypt(private_key, encr_msg):
    d, n = private_key
    tempf = [str(pow(i, d, n)) for i in encr_msg]
    decr_msg = [chr(int(i)) for i in tempf]
    return ''.join(decr_msg)


def key_generation():
    p, q = get_p_q()
    public, private = generate_key_pair(p, q)
    return public, private



