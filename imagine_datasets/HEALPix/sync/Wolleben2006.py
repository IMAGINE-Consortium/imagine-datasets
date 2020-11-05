# import requests, io
# import numpy as np
# import astropy.units as u
# from astropy.io import fits
# import healpy as hp
# import imagine as img
# import imagine_datasets as img_data


# __all__ = ['Wolleben2006']


# class Wolleben2006(img.observables.FaradayDepthHEALPixDataset,
#                    img_data.RepositoryDataset):

#     REF = 'Wolleben et al (2006) A&A, 448'
#     REF_URL = 'https://ui.adsabs.harvard.edu/abs/2006A&A...448..411W/abstract'

#     def __init__(self, Nside=None):
#         # Tries to load from cache
#         full_data = self._load_from_cache()
        
#         # Fetches if needed
#         if full_data is None:
#             print('Downloading data..')
#             tabel1 = requests.get('https://cdsarc.unistra.fr/ftp/J/A+A/448/411/fits/q_gal.fit')
#             tabel2 = requests.get('https://cdsarc.unistra.fr/viz-bin/nph-Cat/fits?J/ApJ/714/1170/table2.dat')
            
            
            
#                     raise NotImplementedError
        
# # Fetches the relevant catalogue from Vizier
# # (see https://astroquery.readthedocs.io/en/latest/vizier/vizier.html for details)
# catalog = Vizier.get_catalogs('J/ApJ/714/1170')[0]
# catalog[:3] # Shows only first rows