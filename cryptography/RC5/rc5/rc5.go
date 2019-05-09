package rc5

import (
	"encoding/binary"
	// "fmt"
	"math/bits"
)

const (
	w   = 32          // The length of a word in bits, typically 16, 32 or 64.
	r   = 12          // The number of rounds to use when encrypting data.
	b   = 16          // The length of the key in bytes.
	c   = 4           // number words in key = ceil(8*b/w)
	t   = 2 * (r + 1) // The number of round subkeys required.
	P_w = 0xb7e15163  // First Magic constant
	Q_w = 0x9e3779b9  // Second Magic constant
)

type cipher32 struct {
	S      [t]uint32 //The round subkey words that used in each round
	Mode   int       // indicate mode of cipher
	Vector uint64    // used to store the Vector used next block
}

func RC5_SETUP(key []byte, iv []byte, mode string) (cipher32, bool) {
	// Check if the length of key in bytes equal to 16
	if len(key) != b {
		return cipher32{}, false
	}

	// Converts the b-byte key into a sequence of words stored in the array L.
	var L [w / 8]uint32
	for i := 0; i < w/8; i++ {
		L[i] = binary.LittleEndian.Uint32(key[:w/8]) // Copy the each word with little-endian
		key = key[w/8:]
	}

	// Initializing sub-key S with magic constant P_w and Q_w
	var S [t]uint32
	S[0] = P_w
	for i := uint(1); i < t; i++ {
		S[i] = S[i-1] + Q_w
	}

	var A uint32
	var B uint32
	var i, j int
	// Mixing the secret key, K, into the expanded key, S.
	for k := 0; k < 3*t; k++ {
		S[i] = bits.RotateLeft32(S[i]+(A+B), 3)
		A = S[i]
		L[j] = bits.RotateLeft32(L[j]+(A+B), int(A+B))
		B = L[j]
		i = (i + 1) % t
		j = (j + 1) % c
	}
	if mode == "CBC" {
		return cipher32{S, 1, binary.BigEndian.Uint64(iv)}, true
	}
	return cipher32{S, 0, 0}, true
}

func (C *cipher32) RC5_ENCRYPT(pt, ct []byte) {
	var ptTemp = make([]byte, len(pt))
	copy(ptTemp, pt)
	if C.Mode == 1 {
		ptNum := binary.BigEndian.Uint64(ptTemp) ^ C.Vector
		binary.BigEndian.PutUint64(ptTemp, ptNum)
	}
	// First converts input bytes into two unsigned integers in word size 32 called A and B
	// Read A and B in byte-reverse order then added with S[0] and S[1]
	A := binary.LittleEndian.Uint32(ptTemp[:w/8]) + C.S[0]
	B := binary.LittleEndian.Uint32(ptTemp[w/8:]) + C.S[1]
	for i := 1; i <= r; i++ {
		// A = ((A XOR B) <<< B) + S[2*i]
		A = bits.RotateLeft32(A^B, int(B)) + C.S[2*i]
		// A = ((B XOR A) <<< A) + S[2*i+1]
		B = bits.RotateLeft32(B^A, int(A)) + C.S[2*i+1]
	}
	// Write A and B in byte-reverse order
	binary.LittleEndian.PutUint32(ct[:w/8], A)
	binary.LittleEndian.PutUint32(ct[w/8:], B)
	if C.Mode == 1 {
		C.Vector = binary.BigEndian.Uint64(ct[:])
	}
}

func (C *cipher32) RC5_DECRYPT(ct, pt []byte) {
	// First converts input bytes into two unsigned integers in word size 32 called A and B
	// Read A and B in byte-reverse order
	A := binary.LittleEndian.Uint32(ct[:w/8])
	B := binary.LittleEndian.Uint32(ct[w/8:])
	for i := r; i > 0; i-- {
		// B = ((B - C.S[2*i+1]) >>> A) XOR A
		B = bits.RotateLeft32(B-C.S[2*i+1], -int(A)) ^ A
		// A = ((A - C.S[2*i]) >>> B) XOR B
		A = bits.RotateLeft32(A-C.S[2*i], -int(B)) ^ B
	}
	// Write A-S[0] and B-S[1] in byte-reverse order
	binary.LittleEndian.PutUint32(pt[w/8:], B-C.S[1])
	binary.LittleEndian.PutUint32(pt[:w/8], A-C.S[0])
	if C.Mode == 1 {
		ptNum := binary.BigEndian.Uint64(pt[:]) ^ C.Vector
		binary.BigEndian.PutUint64(pt, ptNum)
		C.Vector = binary.BigEndian.Uint64(ct[:])
	}
}
