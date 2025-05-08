from bitstring import BitStream
from bitstring import BitArray
from bitreader import BitReader
from binarytree import BinaryTree

LTABLE = dict([
  (257, {"ebits": 0, "length": 3}),
  (258, {"ebits": 0, "length": 4}),
  (259, {"ebits": 0, "length": 5}),
  (260, {"ebits": 0, "length": 6}),
  (261, {"ebits": 0, "length": 7}),
  (262, {"ebits": 0, "length": 8}),
  (263, {"ebits": 0, "length": 9}),
  (264, {"ebits": 0, "length": 10}),
  (265, {"ebits": 1, "length": 11}),
  (266, {"ebits": 1, "length": 13}),
  (267, {"ebits": 1, "length": 15}),
  (268, {"ebits": 1, "length": 17}),
  (269, {"ebits": 2, "length": 19}),
  (270, {"ebits": 2, "length": 23}),
  (271, {"ebits": 2, "length": 27}),
  (272, {"ebits": 2, "length": 31}),
  (273, {"ebits": 3, "length": 35}),
  (274, {"ebits": 3, "length": 43}),
  (275, {"ebits": 3, "length": 51}),
  (276, {"ebits": 3, "length": 59}),
  (277, {"ebits": 4, "length": 67}),
  (278, {"ebits": 4, "length": 83}),
  (279, {"ebits": 4, "length": 99}),
  (280, {"ebits": 4, "length": 115}),
  (281, {"ebits": 5, "length": 131}),
  (282, {"ebits": 5, "length": 163}),
  (283, {"ebits": 5, "length": 195}),
  (284, {"ebits": 5, "length": 227}),
  (285, {"ebits": 0, "length": 258}),
])
DTABLE = dict([
  (0,  {"ebits": 0,  "dist": 1}),
  (1,  {"ebits": 0,  "dist": 2}),
  (2,  {"ebits": 0,  "dist": 3}),
  (3,  {"ebits": 0,  "dist": 4}),
  (4,  {"ebits": 1,  "dist": 5}),
  (5,  {"ebits": 1,  "dist": 7}),
  (6,  {"ebits": 2,  "dist": 9}),
  (7,  {"ebits": 2,  "dist": 13}),
  (8,  {"ebits": 3,  "dist": 17}),
  (9,  {"ebits": 3,  "dist": 25}),
  (10, {"ebits": 4,  "dist": 33}),
  (11, {"ebits": 4,  "dist": 49}),
  (12, {"ebits": 5,  "dist": 65}),
  (13, {"ebits": 5,  "dist": 97}),
  (14, {"ebits": 6,  "dist": 129}),
  (15, {"ebits": 6,  "dist": 193}),
  (16, {"ebits": 7,  "dist": 257}),
  (17, {"ebits": 7,  "dist": 385}),
  (18, {"ebits": 8,  "dist": 513}),
  (19, {"ebits": 8,  "dist": 769}),
  (20, {"ebits": 9,  "dist": 1025}),
  (21, {"ebits": 9,  "dist": 1537}),
  (22, {"ebits": 10, "dist": 2049}),
  (23, {"ebits": 10, "dist": 3073}),
  (24, {"ebits": 11, "dist": 4097}),
  (25, {"ebits": 11, "dist": 6145}),
  (26, {"ebits": 12, "dist": 8193}),
  (27, {"ebits": 12, "dist": 12289}),
  (28, {"ebits": 13, "dist": 16385}),
  (29, {"ebits": 13, "dist": 24577}),
])

def createFixedHuffmanTree():
  tree = BinaryTree()

  for i in range(24):
    code = BitStream(format(i, "#09b"))
    tree.add(code, i + 256)

  for i in range(144):
    j = i + 48
    code = BitStream(format(j, "#010b"))
    tree.add(code, i)

  for i in range(8):
    j = i + 192
    code = BitStream(format(j, "#010b"))
    tree.add(code, i + 280)

  for i in range(112):
    j = i + 16 + 128 + 256
    code = BitStream(format(j, "#011b"))
    tree.add(code, i + 144)
  
  return tree

# Build a Huffman Tree from a list of code lengths
def createHuffmanTreeFromCL(clList):

  orderedCodes = []
  nextCode = 0
  bitLength = 1
  for i in range(1, max(clList) + 1):
    for j, codeBitLength in enumerate(clList):
      if codeBitLength == bitLength:
        orderedCodes.append({"code":j, "bl":codeBitLength, "bitCode":nextCode})
        nextCode += 1
    bitLength += 1
    nextCode <<= 1

  tree = BinaryTree()

  for entry in orderedCodes:
    code = BitStream(format(entry["bitCode"], "#0"+str(entry["bl"] + 2)+"b"))
    tree.add(code, entry["code"])
    print("Code: %-3d     Bit Length: %-2d     Bit Code: %s"%(entry["code"], entry["bl"], format(entry["bitCode"], "#0"+str(entry["bl"] + 2)+"b")))
  
  # print()

  return tree


# Build the Huffman Tree that encodes the code lengths for the dynamic Huffman Tree encoding
def createHuffmanCLTree(bitReader: BitReader, HCLEN: int):
  ALPHABET = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]

  codeBitLengths = [0] * 19
  for i in range(HCLEN):
    codeBitLengths[i] = bitReader.getBits(3).uint

  sortedLengths = []
  for i in range(19):
    sortedLengths.append(codeBitLengths[ALPHABET.index(i)])

  return createHuffmanTreeFromCL(sortedLengths)


# Creates the literal/length and dist dynamic Huffman trees from the encoded data in bitReader
def createDynamicHuffmanTrees(bitReader: BitReader):
  HLIT = bitReader.getBits(5).uint + 257
  HDIST = bitReader.getBits(5).uint + 1
  HCLEN = bitReader.getBits(4).uint + 4

  print("----------------------------------------------------------------------")
  print(" Dynamic Huffman Tree Encoding   HLIT=%d    HDIST=%d   HCLEN=%d"%(HLIT, HDIST, HCLEN))
  print("----------------------------------------------------------------------")

  clTree = createHuffmanCLTree(bitReader, HCLEN)

  codes = []
  i = 0
  while i < HLIT + HDIST:
    nextCode = bitReader.getNextLiteral(clTree)
    if (nextCode <= 15):
      # print("Code", nextCode)
      codes.append(nextCode)
      i += 1
    elif (nextCode == 16):
      eBits = bitReader.getBits(2)
      lastLiteral = codes[-1]
      # print("Code 16, repeat", lastLiteral, 3 + eBits.uint, "times")
      for j in range(3 + eBits.uint):
        codes.append(lastLiteral)
      i += 3 + eBits.uint
    elif (nextCode == 17):
      eBits = bitReader.getBits(3)      
      # print("Code 17, repeat 0", 3 + eBits.uint, "times")
      for j in range(3 + eBits.uint):
        codes.append(0)
      i += 3 + eBits.uint
    elif (nextCode == 18):
      eBits = bitReader.getBits(7)
      # print("Code 18, repeat 0", 11 + eBits.uint, "times")
      for j in range(11 + eBits.uint):
        codes.append(0)
      i += 11 + eBits.uint
    else:
      print("ERROR")

  # Length/Literal Codes
  llCodes = codes[:HLIT]
  # Dist Codes
  dCodes = codes[HLIT:HLIT+HDIST]

  llTree = createHuffmanTreeFromCL(llCodes)
  dTree  = createHuffmanTreeFromCL(dCodes)

  return llTree, dTree


def inflateBlock(bs: BitStream):

  inflatedBlock = []

  bitReader = BitReader(bs)

  BFINAL = bitReader.getBits(1).uint == 1
  BTYPE  = bitReader.getBits(2).uint

  print("-------------------------------------------------")
  print(" Deflate Encoded Block   BFINAL: %s   BTYPE: %d"%(BFINAL, BTYPE))
  print("-------------------------------------------------")

  if BTYPE == 0:
    pass
  elif BTYPE == 1:
    fTree = createFixedHuffmanTree()

    while True:
      literal: BitArray = bitReader.getNextLiteral(fTree)
      if (literal < 256):
        inflatedBlock.append(chr(literal))
      elif (literal == 256):
        break
      elif (literal <= 285):
        numEbits = LTABLE[literal]["ebits"]

        ebits = 0
        if (numEbits > 0):
          ebits = bitReader.getBits(numEbits).uint

        length = LTABLE[literal]["length"] + ebits

        distCode = bitReader.getBits(5).uint
        numEbits = DTABLE[distCode]["ebits"]

        ebits = 0
        if (numEbits > 0):
          ebits = bitReader.getBits(numEbits).uint
        
        dist = DTABLE[distCode]["dist"] + ebits 

        for i in range(length):
          inflatedBlock.append(inflatedBlock[-1 * dist])

  elif BTYPE == 2:
    lTree, dTree = createDynamicHuffmanTrees(bitReader)

    j = 0
    while True:
      literal: BitArray = bitReader.getNextLiteral(lTree)
      if (literal < 256):
        # print(literal)
        inflatedBlock.append(chr(literal))

        j += 1
      elif (literal == 256):
        break
      elif (literal <= 285):
        numEbits = LTABLE[literal]["ebits"]

        ebits = 0
        if (numEbits > 0):
          ebits = bitReader.getBits(numEbits).uint

        # print(literal, ebits, end="   ")
        length = LTABLE[literal]["length"] + ebits

        distCode = bitReader.getNextLiteral(dTree)
        numEbits = DTABLE[distCode]["ebits"]

        ebits = 0
        if (numEbits > 0):
          ebits = bitReader.getBits(numEbits).uint
        
        dist = DTABLE[distCode]["dist"] + ebits 

        # print("<" + str(length) + "," + str(dist) + ">", end="")
        # print(distCode, ebits)
        # inflatedBlock += inflatedBlock[-1 * dist: -1 * dist + length]
        end = len(inflatedBlock)
        if (end - dist + length <= end):
          inflatedBlock += inflatedBlock[end - dist: end - dist + length]
        else:
          for i in range(length):
            inflatedBlock.append(inflatedBlock[end - dist + i])
        # inflatedBlock.append("<" + str(length) + "," + str(dist) + ">")
        j += length
        

  else:
    print("Error")

  return BFINAL, inflatedBlock


def inflate(bs: BitStream):
  inflatedFile = []
  isLast = False
  while not isLast:
    isLast, inflatedBlock = inflateBlock(bs)
    inflatedFile +=inflatedBlock
  
  return inflatedFile