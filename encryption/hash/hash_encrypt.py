import binascii
import hashlib

secret = "this is another secret"
inData = b"The quick brown fox jumps over the lazy dog"
outData = []

secretHash = hashlib.sha3_256()
secretHash.update(secret.encode())
secretDigest = secretHash.digest()
randomnessHash = hashlib.sha3_256()
randomnessHash.update(secretDigest)

inDataIndex = 0
while inDataIndex < len(inData):
 randomnessHash.update(secretDigest)
 randomnessDigest = randomnessHash.digest()
 randomnessHash.update(randomnessDigest)
 randomnessIndex = 0
 while inDataIndex < len(inData) and randomnessIndex < len(randomnessDigest):
  randomnessHash.update(chr(inData[inDataIndex]).encode())
  outByte = inData[inDataIndex] ^ randomnessDigest[randomnessIndex]
  outData.append(chr(outByte))
  print("%c %02x (%03d) ^ %02x (%03d) = %02x" % (
   inData[inDataIndex], inData[inDataIndex], inDataIndex,
   randomnessDigest[randomnessIndex], randomnessIndex,
   outByte))
  inDataIndex += 1
  randomnessIndex += 1


print(binascii.hexlify("".join(outData).encode()))
