class Database:
  def __init__(self):
    self.b1 = [[None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None]]
    self.b2 = [[None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None]]
    self.b3 = [[None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None]]
    self.b4 = [[None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None]]
    self.b5 = [[None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None]]
    
    self.r1 = [[None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None]]
    self.r2 = [[None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None]]
    self.r3 = [[None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None]]
    self.r4 = [[None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None]]
    self.r5 = [[None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None], [None, None, None, None, None]]

    self.match = None

    self.finalData = [self.b1, self.b2, self.b3, self.b4, self.b5, self.r1, self.r2, self.r3, self.r4, self.r5]

  def data_print(self):
    print("Most recent match:")
    print(self.match)
    print('Blue:')
    for i in range(5):
      print(self.finalData[i])
    print('Red:')
    for i in range(5, 10):
      print(self.finalData[i])
    
