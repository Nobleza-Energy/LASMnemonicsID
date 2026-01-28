
import lasio
import pytest
import pandas as pd
from pathlib import Path
from LASMnemonicsID.LAS import parseLAS
from LASMnemonicsID.utils.mnemonics import (
    gamma_names, density_names, neutron_names, 
    dtc_names, sp_names, caliper_names  # All types
)
from LASMnemonicsID.utils.mnemonics import find_column


def test_parseLAS_single_folder():
    """Test directory → {filename: df} dict."""
    data_dir = Path(__file__).parent / 'data'
    result = parseLAS(data_dir, verbose=False)
    assert isinstance(result, dict)
    assert len(result) >= 1  # Adaptive: any # files
    first_df = next(iter(result.values()))
    assert isinstance(first_df, pd.DataFrame)
    assert len(first_df) > 0
    assert 'GR' in first_df.columns  # Standardization ✓


def test_parseLAS_empty_dir():
    empty_path = Path(__file__).parent / 'empty_dir'
    empty_path.mkdir(exist_ok=True)
    result = parseLAS(empty_path, verbose=False)
    assert result == {}
    empty_path.rmdir()  # Cleanup


def test_parseLAS_single_file():
    """Test single file → DataFrame."""
    data_dir = Path(__file__).parent / 'data'
    sample_las_paths = list(data_dir.glob('*.las'))
    first_file = sample_las_paths[0]
    df = parseLAS(first_file, verbose=False)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert 'GR' in df.columns  # Standardization ✓
