# IMAGINE observational datasets repository

*Still under construction*

This package allows one to import a number of observational datasets
in a format compatible with [IMAGINE](https://github.com/IMAGINE-Consortium/imagine/).

## Usage

One can the available datasets using the package's `show_available`
function.
```python
import imagine_datasets as img_data

# Shows a list of available packages
img_data.show_available()
```
This will print the details of all the available datasets to screen. For example,
the part of this output corresponding to the Oppermann2012 Faraday depth map
is:
```console

-------------------imagine_datasets.HEALPix.fd.Oppermann2012--------------------
Class: imagine_datasets.HEALPix.fd.Oppermann2012
Observable: fd
Type: HEALPix
Bibliographic ref:  Oppermann et al. (2012) A&A, 542, A93
URL:  https://ui.adsabs.harvard.edu/abs/2012A&A...542A..93O/abstract
```

A dataset can be used in an IMAGINE inference pipeline by simply
instantiating its corresponding class and including it in a
`Measurements` object, for example,

```python
import imagine as img
import imagine_datasets as img_data
dset = img_data.HEALPix.fd.Oppermann2012(Nside=64)
```

Once loaded, the dataset contents can be used as a regular
IMAGINE dataset:

```python
measurements = img.observables.Measurements(dset)
```

Additionally, the datasets in this repository come with handy
attributes which point to the original publications

```python
citation = dset.ref
citation_url = dset.ref_url
```

Datasets in this repository also support *caching*.
Usually, a dataset is downloaded when it is requested (i.e. instantiated)
for the first time. If a *cache directory* is set, the data is saved to
disk and, thus, will not need to be downloaded again.

One can choose cache directory setting the module variable
`imagine_datasets.cache_dir` or using the environment variable
`IMAGINE_DATASETS_CACHE_PATH`, for example including the following line in
your .bashrc file:

```bash
export IMAGINE_DATASETS_CACHE_DIR=foo/bar/DatasetCacheDir
```
