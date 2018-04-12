Rasterio Code Analyzer
======================

Rasterio 1.0 will not permit reading from datasets opened in "w" mode. The
rasterio_code_analyzer module can be used to find such deprecated usage.

This module requires Python 3.6.

Running it on Rasterio's tests (as of 2018-04-11) yields the following output.

```
$ parallel 'python -m rasterio_code_analyzer {}' ::: tests/*.py
In file tests/test_complex_dtypes.py dataset.read() is called on line 37 and column 18 where dataset is opened in 'w' mode
In file tests/test_dataset_rw.py dst.read() is called on line 37 and column 20 where dst is opened in 'w' mode
In file tests/test_gdal_raster_io.py dataset.read() is called on line 35 and column 18 where dataset is opened in 'w' mode
In file tests/test_gdal_raster_io.py dataset.read() is called on line 47 and column 18 where dataset is opened in 'w' mode
In file tests/test_gdal_raster_io.py dataset.read() is called on line 59 and column 18 where dataset is opened in 'w' mode
In file tests/test_gdal_raster_io.py dataset.read() is called on line 73 and column 17 where dataset is opened in 'w' mode
In file tests/test_gdal_raster_io.py dataset.read() is called on line 89 and column 17 where dataset is opened in 'w' mode
In file tests/test_rio_mask.py out.read() is called on line 200 and column 12 where out is opened in 'w' mode
```
