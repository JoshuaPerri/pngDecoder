from bitstring import BitStream
from bitstring import BitArray
from binarytree import BinaryTree

class BitReader:
  def __init__(self, bits: BitStream):
    self.bitStream = bits
    self.leftEnd = 0
    self.rightEnd = 0
    self.bitsLeft = 0
    self.currentByte = None

  def getNewByte(self):
    self.currentByte: BitArray = self.bitStream.read("bits8")
    self.leftEnd = 0
    self.rightEnd = 8
    self.bitsLeft = 8

  def getBits(self, length: int):
    if (self.currentByte == None):
      self.getNewByte()
    elif (self.bitsLeft <= 0):
      self.getNewByte()

    buffer = BitArray([])

    lengthRemaining = length
    while self.bitsLeft < lengthRemaining:
      lengthRemaining = length - self.bitsLeft

      buffer.prepend(self.currentByte[self.leftEnd:self.rightEnd])
      self.getNewByte()
    
    buffer.prepend(self.currentByte[self.rightEnd-lengthRemaining:self.rightEnd])
    self.bitsLeft -= lengthRemaining
    self.rightEnd -= lengthRemaining

    return(buffer)
  
  def getNextLiteral(self, tree: BinaryTree):
    code: BitArray = BitArray("")
    for i in range(16):
      bit = self.getBits(1)
      code.append(bit)

      if tree.lookup(code) != -1:
        return tree.lookup(code)
    return -1