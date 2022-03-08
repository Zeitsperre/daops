import os

import pytest
import xarray as xr
from roocs_utils.exceptions import InvalidParameterValue

from daops import CONFIG
from daops.ops.regrid import regrid
from tests._common import MINI_ESGF_MASTER_DIR

CMIP5_IDS = [
    "cmip5.output1.MOHC.HadGEM2-ES.rcp85.day.land.day.r1i1p1.latest.mrsos",
    "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas",
    "cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh",
]


def _check_output_nc(result, fname="output_001.nc"):
    assert fname in [os.path.basename(_) for _ in result.file_uris]


@pytest.mark.online
def test_regrid_basic(tmpdir):
    fpath = (
        f"{MINI_ESGF_MASTER_DIR}/"
        "test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/day/"
        "land/day/r1i1p1/latest/mrsos/mrsos_day_HadGEM2-ES_rcp85_r1i1p1_20051201.nc"
    )

    ds = xr.open_dataset(
        fpath,
        use_cftime=True,
    )

    assert ds.lat.size == 145
    assert ds.lon.size == 192

    assert ds.lat.values[1] - ds.lat.values[0] == 1.25
    assert ds.lon.values[1] - ds.lon.values[0] == 1.875

    result = regrid(
        CMIP5_IDS[0],
        method="nearest_s2d",
        adaptive_masking_threshold=0.5,
        grid="1deg",
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)

    ds_regrid = xr.open_dataset(result.file_uris[0], use_cftime=True)

    assert ds_regrid.lat.size == 180
    assert ds_regrid.lon.size == 360

    assert ds_regrid.lat.values[1] - ds_regrid.lat.values[0] == 1.0
    assert ds_regrid.lon.values[1] - ds_regrid.lon.values[0] == 1.0

    assert ds_regrid.regrid_operation == "nearest_s2d_145x192_180x360_peri"
