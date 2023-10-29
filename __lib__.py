from itertools import chain, cycle, count, islice
from collections import defaultdict
from functools import partial
from typing import (
	Callable,
	Iterable,
	Mapping,
	Tuple,
	Any
	)


def max_column_width(
		data: Iterable[Iterable[str]],	# preferably a tuple
		minimum_cell_width: Mapping[int, int] | None = None
		) -> Tuple[int, ...]:
	"""
		Returns a the max width required to represent a uniform table
		Does mpt care if the table has un even number of columns
	"""
	M:dict[int, int] = defaultdict(lambda: 0) # InternalMemory
	# should be sorted because the n+1 element will not be accessed before n
	# a defaultdict is a dict and a dict is an ordereddict

	def compare(
			colum:int, entry:int,
			width:dict[int, int] = M,
			Minimum: Mapping[int, int] = defaultdict(lambda: 0) \
				if minimum_cell_width is None else minimum_cell_width
			):
		width[colum] = max(entry, width[colum], Minimum[colum])

	for row in data:
		for i, entry in enumerate(map(len, row)):
			compare(i, entry)

	return tuple(M.values())


def cell_formatter(
		i: int, entry:str,                        # Indexed Entry
		P: str,                                   # Cell Padding
		C: Mapping[int, int] | Tuple[int, ...],   # Cell Size Reference
		A: Mapping[int, str]                      # Alignment
	) -> str:
	return f"{entry:{P}{A[i]}{C[i]}}"


def solidify(
		data: Iterable[Iterable[Any]],
		fill: bool = False,
		placeholder: str = "",
		mask: Callable[[Any], str] = str
	) -> Tuple[Tuple[str, ...], ...] :
	"""
		Returns iterable safe copy of the data with a mask applied

		Input Arguments:
			data: Iterable[Iterable[Any]],
			fill: bool = False,
			placeholder: str = "",
			mask: Callable[[Any], str] = str
	"""
	data = tuple(tuple(map(mask, row)) for row in data)

	if not fill:
		return data

	columns:int = max(map(len, data), default= 0)   # default for an empty iter()

	filler = cycle([str(placeholder)])

	return tuple(
		tuple(islice(chain(row, filler), columns)) for row in data
	)


def uniform_table(
		data: Iterable[Iterable[Any]],
		alignment_reference: Mapping[int, str] = defaultdict(lambda: "^"),
		padding: str = " ",
		fill_missing: bool = False,
		empty_cell_placeholder: str = "",   # missing column entry placeholder
		minimum_cell_width: Mapping[int, int] | None = None
	) -> Tuple[Tuple[str, ...], ...]:
	r"""
		Returns a Uniform Table

		Support for:
			- specific column alignment for an indexed column
			- make each row the same size with a placeholder option
			- minimum cell size for any column specified by its index

		Input Arguments:
			data: Iterable[Iterable[Any]],
			alignment_reference: Mapping[int, str] = defaultdict(lambda: "^"),
			padding: str = " ",
			fill_missing: bool = False,
			empty_cell_placeholder: str = "",   # missing column entry placeholder
			minimum_cell_width: Mapping[int, int] | None = None
	"""

	# solidify into a tuple of tuple of string
	data = solidify(data, fill=fill_missing, placeholder=empty_cell_placeholder)

	f = partial(
		cell_formatter,
		P = padding, C = max_column_width(data, minimum_cell_width),
		A = alignment_reference
	)

	return tuple(tuple(map(f, count() ,row)) for row in data)


def bind(
		data: Iterable[Iterable[Any]],
		CS: str = "",       # Cell Separator
		RS: str = "\n",     # Rows Separator
		CF: str = "{}",     # Cell Formatting
		RF:str = "{}"       # Row Formatting
	) -> str:
	r"""
		Binds a table to a string
			data: Iterable[Iterable[Any]],
			CS: str = "",       # Cell Separator
			RS: str = "\n",     # Rows Separator
			CF: str = "{}",     # Cell Formatting
			RF:str = "{}"       # Row Formatting
	"""
	return RS.join(
		RF.format(CS.join(map(CF.format, line))) for line in data
	)

