  
import sys
sys.path.append("../..")
import random
from algorithms.bitarray import bitarray
from algorithms.exgcd import inverse
from algorithms.sm2 import SM2

class SM2_DSA(SM2):
    def __init__(self):
        super().__init__()
    
    def _identity(self, uid:bitarray, PK) -> bitarray:
        entlen = bitarray(len(uid), 16)
        a = self._bytes2bits(self._elem2bytes(self._G.a))
        b = self._bytes2bits(self._elem2bytes(self._G.b))
        gx = self._bytes2bits(self._elem2bytes(self._G.x))
        gy = self._bytes2bits(self._elem2bytes(self._G.y))
        ax = self._bytes2bits(self._elem2bytes(PK.x))
        ay = self._bytes2bits(self._elem2bytes(PK.y))
        return self._hash(bitarray.concat((entlen, uid, a, b, gx, gy, ax, ay)))[:256]
    
    def sign(self, M:bytes, uid:bytes, SK:int) -> tuple:
        M, uid = self._bytes2bits(M), self._bytes2bits(uid)
        PK = SK * self._G
        Z = self._identity(uid, PK)
        M = bitarray.concat((Z, M))
        e = self._bytes2int(self._bits2bytes(self._hash(M)))
        while True:
            k = random.randint(1, self._n-1)
            P = k * self._G
            x1 = self._elem2int(P.x)
            r = (e + x1) % self._n
            if r == 0 or r+k == self._n:
                continue
            s = (inverse(1+SK, self._n) * (k-r*SK)) % self._n
            if s != 0:
                break
        r, s = self._int2bytes(r, self._byteLen), self._int2bytes(s, self._byteLen)
        return (r, s)
    
    def verify(self, M:bytes, sign:tuple, uid:bytes, PK):
        r, s = sign
        r, s = self._bytes2int(r), self._bytes2int(s)
        assert 1 <= r <= self._n-1 and 1 <= s <= self._n-1
        M, uid = self._bytes2bits(M), self._bytes2bits(uid)
        Z = self._identity(uid, PK)
        M = bitarray.concat((Z, M))
        e = self._bytes2int(self._bits2bytes(self._hash(M)))
        t = (r + s) % self._n
        assert t != 0
        P = s * self._G + t * PK
        x1 = self._elem2int(P.x)
        R = (e + x1) % self._n
        return R == r
