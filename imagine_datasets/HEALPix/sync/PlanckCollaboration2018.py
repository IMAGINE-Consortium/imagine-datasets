import requests, io
import numpy as np
import astropy.units as apu
from astropy.io import fits
import healpy as hp
import imagine as img
import imagine_datasets as img_data

__all__ = ['Planck2018_Commander_Q', 'Planck2018_Commander_U',
           'Planck2018_LFI_Q_30GHz', 'Planck2018_LFI_U_30GHz',
           'Planck2018_LFI_I_30GHz']


class _Planck2018_LFI_30GHz_base(img.observables.SynchrotronHEALPixDataset,
                                 img_data.RepositoryDataset):

    REF = 'Planck Collaboration, 2020, A&A, 641, A2'
    REF_URL = 'https://ui.adsabs.harvard.edu/abs/2020A%26A...641A...2P/abstract'
    INFO = 'https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/Frequency_maps'
    FREQ = 30*apu.GHz

    def __init__(self, Nside=None):
        # Tries to load from cache
        data_pair = self._load_from_cache()

        if data_pair is None:
            print('Downloading Planck 2018 LFI 30 GHz data')
            download = requests.get('https://pla.esac.esa.int/pla-sl/data-action?MAP.MAP_OID=13737')
            HDUlist = fits.open(io.BytesIO(download.content))

            sync_maps = {}
            # See https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/Frequency_maps#FITS_file_structure
            for name, i_field in (('I', 1), ('Q', 2), ('U', 3),
                                  ('I_var', 5), ('Q_var', 8), ('U_var', 10)):
                print('Preparing Stokes ' + name)
                sync_maps[name] = hp.fitsfunc.read_map(HDUlist, field=i_field-1)

            # Groups the pairs Q+Q_var, U+U_var, I+I_var
            sync_data = {'Planck2018_LFI_'+x+'_30GHz': (sync_maps[x], sync_maps[x+'_var'])
                        for x in ('I', 'Q', 'U')}

            for name, data in sync_data.items():
                self._save_to_cache(data, name=name)
            data_pair = sync_data[self.__class__.__name__]

        value, variance = data_pair

        # Reduces the resolution (if needed)
        value, variance = img_data.util.adjust_nside(Nside, value, variance)

        # Includes units in the data
        value = value << apu.K
        variance = variance << apu.K*apu.K

        # Loads into the Dataset
        super().__init__(data=value, frequency=self.FREQ, typ=self.TYPE,
                         error=np.sqrt(variance))


class Planck2018_LFI_I_30GHz(_Planck2018_LFI_30GHz_base):
    """
    Planck 2018 LFI 30 GHz Stokes I data

    Parameters
    ----------
    Nside : int, optional
        Nside of the maps. If absent, the original maps are returned unchanged.
    """
    TYPE = 'I'


class Planck2018_LFI_Q_30GHz(_Planck2018_LFI_30GHz_base):
    """
    Planck 2018 LFI 30 GHz Stokes Q data

    Parameters
    ----------
    Nside : int, optional
        Nside of the maps. If absent, the original maps are returned unchanged.
    """
    TYPE = 'Q'


class Planck2018_LFI_U_30GHz(_Planck2018_LFI_30GHz_base):
    """
    Planck 2018 LFI 30 GHz Stokes U data

    Parameters
    ----------
    Nside : int, optional
        Nside of the maps. If absent, the original maps are returned unchanged.
    """
    TYPE = 'U'


class _Planck2018_Commander_base(img.observables.SynchrotronHEALPixDataset,
                           img_data.RepositoryDataset):

    REF = 'Planck Collaboration (2020) A&A, 641, A4'
    REF_URL = 'https://ui.adsabs.harvard.edu/abs/2020A%26A...641A...4P/abstract'
    INFO = 'https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/Foreground_maps#Commander-derived_astrophysical_foreground_maps'
    FREQ = 30*apu.GHz

    def __init__(self, Nside=None):
        # Tries to load from cache
        sync_data = self._load_from_cache()

        if sync_data is None:
            print('Downloading Planck 2018 Commander data')
            download = requests.get('http://pla.esac.esa.int/pla/aio/product-action?MAP.MAP_ID=COM_CompMap_QU-synchrotron-commander_2048_R3.00_full.fits')

            HDUlist = fits.open(io.BytesIO(download.content))

            # See https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/Foreground_maps#Synchrotron_emission
            for name, i_field in (('Planck2018_Commander_Q', 1),
                                  ('Planck2018_Commander_U', 2)):
                dataset = hp.fitsfunc.read_map(HDUlist, field=i_field-1)
                self._save_to_cache(dataset, name=name)
                #print(name)
                if name == self.__class__.__name__:
                    sync_data = dataset

        # Gets the variance from _another_ dataset
        dset_LFI = eval('Planck2018_LFI_' + self.TYPE + '_30GHz')(Nside)
        error = dset_LFI._error

        # Reduces the resolution (if needed) and adds units
        sync_data = img_data.util.adjust_nside(Nside, sync_data) << apu.K

        # Loads into the Dataset
        super().__init__(data=sync_data, frequency=self.FREQ, typ=self.TYPE,
                         error=error)


class Planck2018_Commander_Q(_Planck2018_Commander_base):
    """
    Planck 2018 synchrotron component of Stokes Q data, separated from
    dust emission data using the Commander method

    The same variances as `Planck2018_LFI_Q_30GHz` are adopted

    Parameters
    ----------
    Nside : int, optional
        Nside of the maps. If absent, the original maps are returned unchanged.
    """
    TYPE='Q'


class Planck2018_Commander_U(_Planck2018_Commander_base):
    """
    Planck 2018 synchrotron component of Stokes U data, separated from
    dust emission data using the Commander method

    The same variances as `Planck2018_LFI_U_30GHz` are adopted

    Parameters
    ----------
    Nside : int, optional
        Nside of the maps. If absent, the original maps are returned unchanged.
    """
    TYPE='U'
