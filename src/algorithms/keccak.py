import functools
import codecs
from copy import deepcopy
from math import log
from operator import xor

# --------------------------------- Constant --------------------------------- #
ROTATIONCONSTANTS = [
  [  0,  1, 62, 28, 27, ],
  [ 36, 44,  6, 55, 20, ],
  [  3, 10, 43, 25, 39, ],
  [ 41, 45, 15, 21,  8, ],
  [ 18,  2, 61, 56, 14, ]
]

ROUNDCONSTANTS = [
  0x0000000000000001,   0x0000000000008082,   0x800000000000808A,   0x8000000080008000,
  0x000000000000808B,   0x0000000080000001,   0x8000000080008081,   0x8000000000008009,
  0x000000000000008A,   0x0000000000000088,   0x0000000080008009,   0x000000008000000A,
  0x000000008000808B,   0x800000000000008B,   0x8000000000008089,   0x8000000000008003,
  0x8000000000008002,   0x8000000000000080,   0x000000000000800A,   0x800000008000000A,
  0x8000000080008081,   0x8000000000008080,   0x0000000080000001,   0x8000000080008008
]

MASKCONSTANTS = [(1 << i) - 1 for i in range(65)]
# ------------------------------ END OF CONSTANT ----------------------------- #

# ------------------------------ HELPER FUNCTION ----------------------------- #
def bits_to_bytes(x):
    return (int(x) + 7) // 8

def rotate_left(val, left, bits):
    first_part = val >> (bits - left)
    second_part = (val & MASKCONSTANTS[bits - left]) << left
    return first_part | second_part

def rotate_right(val, right, bits):
    bits -= right
    first_part = val >> right;
    second_part = (val & MASKCONSTANTS[right]) << bits
    return first_part | second_part

def multirate_padding(used_bytes, align_bytes):
    diff = align_bytes - used_bytes
    if (diff == 0):
        diff = align_bytes
    return [0x81] if (diff == 1) else [0x01] + ([0x00] * (diff - 2)) + [0x80]

def keccak_f(state):
    def round(A, RC):
        W, H = state.W, state.H
        range_W, range_H = state.range_W, state.range_H
        lane_w = state.lane_w
        zero = state.zero
    
        C = [functools.reduce(xor, A[x]) for x in range_W]
        D = [0] * W
        for x in range_W:
            D[x] = C[(x - 1) % W] ^ rotate_left(C[(x + 1) % W], 1, lane_w)
            for y in range_H:
                A[x][y] ^= D[x]
        
        B = zero()
        for x in range_W:
            for y in range_H:
                B[y % W][(2 * x + 3 * y) % H] = rotate_left(A[x][y], ROTATIONCONSTANTS[y][x], lane_w)
                
        for x in range_W:
            for y in range_H:
                A[x][y] = B[x][y] ^ ((~ B[(x + 1) % W][y]) & B[(x + 2) % W][y])
        
        A[0][0] ^= RC

    l = int(log(state.lane_w, 2))
    nr = 12 + 2 * l
    
    for ir in range(nr):
        round(state.s, ROUNDCONSTANTS[ir])

# -------------------------- END OF HELPER FUNCTION -------------------------- #

class KeccakState(object):
    W = 5
    H = 5
    range_W = range(W)
    range_H = range(H)

    @staticmethod
    def zero():
        return [[0] * KeccakState.W for row in KeccakState.range_H]
    
    @staticmethod
    def format(st):
        rows = []
        def fmt(x): return '%016x' % x
        for y in KeccakState.range_H:
            row = []
            for x in range_W:
                row.append(fmt(st[x][y]))
            rows.append(' '.join(row))
        return '\n'.join(rows)
    
    @staticmethod
    def lane_to_bytes(s, w):
        o = [((s >> b) & 0xff) for b in range(0, w, 8)]
        return o
    
    @staticmethod
    def bytes_to_lane(bytes):
        r = 0
        for byte in reversed(bytes):
            r = (r << 8) | byte
        return r
    
    @staticmethod
    def bytes_to_string(bytes):
        return ''.join(map(chr, bytes))
    
    @staticmethod
    def string_to_bytes(string):
        return map(ord, string)
    
    def __init__(self, bitrate, b):
        self.bitrate = bitrate
        self.b = b

        assert self.bitrate % 8 == 0
        self.bitrate_bytes = bits_to_bytes(self.bitrate)
        
        assert self.b % 25 == 0
        self.lane_w = self.b // 25

        self.s = KeccakState.zero()
    
    def __str__(self):
        return KeccakState.format(self.s)
    
    def absorb(self, bb):
        assert len(bb) == self.bitrate_bytes
        
        bb += [0] * bits_to_bytes(self.b - self.bitrate)
        i = 0

        for y in self.range_H:
            for x in self.range_W:
                self.s[x][y] ^= KeccakState.bytes_to_lane(bb[i : i + 8])
                i += 8
    
    def squeeze(self):
        return self.get_bytes()[:self.bitrate_bytes]
    
    def get_bytes(self):
        out = [0] * bits_to_bytes(self.b)
        i = 0
        for y in self.range_H:
            for x in self.range_W:
                v = KeccakState.lane_to_bytes(self.s[x][y], self.lane_w)
                out[i:i+8] = v
                i += 8
        return out
    
    def set_bytes(self, bb):
        i = 0
        for y in self.range_H:
            for x in self.range_W:
                self.s[x][y] = KeccakState.bytes_to_lane(bb[i:i+8])
                i += 8

class KeccakSponge(object):
    def __init__(self, bitrate, width, padfn, permfn):
        self.state = KeccakState(bitrate, width)
        self.padfn = padfn
        self.permfn = permfn
        self.buffer = []
    
    def copy(self):
        return deepcopy(self)

    def absorb_block(self, bb):
        assert len(bb) == self.state.bitrate_bytes
        self.state.absorb(bb)
        self.permfn(self.state)
    
    def absorb(self, s):
        self.buffer += KeccakState.string_to_bytes(s)

        while len(self.buffer) >= self.state.bitrate_bytes:
            self.absorb_block(self.buffer[:self.state.bitrate_bytes])
            self.buffer = self.buffer[self.state.bitrate_bytes]

    def absorb_final(self):
        padded = self.buffer + self.padfn(len(self.buffer), self.state.bitrate_bytes)
        self.absorb_block(padded)
        self.buffer = []
    
    def squeeze_once(self):
        rc = self.state.squeeze()
        self.permfn(self.state)
        return rc
    
    def squeeze(self, l):
        Z = self.squeeze_once()
        while len(Z) < l:
            Z += self.squeeze_once()
        return Z[:l]

class KeccakHash(object):
    def __init__(self, bitrate_bits, capacity_bits, output_bits):
        assert bitrate_bits + capacity_bits in (25, 50, 100, 200, 400, 800, 1600)
        self.sponge = KeccakSponge(
            bitrate_bits, bitrate_bits + capacity_bits,
            multirate_padding,
            keccak_f
        )
        
        assert output_bits % 8 == 0
        self.digest_size = bits_to_bytes(output_bits)
        self.block_size = bits_to_bytes(bitrate_bits)
    
    def __repr__(self):
        inf = (
            self.sponge.state.bitrate,
            self.sponge.state.b - self.sponge.state.bitrate,
            self.digest_size * 8
        )
        return '<KeccakHash with r=%d, c=%d, image=%d>' % inf
    
    def copy(self):
        return deepcopy(self)
    
    def update(self, s):
        self.sponge.absorb(s)
    
    def digest(self):
        finalised = self.sponge.copy()
        finalised.absorb_final()
        digest = finalised.squeeze(self.digest_size)
        return KeccakState.bytes_to_string(digest)
    
    def hexdigest(self):
        return codecs.encode(self.digest().encode('utf-8'),'hex_codec')
    
    @staticmethod
    def preset(bitrate_bits, capacity_bits, output_bits):
        def create(initial_input = None):
            h = KeccakHash(bitrate_bits, capacity_bits, output_bits)
            if initial_input is not None:
                h.update(initial_input)
            return h
        return create

# SHA3 parameter presets
Keccak224 = KeccakHash.preset(1152, 448, 224)
Keccak256 = KeccakHash.preset(1088, 512, 256)
Keccak384 = KeccakHash.preset(832, 768, 384)
Keccak512 = KeccakHash.preset(576, 1024, 512)

if __name__=="__main__":
    pt = "test"
    h1 = Keccak224(pt).hexdigest()
    print(h1)