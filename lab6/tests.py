#!/usr/bin/env python
import unittest

from arithmetic import *

class ArithmeticCompressionTest(unittest.TestCase):
    
    def test_make_part_with_sequence(self):
    	expected = [0x00, 0x03, 0x01, 0x02, 0x03]
    	actual = sign_sequence([0x01, 0x02, 0x03])
    	self.assertEqual(expected, actual)

    def test_make_part_with_repeating(self):
    	expected = [0x03, 0x00]
    	actual = sign_byte(3, 0x00)
    	self.assertEqual(expected, actual)

    def test_pack_bytes(self):
    	expected = [0x05, 0x41, 0x00, 0x02, 0x43, 0x41, 0x03, 0x42, 0x02, 0x41]
    	actual = pack_bytes(b'AAAAACABBBAA')
    	self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
