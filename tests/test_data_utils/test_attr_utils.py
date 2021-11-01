import numpy as np
import xarray as xr

from daops.data_utils.attr_utils import add_global_attrs_if_needed
from daops.data_utils.attr_utils import edit_global_attrs
from daops.data_utils.attr_utils import edit_var_attrs
from daops.data_utils.attr_utils import remove_fill_values
from tests._common import MINI_ESGF_MASTER_DIR


def test_edit_var_attrs(load_esgf_test_data):
    ds = xr.open_mfdataset(
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_EC-EARTH_historical_r1i1p1_185001-185912.nc",
        combine="by_coords",
        use_cftime=True,
    )

    assert ds.lat.attrs["standard_name"] == "latitude"
    assert ds.lat.attrs["long_name"] == "latitude"

    operands = {
        "var_id": "lat",
        "attrs": {
            "long_name": "False long name",
            "standard_name": "fake_standard_name",
        },
    }
    ds_change_var_attrs = edit_var_attrs(ds, **operands)
    assert ds_change_var_attrs.lat.attrs["standard_name"] == "fake_standard_name"
    assert ds_change_var_attrs.lat.attrs["long_name"] == "False long name"


def test_edit_global_attrs(load_esgf_test_data):
    ds = xr.open_mfdataset(
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_EC-EARTH_historical_r1i1p1_185001-185912.nc",
        combine="by_coords",
        use_cftime=True,
    )

    assert (
        ds.attrs["comment"]
        == "Equilibrium reached after preindustrial spin-up after which data were output starting with nominal date of January 1850"
    )
    assert ds.attrs["title"] == "EC-EARTH model output prepared for CMIP5 historical"
    assert ds.attrs.get("test", None) is None

    operands = {
        "attrs": {
            "comment": "this is a test commment",
            "title": "this is a test title",
            "test": "this is a new test attribute",
        }
    }
    ds_change_global_attrs = edit_global_attrs(ds, **operands)

    assert ds_change_global_attrs.attrs["comment"] == "this is a test commment"
    assert ds_change_global_attrs.attrs["title"] == "this is a test title"
    assert ds_change_global_attrs.attrs["test"] == "this is a new test attribute"


def test_add_global_attrs_if_needed(load_esgf_test_data):
    ds = xr.open_mfdataset(
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_EC-EARTH_historical_r1i1p1_185001-185912.nc",
        combine="by_coords",
        use_cftime=True,
    )

    assert (
        ds.attrs["comment"]
        == "Equilibrium reached after preindustrial spin-up after which data were output starting with nominal date of January 1850"
    )
    assert ds.attrs["title"] == "EC-EARTH model output prepared for CMIP5 historical"
    assert ds.attrs.get("test", None) is None

    operands = {
        "attrs": {
            "comment": "this is a test commment",
            "title": "this is a test title",
            "test": "this is a new test attribute",
        }
    }
    ds_change_global_attrs = add_global_attrs_if_needed(ds, **operands)

    assert (
        ds_change_global_attrs.attrs["comment"]
        == "Equilibrium reached after preindustrial spin-up after which data were output starting with nominal date of January 1850"
    )
    assert (
        ds_change_global_attrs.attrs["title"]
        == "EC-EARTH model output prepared for CMIP5 historical"
    )
    assert ds_change_global_attrs.attrs["test"] == "this is a new test attribute"


def test_remove_fill_values(load_esgf_test_data):
    ds = xr.open_mfdataset(
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_EC-EARTH_historical_r1i1p1_185001-185912.nc",
        combine="by_coords",
        use_cftime=True,
    )

    assert ds.lat.encoding.get("_FillValue", "") == ""
    assert ds.lat.encoding.get("_FillValue", "") == ""
    assert ds.lat.encoding.get("_FillValue", "") == ""

    operands = {}
    ds = remove_fill_values(ds, **operands)

    assert ds.lat.encoding.get("_FillValue", "") is None
    assert ds.lat.encoding.get("_FillValue", "") is None
    assert ds.lat.encoding.get("_FillValue", "") is None