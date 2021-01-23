import os
import xarray as xr

from daops import CONFIG
from daops.ops.subset import subset

CRU_TS_WET_ID = 'cru_ts.4.04.wet'


def _check_output_nc(result, fname="output_001.nc"):
    assert fname in [os.path.basename(_) for _ in result.file_uris]


def test_subset_t(tmpdir, load_ceda_test_data):
    result = subset(
        CRU_TS_WET_ID,
        time=("1955-01-16", "2011-12-16"),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)
    assert ds.time.shape == (684,)
