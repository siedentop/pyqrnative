#Copyright: 2011 Christoph Siedentop
#License: This code is licensed under the GPLv3. For more see LICENSE

from PyQRNative import QRCode, QRErrorCorrectLevel, CodeOverflowException

class QR():
	''' Base QR Code API class.'''
	def __init__(self, size=1, level = QRErrorCorrectLevel.M):
		self.qr = QRCode(size, level)
		self.data = ''
		self.level = level
		self.size = size
		self.needs_update = True
		
	def write(self, text):
		self.data += text.__str__()
		self.needs_update = True
		
	def make(self):
		if self.needs_update == True:
			self.qr = QRCode(self.size, self.level)
			self.qr.addData(self.data)
			# Check that the data fits into the QR code of the required size:
			size = self.qr.getMinimumSize()
			if self.size < size: 
				self.size = size
				self.qr = QRCode(size, self.level)
				self.qr.addData(self.data)
			self.qr.make()
			self.image = self.qr.makeImage()
			self.needs_update = False
		
	def display(self):
		if self.needs_update:
			self.make()
		self.image.show()
		
	def save(self, imagename):
		self.image.save(imagename)
		

class QRFile(QR):
	''' Implements the sending of files, as supported by Scripting Layer for Android (SL4A). 
The first line is the filename, the resulting lines are just the file.

Example usage: 
>>> f = QRFile(infile='myfile.txt', filename= 'myscript.py', size = 5)
>>> f.make()
>>> f.save('tmpfile.png')
>>> f.display()
'''
	def __init__(self, infile, filename, size=10, level = QRErrorCorrectLevel.L):
		''' Input:
	infile: filehandle or filename (string)
	filename: string for output filename
	size: minimum size of QR-code 1..40; Default 10.
	level: Error correction level, (L, M, Q, H).'''
		QR.__init__(self, size= size, level=level)
		self.loadFile(infile, filename)
		
	def loadFile(self, infile, filename):
		self.write(filename)
		self.write('\n')
		if isinstance(infile, file):
			self.write(infile.read())
		elif isinstance(infile, str):
			fh = open(infile, 'r')
			self.write(fh.read())
			fh.close()
		else:
			raise Exception('Could not handle input argument for file.')

class QRUrl(QR):
	''' URL/URI class for QR codes. 

Pass a url, no checking will be done!'''
	def __init__(self, url, size=1, level = QRErrorCorrectLevel.L):
		QR.__init__(self, size= size, level=level)
		self.write(url) # No formatting checks will be performed to allow more flexibility. 


if __name__=='__main__':
	f = QRUrl(url = 'rtsp://sdcard/')
	f.make()
	f.display()