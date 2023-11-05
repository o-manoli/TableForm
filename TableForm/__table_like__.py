from . import __markdown_table__ as markdown
from typing import Iterable, Any
from . import __lib__ as lib

def table (
		data: Iterable[Iterable[Any]],
		show: bool = False,
		alignment:str = "^",
		cell_format: str = "{}",
		cells_separator:str = " ",
		cell_padding:str = "",
		fill: bool = False,
	) -> str | None:
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
		return
	return table

