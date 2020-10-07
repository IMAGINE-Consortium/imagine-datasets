# %% IMPORTS
# Built-in imports
import abc
import os

# Package imports
import hickle as hkl

# IMAGINE imports
import imagine
from imagine.tools import BaseClass, req_attr
import imagine_datasets as img_data
from imagine.observables.dataset import *

__all__ = ['RepositoryDataset']

class RepositoryDataset(Dataset, metaclass=abc.ABCMeta):
    """
    Base class to be used for datasets in the IMAGINE-datasets repository
    """
    @property
    @req_attr
    def ref(self):
        """
        Bibliographic reference
        
        Example:  'Oppermann et al. (2012) A&A, 542, A93'
        """
        return(self.REF)
    
    @property
    @req_attr
    def ref_url(self):
        """
        URL to the biblographic reference
        (preferably to the NASA ADS entry)
        
        """
        return(self.REF_URL)
    
    @property
    def cache_dir(self):
        """
        Directory where the cache is saved. By default, this corresponds to
        the :py:data:`imagine.datasets` global variable.
        """
        if not hasattr(self, '_cache_dir'):
            self._cache_dir = img_data.cache_dir
        return self._cache_dir

    @cache_dir.setter
    def cache_dir(self, path):
        assert os.path.isdir(path)
        self._cache_dir = path

    @property
    def cache_path(self):
        return os.path.join(self.cache_dir, self.__class__.__name__ + '.hkl')

    def _load_from_cache(self):
        """
        Loads data from disk cache
        """
        if self.cache_dir is not None:
            if os.path.isfile(self.cache_path):
                return hkl.load(self.cache_path)
        return None

    def _save_to_cache(self, data):
        """
        Saves data to disk cache

        Parameters
        ----------
        data
            Data to be dumped in the cache. Any python object is allowed, but
            a numpy array is preferred.
        """
        if self.cache_dir is not None:
            hkl.dump(data, self.cache_path)


    def clean_cache(self):
        if os.path.isfile(self.cache_path):
            os.remove(self.cache_path)
