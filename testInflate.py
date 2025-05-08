from bitstring import BitStream
from bitstring import BitArray
import inflate

with open("testfiles/test4.txt.gz", "rb") as file:
  data = file.read()

  bits = BitStream(data)
  id1 = bits.read('hex8')
  id2 = bits.read('hex8')

  CM = bits.read('hex8')

  print("CM", CM)

  FLG = bits.read('bin8')

  print("FLG", FLG)

  MTIME = bits.read('hex32')

  XFL = bits.read('bin8')
  OS = bits.read('bin8')

  print("XFL", XFL)
  print("OS", OS)

  out = inflate.inflate(bits)

  for c in out:
    print(c, end="")
  print()