# -*- coding: utf-8 -*-
"""KI-DES-Implementation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ov7VzmE2MNlalkezHBguJDN_D93JkcoA
"""

import numpy as np
import secrets

IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

FP = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]

EBox = [32,1,2,3,4,5,
            4,5,6,7,8,9,
            8,9,10,11,12,13,
            12,13,14,15,16,17,
            16,17,18,19,20,21,
            20,21,22,23,24,25,
            24,25,26,27,28,29,
            28,29,30,31,32,1]

SBox =[
		# S1
		[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
		 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
		 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
		 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

		# S2
		[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
		 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
		 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
		 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

		# S3
		[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
		 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
		 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
		 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

		# S4
		[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
		 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
		 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
		 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

		# S5
		[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
		 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
		 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
		 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

		# S6
		[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
		 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
		 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
		 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

		# S7
		[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
		 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
		 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
		 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

		# S8
		[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
		 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
		 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
		 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
	]

F_PBox = [16, 7, 20, 21, 29, 12, 28, 17,
              1, 15, 23, 26, 5, 18, 31, 10,
              2, 8, 24, 14, 32, 27, 3, 9,
              19, 13, 30, 6, 22, 11, 4, 25 ]

key_PBox = [14,    17,   11,    24,     1,    5,
                  3,    28,   15,     6,    21,   10,
                 23,    19,   12,     4,    26,    8,
                 16,     7,   27,    20,    13,    2,
                 41,    52,   31,    37,    47,   55,
                 30,    40,   51,    45,    33,   48,
                 44,    49,   39,    56,    34,  53,
                 46,    42,   50,    36,    29,   32]
# Fungsi untuk melakukan XOR
def xor(left, xorstream):
    xorresult = np.logical_xor(left, xorstream)
    return xorresult.astype(int)

# Fungsi EBox untuk ekspansi
def E_box(right):
    expanded = np.empty(48)
    j = 0
    for i in EBox:
        expanded[j] = right[i - 1]
        j += 1
    expanded = list(map(int, expanded))
    return np.array(expanded)

# Fungsi lookup SBox
def sboxloopup(sinput, x):
    tableno = x - 1
    row = int((np.array2string(sinput[0]) + np.array2string(sinput[5])), 2)
    column = int(np.array2string(sinput[1:5])[1:8].replace(" ", ""), 2)
    elementno = (16 * row) + column
    soutput = SBox[tableno][elementno]
    return np.array(list(map(int, np.binary_repr(soutput, width=4))))

# Fungsi SBox
def sbox(sboxin):
    return np.concatenate([sboxloopup(sboxin[i:i+6], i//6 + 1) for i in range(0, 48, 6)])

# Permutasi
def f_permute(topermute):
    permuted = np.empty(32)
    for j, i in enumerate(F_PBox):
        permuted[j] = topermute[i - 1]
    return permuted

# Fungsi f pada DES
def f_function(right, rkey):
    expanded = E_box(right)
    xored = xor(expanded, rkey)
    sboxed = sbox(xored)
    return f_permute(sboxed)

# Fungsi round DES
def round(data, rkey):
    l0, r0 = data[:32], data[32:]
    r1 = xor(l0, f_function(r0, rkey))
    return np.concatenate([r0, r1])

# Permutasi awal dan final
def permutation(data, initial=True):
    table = IP if initial else FP
    return np.array([data[i-1] for i in table])

def keyshift(toshift, n):
    return np.roll(toshift, -1 if n in [1, 2, 9, 16] else -2)

def keypermute(key16):
    return np.array([[key[i - 1] for i in key_PBox] for key in key16])

def keyschedule(key):
    left, right = key[:28], key[28:]
    key16 = np.zeros((16, 56), dtype=int)
    for i in range(1, 17):
        left, right = keyshift(left, i), keyshift(right, i)
        key16[i-1] = np.concatenate([left, right])
    return keypermute(key16)

def generate_hex_key():
    return secrets.token_hex(8)

# Fungsi untuk mengkonversi teks ke bit (dengan padding)
def text_to_bits(text):
    # Convert text to bits and pad to make sure it's a multiple of 64 bits
    text_bits = np.array(list(map(int, bin(int.from_bytes(text.encode(), 'big'))[2:].zfill(64))))
    while len(text_bits) % 64 != 0:
        text_bits = np.append(text_bits, 0)
    return text_bits

# Fungsi untuk mengkonversi bit ke teks (menghapus padding)
def bits_to_text(bits):
    # Join the bits to form a binary string
    bits_str = ''.join(map(str, bits))
    # Convert binary string back to integer
    n = int(bits_str, 2)
    try:
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8')
    except UnicodeDecodeError:
        return "[Decrypted non-UTF-8 data]"

# mengkonversi bit ke hexadecimal
def bits_to_hex(bits):
    n = int(''.join(map(str, bits)), 2)
    return hex(n)[2:].zfill(16)  

def userinput():
    text = input("Enter the text to encrypt: ")
    keyinp = generate_hex_key()
    print(f"Generated Key: {keyinp}")
    keyinp_bin = bin(int(keyinp, 16))[2:].zfill(64)[:56]
    keyinp_bin = list(map(int, keyinp_bin))
    data_bits = text_to_bits(text)
    print(f"Text in bits: {data_bits}")
    return keyinp_bin, data_bits

def main():
    key, data_bits = userinput()
    key16 = keyschedule(key)
    encrypted = permutation(data_bits, initial=True)

    for i in range(16):
        encrypted = round(encrypted, key16[i])

    encrypted = permutation(encrypted, initial=False)
    print(f"Encrypted bits: {encrypted}")
    print(f"Cipher text: {bits_to_hex(encrypted)}")

    decrypted = permutation(encrypted, initial=True)
    for i in reversed(range(16)):
        decrypted = round(decrypted, key16[i])

    decrypted = permutation(decrypted, initial=False)
    print(f"Decrypted bits: {decrypted}")
    print(f"Decrypted text: {bits_to_text(decrypted)}")

if __name__ == "__main__":
    main()
