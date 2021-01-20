import os

import pytest
import xarray as xr

from daops import CONFIG
from daops.ops.average import average_over_dims

CMIP5_IDS = [
    "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas",
    "cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh",
]


def _check_output_nc(result, fname="output_001.nc"):
    assert fname in [os.path.basename(_) for _ in result.file_uris]


@pytest.mark.online
def test_average_time(tmpdir):
    result = average_over_dims(
        CMIP5_IDS[1],
        dims=["time"],
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)
    print(ds)
