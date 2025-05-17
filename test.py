#!/usr/bin/env python3

import unittest

from scripts import triple_char

class testscripts(unittest.TestCase)

    def test_triple_char(self)
    """Test the triple_char scripts to ensure script functions as intended."""
        self.assertEqual(triple_char("Hello"), "HHHeeellllllo")
        self.assertEqual(triple_char("Test"), "TTTeeesssttt")
        self.assertEqual(triple_char("123!"), "111222333!!!")
