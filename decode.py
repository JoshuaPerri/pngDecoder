from bitstring import BitStream
import inflate

def decodePNG(file):
  header = file.read(8)

  if (bytes.hex(header) != '89504e470d0a1a0a'):
    return(1)

  dims = {"length": 0, "width":0}
  img = []
  while True:
    length = int.from_bytes(file.read(4))
    chunkType = file.read(4).decode("ascii")
    chunkData = file.read(length)
    crc = file.read(4)
    print(chunkType)

    if (chunkType == "IHDR"):
      dims["length"] = int.from_bytes(chunkData[0:4])
      dims["width"] = int.from_bytes(chunkData[4:8])
      bitDepth = int.from_bytes(chunkData[8:9])
      colorType = int.from_bytes(chunkData[9:10])
      compMethod = int.from_bytes(chunkData[10:11])
      filterMethod = int.from_bytes(chunkData[11:12])
      interlaceMethod = int.from_bytes(chunkData[12:13])

      print("bit depth: ", bitDepth)
      print("color type: ", colorType)

    if (chunkType == "IDAT"):
      data = file.read()
      img += inflate.inflate(BitStream(data))

    if (chunkType == "IEND"):
      print(img)
      break


  # lines = file.readlines()
  # k = 0
  # for i in lines:
  #   print(i)
  #   k += 1

with open("testfiles/test2.png", "rb") as file:
  decodePNG(file)