import sys, getopt, hashlib
import random
from math import exp, expm1

ROUNDS = 8
BLOCKSIZE = 8
BLOCKSIZE_BITS = 64
SECRET = "3f788083-77d3-4502-9d71-21319f1792b6"

sb1 = [ 4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3 ]
sb2 = [ 14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9 ]
sb3 = [ 5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11 ]
sb4 = [ 7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3 ]
sb5 = [ 6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2 ]
sb6 = [ 4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14 ]
sb7 = [ 13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12 ]
sb8 = [ 1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12 ]

sb = [ sb1, sb2, sb3, sb4, sb5, sb6, sb7, sb8 ]

def shuffle(message, key):
    random.seed(key)
    l = range(len(message))
    random.shuffle(list(l))
    return [message[x] for x in l]

def unshuffle(shuffled_message, key):
    random.seed(key)
    l = range(len(shuffled_message))
    random.shuffle(list(l))
    out = [None] * len(shuffled_message)
    for i, x in enumerate(l):
        out[x] = shuffled_message[i]
    return out

def encrypt(key, message, mode):
    ciphertext = ""
    n = BLOCKSIZE
    message = [message[i: i + n] for i in range(0, len(message), n)]
    length_of_last_block = len(message[len(message)-1])

    if (length_of_last_block < BLOCKSIZE):
        for i in range(length_of_last_block, BLOCKSIZE):
            message[len(message)-1] += " "

    key = key_256(key)
    key_initial = key
    ctr = 0
    for block in message:
        L = [""] * (ROUNDS + 1)
        R = [""] * (ROUNDS + 1)
        L[0] = block[0:BLOCKSIZE//2]
        R[0] = block[BLOCKSIZE//2:BLOCKSIZE]

        for i in range(1, ROUNDS+1):
            round_key = subkeygen(str(i), key, i)
            lr_im = R[i - 1][:BLOCKSIZE//4]
            rr_im = R[i - 1][BLOCKSIZE//4:]

            ll_i = rr_im
            rl_i = xor(lr_im, scramble(rr_im, i, round_key))

            L[i] = ll_i + rl_i
            R[i] = xor(L[i - 1], scramble(R[i - 1], i, round_key))

        partial_cipher = L[ROUNDS] + R[ROUNDS]
        shuffle(partial_cipher, key)
        ciphertext += partial_cipher
        if (mode == "cbc"):
            key = subkeygen(L[0], key, i)
        if (mode == "counter"):
            key = subkeygen(str(ctr), key_initial, i)
            ctr += 1

    return ciphertext

def decrypt(key, ciphertext, mode):
    message = ""
    n = BLOCKSIZE
    ciphertext = [ciphertext[i: i + n] for i in range(0, len(ciphertext), n)]
    length_of_last_block = len(ciphertext[len(ciphertext)-1])

    if (length_of_last_block < BLOCKSIZE):
        for i in range(length_of_last_block, BLOCKSIZE):
            ciphertext[len(ciphertext)-1] += " "

    key = key_256(key)
    key_initial = key
    ctr = 0
    for block in ciphertext:
        L = [""] * (ROUNDS + 1)
        R = [""] * (ROUNDS + 1)
        L[ROUNDS] = block[0:BLOCKSIZE//2]
        R[ROUNDS] = block[BLOCKSIZE//2:BLOCKSIZE]

        for i in range(ROUNDS, 0, -1):
            round_key = subkeygen(str(i), key, i)
            ll_i = L[i][:BLOCKSIZE//4]
            rl_i = L[i][BLOCKSIZE//4:]

            rr_im = ll_i
            lr_im = xor(rl_i, scramble(rr_im, i, round_key))

            R[i - 1] = lr_im + rr_im
            L[i - 1] = xor(R[i], scramble(R[i - 1], i, round_key))

        partial_message = L[0] + R[0]
        unshuffle(partial_message, key)
        message += partial_message
        if (mode == "cbc"):
            key = subkeygen(L[0], key, i)
        if (mode == "counter"):
            key = subkeygen(str(ctr), key_initial, i)
            ctr += 1

    return message

def key_256(key):
    return hashlib.sha256((key + SECRET).encode("UTF-8")).hexdigest()

def subkeygen(s1, s2, i):
    result = hashlib.sha256((s1 + s2).encode('UTF-8')).hexdigest()
    return result

def scramble(x, i, k):
    k = stobin(k)
    x = stobin(str(x))

    if (len(x) == 32) :
        out = ""
        for i in range(8):
            val = bintoint(x[i*4:(i*4) + 4])
            out += bin(sb[i].index(val))[2:].zfill(4)

        out = out[4:len(out)] + out[0:4]
    else:
        out = x

    k = bintoint(k)
    x = bintoint(out)
    res = pow((x * k), i)
    res = itobin(res)

    return bintostr(res)

def xor(s1, s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

def stobin(s):
    return ''.join('{:08b}'.format(ord(c)) for c in s)

def bintoint(s):
    return int(s, 2)

def itobin(i):
    return bin(i)

def bintostr(b):
    n = int(b, 2)
    return ''.join(chr(int(b[i: i + 8], 2)) for i in range(0, len(b), 8))