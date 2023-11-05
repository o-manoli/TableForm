
import unittest

Loader = unittest.TestLoader()
Runner = unittest.TextTestRunner(verbosity= 2)

TestSuit = Loader.discover(f"./{__package__}")
Runner.run(TestSuit)

