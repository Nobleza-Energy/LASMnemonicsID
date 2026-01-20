
import pytest
import lasio
import pandas as pd
from pathlib import Path
from LASMnemonicsID.LAS import parseLAS

def test_parseLAS_single_file(single_las_path):
    result = parseLAS(single_las_path.parent, verbose=False)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert len(result) > 0
    assert 'GR' in result.columns or any('GR' in col for col in result.columns)

def test_parseLAS_multiple_files(sample_las_paths):
    result = parseLAS(sample_las_paths[0].parent, verbose=False)
    assert isinstance(result, dict)
    assert len(result) > 0
    first_folder = next(iter(result))
    assert isinstance(result[first_folder], dict)
    first_well = next(iter(result[first_folder]))
    df = result[first_folder][first_well]
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_no_files():
    from tempfile import mkdtemp
    import shutil
    temp_dir = Path(mkdtemp())
    result = parseLAS(temp_dir, verbose=False)
    assert result == {}
    shutil.rmtree(temp_dir)

def test_las_read_errors(single_las_path):
    # Test error handling (create invalid LAS for full coverage)
    pass
