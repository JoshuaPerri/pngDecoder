from bitstring import BitStream
from bitstring import BitArray
from binarytree import BinaryTree

class BitReader:
  def __init__(self, bits: BitStream):
    self.bitStream = bits
    self.currentByte = None
    self.rightEnd = 0
    self.bitsLeft = 0

  def getNewByte(self):
    self.currentByte: BitArray = self.bitStream.read("bits8")
    self.rightEnd = 8
    self.bitsLeft = 8

  def getNextBit(self):
    if (self.currentByte == None or self.bitsLeft <= 0):
      self.getNewByte()

    bit = self.currentByte[self.rightEnd-1:self.rightEnd]    
    self.bitsLeft -= 1
    self.rightEnd -= 1

    return bit

  def getBits(self, length: int):
    # if (self.currentByte == None):
    #   self.getNewByte()
    # elif (self.bitsLeft <= 0):
    #   self.getNewByte()

    # buffer = BitArray([])

    # lengthRemaining = length
    # while self.bitsLeft < lengthRemaining:
    #   lengthRemaining = length - self.bitsLeft

    #   buffer.prepend(self.currentByte[0:self.rightEnd])
    #   self.getNewByte()
    
    # buffer.prepend(self.currentByte[self.rightEnd-lengthRemaining:self.rightEnd])
    # self.bitsLeft -= lengthRemaining
    # self.rightEnd -= lengthRemaining

    buffer: BitArray = BitArray([])
    for i in range(length):
      buffer.prepend(self.getNextBit())

    return(buffer)
  
  def getNextLiteral(self, tree: BinaryTree):
    code: BitArray = BitArray("")
    for i in range(16):
      bit = self.getNextBit()
      code.append(bit)

      if tree.lookup(code) != -1:
        return tree.lookup(code)
    return -1