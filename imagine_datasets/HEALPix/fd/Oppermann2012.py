import requests, io
import numpy as np
import astropy.units as u
from astropy.io import fits
import imagine as img
import imagine_datasets as img_data

__all__ = ['Oppermann2012']

class Oppermann2012(img.observables.FaradayDepthHEALPixDataset,
                    img_data.RepositoryDataset):
    """
    Dataset corresponding to Oppermann et al. (2012) Faraday Depth map

    Parameters
    ----------
    Nside : int, optional
        Nside of the maps. If absent, the original maps are returned unchanged.
    """
    REF = 'Oppermann et al. (2012) A&A, 542, A93'
    REF_URL = 'https://ui.adsabs.harvard.edu/abs/2012A&A...542A..93O/abstract'

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

        # Reduces the resolution (if needed)
        fd_raw, sigma_fd_raw = img_data.util.adjust_nside(Nside, fd_raw,
                                                          sigma_fd_raw)

        # Includes units in the data
        fd_raw = fd_raw << u.rad/u.m/u.m
        sigma_fd_raw = sigma_fd_raw << u.rad/u.m/u.m

        # Loads into the Dataset
        super().__init__(data=fd_raw, error=sigma_fd_raw)
