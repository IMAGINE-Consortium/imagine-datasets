import os
import imagine
import imagine_datasets as img_data
from imagine.observables.dataset import *
import hickle as hkl

__all__ = ['RepositoryDataset']

class RepositoryDataset(Dataset):

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
