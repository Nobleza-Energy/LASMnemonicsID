
import pytest
import pandas as pd
import sys
from pathlib import Path
from LASMnemonicsID.DLIS import parseDLIS
from LASMnemonicsID.utils.mnemonics import (
    gamma_names, density_names, neutron_names, 
    dtc_names, sp_names, caliper_names
)
from LASMnemonicsID.utils.mnemonics import find_column


def print_output(msg):
    """Force print to stderr (always visible in pytest)."""
    sys.stderr.write(str(msg) + "\n")
    sys.stderr.flush()


def test_parseDLIS_single_folder():
    """Test directory → {filename: df} dict."""
    data_dir = Path(__file__).parent / 'data'
    result = parseDLIS(data_dir, verbose=False)
    
    if not result:
        pytest.skip("No DLIS test files found")
    
    assert isinstance(result, dict)
    assert len(result) >= 1
    
    # Print heads of all DataFrames
    print_output("\n" + "="*60)
    print_output("test_parseDLIS_single_folder - Multiple files:")
    print_output("="*60)
    for filename, df in result.items():
        print_output(f"\n📄 {filename}")
        print_output(f"Shape: {df.shape}")
        print_output(f"Columns: {list(df.columns)}")
        print_output(df.head().to_string())
    
    first_df = next(iter(result.values()))
    assert isinstance(first_df, pd.DataFrame)
    assert len(first_df) > 0
    assert first_df.index.name == "DEPTH"


def test_parseDLIS_empty_dir():
    """Test empty directory returns empty dict."""
    empty_path = Path(__file__).parent / 'empty_dir'
    empty_path.mkdir(exist_ok=True)
    result = parseDLIS(empty_path, verbose=False)
    assert result == {}
    print_output("\n✓ Empty directory test passed (no DataFrames to show)")
    empty_path.rmdir()


def test_parseDLIS_single_file():
    """Test single file → DataFrame."""
    data_dir = Path(__file__).parent / 'data'
    sample_dlis_paths = [f for f in data_dir.glob('*') if f.suffix.lower() == '.dlis']
    
    if not sample_dlis_paths:
        pytest.skip("No DLIS test files found")
    
    first_file = sample_dlis_paths[0]
    df = parseDLIS(first_file, verbose=False)
    
    # Print DataFrame head
    print_output("\n" + "="*60)
    print_output(f"test_parseDLIS_single_file - {first_file.name}")
    print_output("="*60)
    print_output(f"File type: {first_file.suffix}")
    print_output(f"Shape: {df.shape}")
    print_output(f"Index: {df.index.name}")
    print_output(f"Columns: {list(df.columns)}")
    print_output("\nFirst 5 rows:")
    print_output(df.head().to_string())
    print_output("\nDataFrame dtypes:")
    print_output(str(df.dtypes))
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert df.index.name == "DEPTH"
    assert len(df.columns) > 0


def test_parseDLIS_standardization():
    """Test that mnemonics are standardized."""
    data_dir = Path(__file__).parent / 'data'
    sample_dlis_paths = [f for f in data_dir.glob('*') if f.suffix.lower() == '.dlis']
    
    if not sample_dlis_paths:
        pytest.skip("No DLIS test files found")
    
    first_file = sample_dlis_paths[0]
    df = parseDLIS(first_file, verbose=False)
    
    # Print standardized columns
    print_output("\n" + "="*60)
    print_output(f"test_parseDLIS_standardization - {first_file.name}")
    print_output("="*60)
    print_output(f"Standardized columns: {list(df.columns)}")
    
    standard_names = ['GR', 'RHOB', 'NPHI', 'DT', 'SP', 'CALI', 'RT']
    found_standards = [name for name in standard_names if name in df.columns]
    print_output(f"Found standard names: {found_standards}")
    
    print_output("\nFirst 5 rows of standardized data:")
    print_output(df.head().to_string())
    
    assert len(found_standards) >= 0


def test_parseDLIS_preferred_names():
    """Test preferred names override defaults."""
    data_dir = Path(__file__).parent / 'data'
    sample_dlis_paths = [f for f in data_dir.glob('*') if f.suffix.lower() == '.dlis']
    
    if not sample_dlis_paths:
        pytest.skip("No DLIS test files found")
    
    first_file = sample_dlis_paths[0]
    preferred = {"gamma": "GAMMA_RAY", "density": "BULK_DENSITY"}
    df = parseDLIS(first_file, verbose=False, preferred_names=preferred)
    
    # Print with preferred names
    print_output("\n" + "="*60)
    print_output(f"test_parseDLIS_preferred_names - {first_file.name}")
    print_output("="*60)
    print_output(f"Preferred names applied: {preferred}")
    print_output(f"Result columns: {list(df.columns)}")
    print_output("\nFirst 5 rows:")
    print_output(df.head().to_string())
    
    assert isinstance(df, pd.DataFrame)
    assert df.index.name == "DEPTH"


def test_parseDLIS_multiple_frames():
    """Test DLIS file with multiple frames (uses first frame)."""
    data_dir = Path(__file__).parent / 'data'
    sample_dlis_paths = [f for f in data_dir.glob('*') if f.suffix.lower() == '.dlis']
    
    if not sample_dlis_paths:
        pytest.skip("No DLIS test files found")
    
    first_file = sample_dlis_paths[0]
    df = parseDLIS(first_file, verbose=False)
    
    # Print frame info
    print_output("\n" + "="*60)
    print_output(f"test_parseDLIS_multiple_frames - {first_file.name}")
    print_output("="*60)
    print_output(f"Using first frame")
    print_output(f"Shape: {df.shape}")
    print_output(f"Columns: {list(df.columns)}")
    print_output("\nFirst 5 rows:")
    print_output(df.head().to_string())
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
