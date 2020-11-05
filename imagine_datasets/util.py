"""
This module contains general purpose
"""
import healpy as hp

def adjust_nside(Nside, hp_map, hp_variance=None):
    """
    Reduces the resolution of a HEALPix map

    Parameters
    ----------
    Nside : int or None
        Nside of the map. If None, the original maps are returned unchanged.
    hp_map : numpy.ndarray
        Numpy array containing the map.
    hp_variance : numpy.ndarray
        Numpy array containing the variances of `hp_map`.

    Returns
    -------
    hp_map : numpy.ndarray
        Numpy array containing the downgraded map.
    hp_variance : numpy.ndarray
        Numpy array containing the variances of `hp_map`
        (returned only if originally hp_variance was not `None`).
    """
    if Nside is None:
        if hp_variance is not None:
            return hp_map, hp_variance
        else:
            return hp_map

    Nside_original = hp.get_nside(hp_map)
    assert Nside_original > Nside

    hp_map = hp.ud_grade(hp_map, Nside)

    if hp_variance is not None:
        assert Nside_original == hp.get_nside(hp_variance)
        hp_variance = hp.ud_grade(hp_variance, Nside)

        # Rescales the variance accounting for the difference in resolution
        # (the un
        rescaler = (Nside/Nside_original)**2
        hp_variance *= rescaler

        return hp_map, hp_variance
    else:
        return hp_map
