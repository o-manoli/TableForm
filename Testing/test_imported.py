
import unittest

class TestingImporting(unittest.TestCase):

	def test_import(self):
		import TableForm

		print(
		f"""

			Hello, World!

		Package Content:

		""", *dir(TableForm), sep = "\n"
		)

		self.assertTrue(
			hasattr(TableForm, "table"),
			msg= "The Package is missing the API: table"
		)

		self.assertTrue(
			hasattr(TableForm, "plain_table"),
			msg= "The Package is missing the API: plain_table"
		)

		print("\n\tTest import: PASSED ...\n")


