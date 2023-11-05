# Python Package TableForm

## Support for:

### [2B imported as API-Library Code](./__init__.py)

Provides an interface to create a "table" by just calling function like `table`, `plain_table` with form of an Iterable `tuple, list, generator, numpy.ndarry ...` just about anything, that can be passed to the `iter` function.

The data is expected to be in matrix form. So iterating over the data-object means to iterate over rows of a matrix. Each row should be Iterable and to loop over the row-object means to fetch the column-entry for that row. The rows shouldn't necessary be of uniform shape.

