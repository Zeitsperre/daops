import os
import tempfile
from pathlib import Path

from jinja2 import Template

TESTS_HOME = os.path.abspath(os.path.dirname(__file__))
TESTS_OUTPUTS = os.path.join(TESTS_HOME, "_outputs")
ROOCS_CFG = os.path.join(tempfile.gettempdir(), "roocs.ini")

MINI_ESGF_CACHE_DIR = Path.home() / ".mini-esgf-data"
MINI_ESGF_MASTER_DIR = os.path.join(MINI_ESGF_CACHE_DIR, "master")

try:
    os.mkdir(TESTS_OUTPUTS)
except Exception:
    pass


def write_roocs_cfg():
    cfg_templ = """
    [project:cmip5]
    base_dir = {{ base_dir }}/test_data/badc/cmip5/data/cmip5

    [project:cmip6]
    base_dir = {{ base_dir }}/test_data/badc/cmip6/data/CMIP6

    [project:cordex]
    base_dir = {{ base_dir }}/test_data/badc/cordex/data/cordex

    [project:c3s-cmip5]
    base_dir = {{ base_dir }}/test_data/gws/nopw/j04/cp4cds1_vol1/data/c3s-cmip5

    [project:c3s-cmip6]
    base_dir = {{ base_dir }}/test_data/badc/cmip6/data/CMIP6

    [project:c3s-cordex]
    base_dir = {{ base_dir }}/test_data/gws/nopw/j04/cp4cds1_vol1/data/c3s-cordex

    [project:cru_ts]
    base_dir = {{ ceda_base_dir }}/archive/badc/cru/data/cru_ts
    file_name_template = {__derive__var_id}_{frequency}_{__derive__time_range}.{__derive__extension}
    fixed_path_mappings =
        cru_ts.4.04.cld:cru_ts_4.04/data/cld/*.nc
        cru_ts.4.04.dtr:cru_ts_4.04/data/dtr/*.nc
        cru_ts.4.04.frs:cru_ts_4.04/data/frs/*.nc
        cru_ts.4.04.pet:cru_ts_4.04/data/pet/*.nc
        cru_ts.4.04.pre:cru_ts_4.04/data/pre/*.nc
        cru_ts.4.04.tmn:cru_ts_4.04/data/tmn/*.nc
        cru_ts.4.04.tmp:cru_ts_4.04/data/tmp/*.nc
        cru_ts.4.04.tmx:cru_ts_4.04/data/tmx/*.nc
        cru_ts.4.04.vap:cru_ts_4.04/data/vap/*.nc
        cru_ts.4.04.wet:cru_ts_4.04/data/wet/*.nc
    attr_defaults =
        frequency:mon
    facet_rule = project version_major version_minor variable
    """
    cfg = Template(cfg_templ).render(base_dir=MINI_ESGF_MASTER_DIR)
    with open(ROOCS_CFG, "w") as fp:
        fp.write(cfg)

    # point to roocs cfg in environment
    os.environ["ROOCS_CONFIG"] = ROOCS_CFG
