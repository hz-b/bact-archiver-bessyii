'''Retrieve bpm data from archiver and export them

Todo:
    Shall be bpm_data generalised?
'''
from bact_archiver.archiver import ArchiverInterface
import xarray as xr
import h5netcdf
import numpy as np
import datetime
import logging
from typing import Sequence

logger = logging.getLogger('bact_archiver')


def bpm_data(archiver: ArchiverInterface,
             t0: datetime.datetime, t1: datetime.datetime, *,
             bpm_names: Sequence[str], bpm_pos: Sequence[float]) -> xr.Dataset:
    '''Retrieve bpm data for time interval and store them as data set

    Args:
        archiver:  archiver interface
        t0:        start time of interval
        t1:        end time of interval
        bpm_names: names of the beam position monitors

    This function retrieves the bpm data from the archiver. It uses the names used
    at BESSY II archiver.

    * x plane
    * y plane
    * state: if bpm is active

    Warning:
        The code does not check if the path already exists. Netcdf
        will complain if the file is locked (typically used by an
        other instance, read access also locks).
    '''

    # Get the dataframes
    kwargs = dict(t0=t0, t1=t1, time_format='datetime')
    bpm_x = archiver.getData('FOFBCC:fastBpmX', **kwargs)
    bpm_y = archiver.getData('FOFBCC:fastBpmY', **kwargs)
    bpm_state = archiver.getData('FOFBCC:fastStateBpm', **kwargs)

    if bpm_x.shape[0] < bpm_y.shape[0]:
        index_to_use = bpm_x.index
    else:
        index_to_use = bpm_y.index
    n_rows = len(index_to_use)

    data = xr.DataArray(
        dims=['time', 'bpm', 'plane'],
        coords=[index_to_use.values, bpm_names, ['x', 'y']],
        name='bpm_data'
    )
    data.loc[dict(plane='x')] = bpm_x[:n_rows]
    data.loc[dict(plane='y')] = bpm_y[:n_rows]

    state = xr.DataArray(
        data=bpm_state.astype(np.bool), dims=['time2', 'bpm'],
        coords=[bpm_state.index.values, bpm_names],
        name='bpm_state'
    )

    valid_bpm = state.isel(time2=0)
    bpmpos_a = xr.DataArray(dims=['bpm'], coords=[bpm_names], name='bpm_pos')
    bpmpos_a.loc[dict(bpm=valid_bpm)] = bpm_pos

    dataset = xr.Dataset(dict(data=data, state=state, pos=bpmpos_a))
    return dataset


def export_bpm_data(*args, save_path: str, **kwargs) -> None:
    '''Retrieve bpm data and store them in the save path

    For details of the arguments and keyword arguments see
    :func:`bpm_data`

    Args:
        save_path: path to export the data to.
    '''

    dataset = bpm_data(*args, **kwargs)
    dataset.to_netcdf(save_path, engine='h5netcdf')


__all__ = ['bpm_data', 'export_bpm_data']
