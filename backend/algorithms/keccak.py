rate = {224: 1152, 256: 1088, 384: 832, 512: 576}

rot_vals = [
    [153, 231, 3, 10, 171],
    [55, 276, 36, 300, 6],
    [28, 91, 0, 1, 190],
    [120, 78, 210, 66, 253],
    [21, 136, 105, 45, 15]
]

RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
]

def ascii_to_binary(chars):
    return ''.join('{:08b}'.format(ord(char)) for char in chars)

def binary_to_hex(binary):
    return ''.join('{:0x}'.format(int(binary[i:i+4], 2)) for i in range(0, len(binary), 4))

class SHA3():
    def __init__(self, output=224):
        self.output = output
        assert self.output in rate, 'Invalid bit length'
        self.rate = rate[self.output]
        self.state_value = 1600
        self.capacity = self.state_value - self.rate
        self.bus = self.rate + self.capacity

    def __str__(self):
        return self.output
    
    def init_state(self):
        state_ = []
        for x in range(5):
            tmp_1 = []
            for y in range(5):
                tmp_2 = []
                for z in range(64):
                    tmp_2.append('')
                tmp_1.append(tmp_2)
            state_.append(tmp_1)
        return state_

    def pad_with(self, x, m):
        assert x > 0 and m >= 0
        j = (-m - 2) % x
        pad = '1' + ('0' * j) + '1'
        return pad

    def preprocess(self, message):
        message = ascii_to_binary(message)
        padded_message = message + self.pad_with(self.rate, len(message))
        message_blocks = []
        for i in range(0, len(padded_message), self.rate):
            message_blocks.append(padded_message[i : i + self.rate])
        return message_blocks

    def change_conventions(self, state):
        state_ = self.init_state()
        for x in range(2, 7):
            for y in range(2, 7):
                state_[x-2][y-2] = list(self.lane(state, x%5, y%5))
        return state_

    def theta(self, state):
        def C(x, z):
            return self.xor(*[state[x][i][z] for i in range(5)])

        def D(x, z):
            val_1 =  C((x-1) % 5, z)
            val_2 = C((x+1) % 5, (z-1) % 64)
            return self.xor_2(val_1, val_2)

        state_ = self.init_state()
        for x in range(5):
            for y in range(5):
                for z in range(64):
                    state_[x][y][z] = self.xor_2(state[x][y][z], D(x, z))
        return state_

    def rot(self, word, shift):
        shift = shift % len(word)
        return word[-shift:]+word[:-shift]

    def rho(self, state):
        state_ = self.init_state()
        for x in range(5):
            for y in range(5):
                state_[y][((2*x) + (3*y)) %5] = list(self.rot(self.lane(state, x, y), rot_vals[(y+2)%5][(x+2)%5]%64))
        return state_

    def pi(self, state):
        state_ = self.init_state()
        for x in range(5):
            for y in range(5):
                for z in range(64):
                    state_[x][y][z] = state[(x+(3*y))%5][x][z]
        return state_

    def chi(self, state):
        state_ = self.init_state()
        for x in range(5):
            for y in range(5):
                state_[x][y] = list(self.xor_2(self.lane(state, x, y), bin((int(self.lane(state, (x+1)%5, y), 2) ^ 1) & int(self.lane(state, (x+2)%5, y), 2))[2:].zfill(64)))
        return state_

    def iota(self, state):
        state_ = self.init_state()
        for x in range(5):
            for y in range(5):
                state_[x][y] = list(self.xor_2(self.lane(state, x, y), bin(RC[self.round_count])[2:].zfill(64)))
        return state_

    def lane(self, state, x, y):
        lane_ = ''.join(state[x][y])
        assert len(state[x][y]) == 64
        assert len(lane_) == 64, (x, y)
        return lane_

    def plane(self, state, y):
        return ''.join(self.lane(state, i, y) for i in range(5))
        
    def form_state(self, data):
        assert len(data) == 1600
        state = self.init_state()
        for x in range(5):
            for y in range(5):
                for z in range(64):
                    state[x][y][z] = data[64 * ((5 * y) + x) + z]

        assert data == ''.join(self.plane(state, i) for i in range(5))
        return self.change_conventions(state)

    def xor_2(self, a, b):
        return ''.join('0' if i == j else '1' for i, j in zip(a, b))

    def xor(self, *words):
        first, *words = words
        result = first
        for word in words:
            result = self.xor_2(result, word)
        return result

    def _round(self, b):
        b = self.theta(b)
        b = self.rho(b)
        b = self.pi(b)
        b = self.chi(b)
        b = self.iota(b)
        return b

    def f(self, r, c):
        b = r + c
        assert len(b) == 1600
        state = self.form_state(b)
        self.rounds = 24
        for i in range(self.rounds):
            self.round_count = i
            state = self._round(state)
        unpacked_state = ''.join(self.plane(state, i) for i in range(5))
        return unpacked_state[0:self.rate], unpacked_state[self.rate:]

    def hash(self, message):
        message = self.preprocess(message)
        r = '0' * self.rate
        c = '0' * self.capacity
        
        for block in message:
            f_inp = self.xor_2(block, r)
            r, c = self.f(f_inp, c)

        value = r[0:self.output]
        return binary_to_hex(value)

if (__name__=="__main__"):
    hash_this = 'Hello'

    sha = SHA3(224)
    hashed = sha.hash(hash_this)
    print(sha.__str__(), hashed)

    sha = SHA3(256)
    hashed = sha.hash(hash_this)
    print(sha.__str__(), hashed)

    sha = SHA3(384)
    hashed = sha.hash(hash_this)
    print(sha.__str__(), hashed)

    sha = SHA3(512)
    hashed = sha.hash(hash_this)
    print(sha.__str__(), hashed)