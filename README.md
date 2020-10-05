# IMAGINE observational datasets repository

*Still under construction*

This package allows one to import a number of observational datasets
in a format compatible with [IMAGINE](https://github.com/IMAGINE-Consortium/imagine/).

## Usage

One can list the available datasets using the package's `list` function. 
```python
import imagine_datasets as img_dset

# Shows a list of available packages
img_dset.list()
```

A dataset can be used in an IMAGINE inference pipeline by simply
instantiating its corresponding class and including it in a
`Measurements` object, for example,
```python
import imagine as img
dset = img_dset.HEALPix.fd.Opperman2012(Nside=32)
measurements = img.observables.Measurements(dset)
```

Usually, a dataset is downloaded when it is requested (i.e. instantiated)
for the first time. If a *cache directory* is set, the data is saved to 
disk and will not need to be downloaded again. 

One can set cache directory 
using the `IMAGINE_DATASET_CACHE_PATH` environment variable, for example
including including the following line in your .bashrc file:
```bash
export IMAGINE_DATASET_CACHE_PATH=foo/bar/DatasetCacheDir
```
