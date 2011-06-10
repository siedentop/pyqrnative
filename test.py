##!/usr/bin/python
import zbar #Zbar can be installed in Debian/Ubuntu by installing python-zbar
import Image
import unittest
import PyQRNative

class TestQRCode(unittest.TestCase):

    def setUp(self):
        self.data = "Test string"
        
        # Create image
        qr = PyQRNative.QRCode(4, PyQRNative.QRErrorCorrectLevel.L)
        qr.addData(self.data)
        qr.make()
        self.image = qr.makeImage()

        # Set up scanner
        self.scanner = zbar.ImageScanner()
        self.scanner.parse_config('enable')

    def test_result(self):
        ''' Assert that the image contains the requested data'''
        self.image = self.image.convert('L')
        width, height = self.image.size
        raw = self.image.tostring()
        
        zimage = zbar.Image(width, height, 'Y800', raw)
        
        self.scanner.scan(zimage)

        for symbol in zimage:
            t =  symbol.type
            data = symbol.data
        self.assertEqual(data, self.data)
        self.assertEqual(t, zbar.EnumItem(64, 'QRCODE'))
    
    def tearDown(self):
        del(self.image)


if __name__ == '__main__':
    unittest.main()
