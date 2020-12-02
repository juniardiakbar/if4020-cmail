import os
import math
import random
import hashlib
import codecs
from algorithms.keccak import SHA3
from algorithms.bitarray import bitarray
from algorithms.residue_field import RF
from algorithms.ecc import ECC

class SM2:
    def __init__(self):
        self._reset_data()
        self._G = ECC(a=self._a, b=self._b, field=self._RF_q, x=self._gx, y=self._gy)
        self._byteLen = math.ceil(math.ceil(math.log2(self._q))/8)
        self._HashFunc = SHA3(512).hash
        self._v = 512
    
    def generate_keys(self) -> tuple:
        d = random.randint(1, self._n-2)
        return (d, d * self._G)
    
    def _reset_data(self):
        self._a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
        self._b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
        self._q = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
        self._n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
        self._gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
        self._gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
        class RF_q(RF):
            def __init__(self, data, modulo=self._q):
                super().__init__(data, modulo)
        self._RF_q = RF_q
    
    def _int2bytes(self, x:int, k:int) -> bytes:
        return x.to_bytes(k, byteorder='big')
    
    def _bytes2int(self, m:bytes) -> int:
        return int.from_bytes(m, byteorder='big')
    
    def _bits2bytes(self, b:bitarray) -> bytes:
        return b.to_bytes()
    
    def _bytes2bits(self, b:bytes) -> bitarray:
        return bitarray.from_bytes(b)
    
    def _elem2bytes(self, e:RF) -> bytes:
        return self._int2bytes(e.data, self._byteLen)
    
    def _bytes2elem(self, s:bytes) -> RF:
        return self._RF_q(self._bytes2int(s))
    
    def _elem2int(self, e:RF) -> int:
        return e.data
    
    def _point2bytes(self, p:ECC, method='uncompressed') -> bytes:
        assert p.isInfty == False
        x1 = self._elem2bytes(p.x)
        if method == 'uncompressed':
            y1 = self._elem2bytes(p.y)
            PC = 0x04
            return bytes([PC]) + x1 + y1
    
    def _bytes2point(self, s:bytes, method='uncompressed') -> ECC:
        PC, x1, y1 = s[0], s[1:1+self._byteLen], s[1+self._byteLen:]
        xp = self._bytes2elem(x1)
        if method == 'uncompressed':
            assert PC == 4
            yp = self._bytes2elem(y1)
        assert self._G.belong(xp, yp)
        return self._G(xp, yp)
    
    def _hash(self, z:bitarray) -> bitarray:
        z = self._bits2bytes(z)
        x = self._HashFunc(codecs.decode(z, 'ISO-8859-1'))
        return self._bytes2bits(bytes(x, 'ISO-8859-1'))
    
    def _kdf(self, z:bitarray, klen:int) -> bitarray:
        ct = bitarray(1, 32)
        t = bitarray()
        for i in range(math.ceil(klen/self._v)):
            t = bitarray.concat((t, self._hash(bitarray.concat((z, ct)))))
            ct = ct + bitarray(1, 32)
        return t[:klen]
