import requests, io
import numpy as np
import astropy.units as u
from astropy.io import fits
import healpy as hp
import imagine as img
import imagine_datasets as img_data

__all__ = ['Oppermann2012']

class Oppermann2012(img.observables.FaradayDepthHEALPixDataset,
                                img_data.RepositoryDataset):
    def __init__(self, Nside=None):
        # Tries to load from cache
        fd_data = self._load_from_cache()

        # Fetches if needed
        if fd_data is None:
            print('Downloading data..')
            download = requests.get('https://wwwmpa.mpa-garching.mpg.de/ift/faraday/2012/faraday.fits')
            raw_dataset = fits.open(io.BytesIO(download.content))
            # Faraday depth and uncertainty are in the 3rd and 4th cols
            fd_raw = np.array(raw_dataset[3].data.astype(float))
            sigma_fd_raw = np.array(raw_dataset[4].data.astype(float))
            fd_data = fd_raw, sigma_fd_raw
            self._save_to_cache(fd_data)
        else:
            fd_raw, sigma_fd_raw = fd_data

        # Reduces the resolution
        if Nside is not None:
            fd_raw = hp.pixelfunc.ud_grade(fd_raw, Nside)
            sigma_fd_raw = hp.pixelfunc.ud_grade(sigma_fd_raw, Nside)

        # Includes units in the data
        fd_raw *= u.rad/u.m/u.m
        sigma_fd_raw *= u.rad/u.m/u.m

        # Loads into the Dataset
        super().__init__(data=fd_raw, error=sigma_fd_raw)
