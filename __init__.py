"""
	TableForm

	format a "matrix" of strings int a table


"""


from . import __lib__ as lib
from . import __markdown_table__ as markdown

table = markdown.formatted_table


def plain_table (
		data: lib.Iterable[lib.Iterable[lib.Any]],
		show: bool = False,
		alignment:str = "^",
		cell_format: str = "{}",
		cells_separator:str = " ",
		cell_padding:str = "",
		fill: bool = False,
	) -> str:
	"""
		Just a table with a formatted cell
	"""
	table: str = lib.bind(
		lib.uniform_table(
			data,
			padding = cell_padding, fill_missing = fill,
			alignment_reference = markdown.generate_alignment_reference(alignment)
		),
		CS= cells_separator, CF= cell_format
	)
	if show:
		print(table)
	return table

