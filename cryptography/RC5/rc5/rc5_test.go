package rc5

import (
	"bytes"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math/rand"
	"os"
	"testing"
)

func TestRC5_Random(t *testing.T) {
	random := rand.New(rand.NewSource(99))
	max := 1

	var encrypted [8]byte
	var decrypted [8]byte

	for i := 0; i < max; i++ {
		key := make([]byte, 16)
		random.Read(key)
		value := make([]byte, 8)
		random.Read(value)

		iv := make([]byte, 8)
		random.Read(iv)

		cipher, ok := RC5_SETUP(key, iv, "CBC")
		if ok {
			cipher.RC5_ENCRYPT(value[:], encrypted[:])

			cipher, _ := RC5_SETUP(key, iv, "CBC")
			cipher.RC5_DECRYPT(encrypted[:], decrypted[:])

			if !bytes.Equal(value[:], decrypted[:]) {
				t.Errorf("encryption/decryption failed: % 02x != % 02x\n", value, decrypted)
			}
		}
	}
}

func TestRC5_TESTVECTORS_R12(t *testing.T) {
	vectors := readJSON("../TestVectors/RC5_TestVectors_r12.json")
	runTest(vectors, t)
}

// func TestRC5_TESTVECTORS_R20(t *testing.T) {
// 	vectors := readJSON("../TestVectors/RC5_TestVectors_r20.json")
// 	runTest(vectors, t)
// }

func runTest(vectors []map[string]string, t *testing.T) {
	var encrypted [8]byte
	var decrypted [8]byte
	for _, item := range vectors {
		key, _ := hex.DecodeString(item["Key"])
		pt, _ := hex.DecodeString(item["Input"])
		ct, _ := hex.DecodeString(item["Output"])

		cipher, ok := RC5_SETUP(key, []byte(""), "None")
		if ok {
			cipher.RC5_ENCRYPT(pt[:], encrypted[:])
			if !bytes.Equal(ct[:], encrypted[:]) {
				t.Errorf("encryption/decryption failed: % 02x != % 02x\n", encrypted, ct)
			}

			cipher.RC5_DECRYPT(encrypted[:], decrypted[:])
			if !bytes.Equal(decrypted[:], pt[:]) {
				t.Errorf("encryption/decryption failed: % 02x != % 02x\n", decrypted, pt)
			}
		}
	}
}

func readJSON(path string) []map[string]string {
	jsonFile, err := os.Open(path)
	// if we os.Open returns an error then handle it
	if err != nil {
		fmt.Println(err)
	}
	defer jsonFile.Close()
	byteValue, _ := ioutil.ReadAll(jsonFile)
	var result []map[string]string
	json.Unmarshal([]byte(byteValue), &result)
	return result
}
