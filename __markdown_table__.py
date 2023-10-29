from . import __lib__ as lib
from collections import defaultdict
from typing import (
	Iterable,
	Iterator,
	Callable,
	Any
	)


# Python Alignment Options
PAling: tuple[str, str, str] = "<", ">", "^"       # left, right and center

# Markdown Alignment Options
MAling: tuple[str, str, str] = ":-", "-:", ":-:"   # left, right and center
MINIMUM_CELL_SIZE = {k:len(k) for k in MAling}

def mapping(keys: Iterable[str], values: Iterable[str]) -> dict[str, str]:
	return { key: value for key, value in zip(keys, values)}

P2P:dict[str, str] = mapping(PAling, PAling)
M2P:dict[str, str] = mapping(MAling, PAling)
M2M:dict[str, str] = mapping(MAling, MAling)
P2M:dict[str, str] = mapping(PAling, MAling)

# Markdown or Python to Python Alignment
MOP2P: dict[str, str] = P2P | M2P                              # InterpreterStone
MOP2M: dict[str, str] = P2M | M2M | defaultdict(lambda: "-")   # InterpreterStone


# left, right and center
formatted_separator: dict[str, Callable[[int], str]] = {
	":-"  : lambda size= 0 : f":-{(size-2)*'-'}",
	"-:"  : lambda size= 0 : f"{(size-2)*'-'}-:",
	":-:" : lambda size= 0 : f":-{(size-3)*'-'}:",
	"-"   : lambda size= 0 : f"{size*'-'}"
}


def generate_alignment_reference(
		*alignment:str,
		default_alignment:str | None = None,
		InterpreterStone: dict[str, str] = MOP2P,
		columns_alignment: dict[int, str] = {}
		) -> dict[int, str]:
	r"""
		Returns a Mapping an alignment list

		Alignment Option:
			# left, right and center
				"<", ">", "^"             # Python Syntax
				":-", "-:", ":-:"         # Markdown Syntax

		if default_alignment the first argument will be considered the default
		if there is no first argument it reverts to center alignment

	"""

	if default_alignment is None:
		default_alignment = alignment[0] if len(alignment) else "^"

	return {
			column : InterpreterStone[align] for column, align in enumerate(alignment)
	} | {
			i: InterpreterStone[a] for i, a in columns_alignment.items()
	} | defaultdict(lambda: InterpreterStone[default_alignment])


def formatted_table(
		data: Iterable[Iterable[Any]],
		default_alignment: str = "^",
		*column_alignment: str,
		# out of order colum alignment options
		columns_alignment: dict[int, str] = {},
		header: Iterable[Any] | None = None,
	) -> str:

	"""
		Returns a Markdown formatted Table

		Alignment Option:
			# left, right and center
				"<", ">", "^"             # Python Syntax
				":-", "-:", ":-:"         # Markdown Syntax

		if the header is specifically defined the first row will be the table header

	"""

	Align: dict[int, str] = generate_alignment_reference(
			*column_alignment,
			default_alignment = default_alignment,
			columns_alignment = columns_alignment
		)

	def iterate() -> Iterator[Iterable[Any]]:
		if header is not None:
			yield header
		yield from data

	entry_table = lib.uniform_table(
		iterate(),
		alignment_reference= Align,
		fill_missing= True,
		minimum_cell_width= {
			column: MINIMUM_CELL_SIZE[P2M[a]] for column, a in Align.items()
			} | defaultdict(lambda: len(P2M[MOP2P[default_alignment]]))
	)

	if not len(entry_table):
		return ""

	def format_markdown_header(
			header:tuple[str, ...]
		) ->Iterator[tuple[str, ...]]:
		yield header
		yield tuple(
				formatted_separator[P2M[Align[i]]](size)
				for i, size in enumerate(map(len, header))
			)

	def yielder() -> Iterator[tuple[str, ...]]:
		yield from format_markdown_header(entry_table[0])
		yield from entry_table[1:]

	return lib.bind(yielder(), CS="|", CF=" {} ", RF = "|{}|")


def unformatted_table(
		data: Iterable[Iterable[Any]],
		default_alignment: str = "^",
		*column_alignment: str,
		# out of order colum alignment options
		columns_alignment: dict[int, str] = {},
		header: Iterable[Any] | None = None,
	) -> str:

	"""
		Returns a Markdown formatted Table

		Alignment Option:
			# left, right and center
				"<", ">", "^"             # Python Syntax
				":-", "-:", ":-:"         # Markdown Syntax

		if the header is specifically defined the first row will be the table header

	"""

	Align: dict[int, str] = generate_alignment_reference(
			*column_alignment,
			default_alignment = default_alignment,
			InterpreterStone= MOP2M,
			columns_alignment = columns_alignment
		)

	def iterate() -> Iterator[Iterable[Any]]:
		if header is not None:
			yield header
		yield from data

	entry_table = lib.solidify(iterate(), fill= True, placeholder= "")

	if not len(entry_table):
		return ""

	def format_markdown_header(
			header:tuple[str, ...]
		) ->Iterator[tuple[str, ...]]:
		yield header
		yield tuple(
				formatted_separator[Align[i]](size)
				for i, size in enumerate(map(len, header))
			)

	def yielder() -> Iterator[tuple[str, ...]]:
		yield from format_markdown_header(entry_table[0])
		yield from entry_table[1:]

	return lib.bind(yielder(), CS="|", CF="{}", RF = "|{}|")

