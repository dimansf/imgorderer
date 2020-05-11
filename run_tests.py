from unittest import TestLoader, TestSuite, TextTestRunner
import os
import sys

# print()


tl = TestLoader()
r = tl.discover(start_dir=os.getcwd())

tr = TextTestRunner(verbosity=2)
tr.run(r)

