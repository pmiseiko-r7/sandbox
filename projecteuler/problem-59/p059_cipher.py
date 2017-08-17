import string
import re

def crypt(keyOctets, cipherOctets):
 textChars = []
 keyOctetIndex = 0
 for cipherOctet in cipherOctets:
  if keyOctetIndex >= len(keyOctets):
   keyOctetIndex = 0
  textChar = chr(keyOctets[keyOctetIndex] ^ cipherOctet)
  textChars.append(textChar)
  keyOctetIndex += 1
 return "".join(textChars)

def findKey(cipherOctets, dictionaryWords, validWordThreshold):
 matches = []
 for keyChar1 in string.ascii_lowercase:
  keyOctet1 = ord(keyChar1)
  for keyChar2 in string.ascii_lowercase:
   keyOctet2 = ord(keyChar2)
   for keyChar3 in string.ascii_lowercase:
    keyOctet3 = ord(keyChar3)
    keyOctets = [keyOctet1, keyOctet2, keyOctet3]
    keyChars = keyChar1 + keyChar2 + keyChar3
    print "Testing key:", keyChars, keyOctets
    resultChars = crypt(keyOctets, cipherOctets)
    # print "Key output:", resultChars
    badResult = False
    for resultChar in resultChars:
     if resultChar not in string.printable:
      badResult = True
      break
    # Short circuit to improve performance.
    if badResult:
     continue
    # Now test if the key produced real english.
    wordCount = 0
    validWordCount = 0
    for m in re.finditer("([a-zA-Z]+)", resultChars):
     word = m.group(1)
     wordCount += 1
     if word in dictionaryWords:
      validWordCount += 1
    # Must be at least 1 valid word.
    if validWordCount > 0:
     validWordPercentage = float(validWordCount) / wordCount
     if validWordPercentage >= validWordThreshold:
      print "Key output has", wordCount, "word(s) with", validWordCount, "valid."
      print "Key output has", validWordPercentage, "% valid word(s)."
      print "Key output:", resultChars
      matches.append((keyChars, wordCount, validWordCount, resultChars))
     else:
      # print "Key", keyChars, "incorrect."
      pass
 return matches

with open("/usr/share/dict/words", "r") as dictionaryFile:
 dictionaryWords = []
 for line in dictionaryFile:
  dictionaryWord = line.strip()
  dictionaryWords.append(dictionaryWord)
 with open("p059_cipher.txt", "r") as cipherFile:
  data = cipherFile.read()
  cipherOctets = []
  for octet in data.split(","):
   cipherOctets.append(int(octet))
  for match in findKey(cipherOctets, dictionaryWords, 0.80):
   key, wordCount, validWordCount, text = match
   print "Key:", key
   print "Word Count:", wordCount
   print "Valid Word Count:", validWordCount
   print "Text:", text
