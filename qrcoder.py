from pyqrnative.PyQRNative import QRCode, QRErrorCorrectLevel, CodeOverflowException

class QR():
	def __init__(self, size=1, level = QRErrorCorrectLevel.M):
		self.qr = QRCode(size, level)
		self.data = ''
		self.level = level
		self.size = size
		
	def write(self, text):
		self.data += text.__str__()
		
	def make(self):
		complete = False
		while not complete:
			self.qr = QRCode(self.size, self.level)
			self.qr.addData(self.data)
			try:
				self.qr.make()
			except CodeOverflowException:
				self.size +=1
			else:
				complete = True
		self.image = self.qr.makeImage()
		
	def display(self):
		self.make()
		self.image.show()
		

class QRFile(QR):
	def __init__(self, infile, size=10, level = QRErrorCorrectLevel.L):
		QR.__init__(self, size= size, level=level)
		self.loadFile(infile)
		
	def loadFile(self, infile):
		if isinstance(infile, file):
			self.write(infile.read())
		elif isinstance(infile, str):
			fh = open(infile, 'r')
			self.write(fh.read())
			fh.close()
		else:
			raise Exception('Could not handle input argument for file.')
	

if __name__=="__main__":
	fh = open('somecode.py', 'r')
	
	q = QR()
	q.write('sometext')
	q.write('other stuff')
	#q.display()
	
	f = QRFile(infile = 'somecode.py', size = 15)
	f.make()
	print "Size is %s" %(f.size)
	f.display()