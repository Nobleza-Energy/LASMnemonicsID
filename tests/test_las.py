
import pytest
import pandas as pd
from pathlib import Path
from LASMnemonicsID.LAS import parseLAS

def test_parseLAS_single_folder(sample_las_paths):
    result = parseLAS(sample_las_paths[0].parent, verbose=False)  # tests/data/
    assert isinstance(result, dict)  # Multiple files → {folder: {well: df}}
    assert len(result) == 1  # 1 folder: 'data'
    data_folder = next(iter(result))
    assert data_folder == 'data'
    wells = result[data_folder]
    assert len(wells) >= 5  # Your 5 LAS files
    first_df = next(iter(wells.values()))
    assert isinstance(first_df, pd.DataFrame)
    assert 'GR' in first_df.columns  # GR standardization

def test_parseLAS_empty_dir():
    result = parseLAS(Path(__file__).parent / 'empty_dir', verbose=False)
    assert result == {}
