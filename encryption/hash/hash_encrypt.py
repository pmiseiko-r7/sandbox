import binascii
import hashlib
import string

secret = "this is another secret"
inData = b"The quick brown fox jumps over the lazy dog"

def crypt(secret, inData, encrypt):
 outData = []
 secretHash = hashlib.sha256()
 secretHash.update(secret.encode())
 secretDigest = secretHash.digest()
 randomnessHash = hashlib.sha256()
 randomnessHash.update(secretDigest)

 inDataIndex = 0
 while inDataIndex < len(inData):
  randomnessHash.update(secretDigest)
  randomnessDigest = randomnessHash.digest()
  randomnessHash.update(randomnessDigest)
  randomnessIndex = 0
  while inDataIndex < len(inData) and randomnessIndex < len(randomnessDigest):
   if encrypt:
    randomnessHash.update(chr((inDataIndex & 0xFF) ^ inData[inDataIndex]).encode())
   outByte = inData[inDataIndex] ^ randomnessDigest[randomnessIndex]
   if not encrypt:
    randomnessHash.update(chr((inDataIndex & 0xFF) ^ outByte).encode())
   outData.append(chr(outByte))
   if encrypt:
    print("%c 0x%02X (%03d) ^ 0x%02X (%03d) = 0x%02X" % (
     inData[inDataIndex], inData[inDataIndex], inDataIndex,
     randomnessDigest[randomnessIndex], randomnessIndex,
     outByte))
   else:
    outByteText = chr(outByte)
    if outByteText not in string.printable:
     outByteText = "."
    print(". 0x%02X (%03d) ^ 0x%02X (%03d) = %c 0x%02X" % (
     inData[inDataIndex], inDataIndex,
     randomnessDigest[randomnessIndex], randomnessIndex,
     outByteText, outByte))
   inDataIndex += 1
   randomnessIndex += 1

 return "".join(outData)


outData1 = crypt(secret, inData, True).encode("latin_1")
outData2 = crypt(secret, outData1, False).encode("latin_1")

print(binascii.hexlify(outData1))
print(binascii.hexlify(outData2))
print(inData == outData2)
