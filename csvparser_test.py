# -*- coding: utf-8 -*-
import unittest
from csvparser import CsvParser
from StringIO import StringIO

class TestCsvParser(unittest.TestCase):

    def setUp(self):
        self.parser = parser = CsvParser()

    def parse(self, src):
        return self.parser.parse(StringIO(src))

    def test(self):
        self.assertEqual([], self.parse(''))
        self.assertEqual([['a']], self.parse('a'))
        self.assertEqual([[u'山田']], self.parse(u'山田'))
        self.assertEqual([['', '']], self.parse(','))
        self.assertEqual([['', '', '']], self.parse(',,'))
        self.assertEqual([['']], self.parse('\n'))
        self.assertEqual([['a'], ['b']], self.parse('a\nb'))
        self.assertEqual([['a'], ['b']], self.parse('a\r\nb'))
        self.assertEqual([['a'], ['b"c']], self.parse('a\nb"c'))
        self.assertEqual([['']], self.parse('""'))
        self.assertEqual([['']], self.parse('""\n'))
        self.assertEqual([['']], self.parse('""\r\n'))
        self.assertEqual([['"']], self.parse('""""\r\n'))
        self.assertEqual([['a', 'b\nc', 'd']], self.parse('a,"b\nc",d'))

if __name__ == '__main__':
    unittest.main()
