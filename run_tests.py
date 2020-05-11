from unittest import TestLoader, TestSuite, TextTestRunner
import os
import sys




tl = TestLoader()
r = tl.discover(start_dir=os.getcwd())

tr = TextTestRunner()
tr.run(r)

