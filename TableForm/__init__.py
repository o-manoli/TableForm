"""
	TableForm

	format a "matrix" of strings int a table


"""

from . import __markdown_table__ as markdown
from . import __table_like__ as Tables
from . import __lib__ as lib

table = markdown.formatted_table

plain_table = Tables.table

uniform_table = lib.uniform_table

