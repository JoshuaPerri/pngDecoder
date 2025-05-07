class BinaryTree:
  def __init__(self):
    self.head = Node()

  def add(self, code, value):
    current = self.head
    next = None
    for bit in code:
      next = current.children[bit]

      if (next == None):
        next = Node()
        current.addChild(bit, next)
      
      current = next
    
    current.setValue(value)

  def lookup(self, code):
    current = self.head
    next = None
    for bit in code:
      next = current.children[bit]

      if (next == None):
        return -1
      
      current = next
    
    return current.value

class Node:
  def __init__(self):
    self.children = [None, None]
    self.value = -1

  def isEnd(self):
    if (len(self.children) == 0):
      return False
    else:
      return True

  def addChild(self, dir, child):
    self.children[dir] = child

  def setValue(self, value):
    self.value = value
  