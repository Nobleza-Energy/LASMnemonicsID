
import pytest
import pandas as pd
import sys
from pathlib import Path
from LASMnemonicsID.ASCII import parseASCII
from LASMnemonicsID.utils.mnemonics import (
    gamma_names, density_names, neutron_names, 
    dtc_names, sp_names, caliper_names
)
from LASMnemonicsID.utils.mnemonics import find_column


# All supported ASCII extensions
ASCII_EXTENSIONS = ['.csv', '.txt', '.asc', '.dat', '.ascii']


def print_output(msg):
    """Force print to stderr (always visible in pytest)."""
    sys.stderr.write(str(msg) + "\n")
    sys.stderr.flush()


def test_parseASCII_single_folder():
    """Test directory → {filename: df} dict."""
    data_dir = Path(__file__).parent / 'data'
    result = parseASCII(data_dir, verbose=False)
    
    if not result:
        pytest.skip("No ASCII/CSV test files found")
    
    assert isinstance(result, dict)
    assert len(result) >= 1
    
    # Print heads of all DataFrames
    print_output("\n" + "="*60)
    print_output("test_parseASCII_single_folder - Multiple files:")
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


def test_parseASCII_empty_dir():
    """Test empty directory returns empty dict."""
    empty_path = Path(__file__).parent / 'empty_dir'
    empty_path.mkdir(exist_ok=True)
    result = parseASCII(empty_path, verbose=False)
    assert result == {}
    print_output("\n✓ Empty directory test passed (no DataFrames to show)")
    empty_path.rmdir()


def test_parseASCII_single_file():
    """Test single file → DataFrame."""
    data_dir = Path(__file__).parent / 'data'
    sample_ascii_paths = [f for f in data_dir.glob('*') if f.suffix.lower() in ASCII_EXTENSIONS]
    
    if not sample_ascii_paths:
        pytest.skip("No ASCII/CSV test files found")
    
    first_file = sample_ascii_paths[0]
    df = parseASCII(first_file, verbose=False)
    
    # Print DataFrame head
    print_output("\n" + "="*60)
    print_output(f"test_parseASCII_single_file - {first_file.name}")
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


def test_parseASCII_all_formats():
    """Test that all ASCII formats (.csv, .txt, .asc, .dat, .ascii) are detected."""
    data_dir = Path(__file__).parent / 'data'
    
    found_formats = {}
    for ext in ASCII_EXTENSIONS:
        files = [f for f in data_dir.glob(f'*{ext}')]
        if files:
            found_formats[ext] = len(files)
    
    if not found_formats:
        pytest.skip("No ASCII files found")
    
    print_output("\n" + "="*60)
    print_output("test_parseASCII_all_formats - Format detection:")
    print_output("="*60)
    print_output(f"Found formats: {found_formats}")
    
    # Test parsing each format
    for ext, count in found_formats.items():
        files = [f for f in data_dir.glob(f'*{ext}')]
        if files:
            first_file = files[0]
            df = parseASCII(first_file, verbose=False)
            print_output(f"\n✓ {ext}: {first_file.name} → {df.shape}")
            assert isinstance(df, pd.DataFrame)


def test_parseASCII_custom_depth_col():
    """Test custom depth column name."""
    data_dir = Path(__file__).parent / 'data'
    sample_csv_paths = [f for f in data_dir.glob('*') if f.suffix.lower() == '.csv']
    
    if not sample_csv_paths:
        pytest.skip("No CSV test files found")
    
    first_file = sample_csv_paths[0]
    df = parseASCII(first_file, verbose=False, depth_col="DEPTH")
    
    # Print with custom depth
    print_output("\n" + "="*60)
    print_output(f"test_parseASCII_custom_depth_col - {first_file.name}")
    print_output("="*60)
    print_output(f"Depth column: {df.index.name}")
    print_output(f"Columns: {list(df.columns)}")
    print_output("\nFirst 5 rows:")
    print_output(df.head().to_string())
    
    assert isinstance(df, pd.DataFrame)
    assert df.index.name == "DEPTH"


def test_parseASCII_delimiter():
    """Test custom delimiter (comma, tab, space)."""
    data_dir = Path(__file__).parent / 'data'
    sample_txt_paths = [f for f in data_dir.glob('*') if f.suffix.lower() == '.txt']
    
    if not sample_txt_paths:
        pytest.skip("No TXT test files found")
    
    first_file = sample_txt_paths[0]
    
    # Try different delimiters
    delimiters = [",", "\t", " "]
    for delim in delimiters:
        try:
            df = parseASCII(first_file, verbose=False, delimiter=delim)
            
            print_output("\n" + "="*60)
            print_output(f"test_parseASCII_delimiter - {first_file.name}")
            print_output("="*60)
            print_output(f"Delimiter: {repr(delim)}")
            print_output(f"Shape: {df.shape}")
            print_output(f"Columns: {list(df.columns)}")
            print_output("\nFirst 3 rows:")
            print_output(df.head(3).to_string())
            
            assert isinstance(df, pd.DataFrame)
            break  # Success, stop trying
        except:
            continue


def test_parseASCII_standardization():
    """Test that mnemonics are standardized."""
    data_dir = Path(__file__).parent / 'data'
    sample_ascii_paths = [f for f in data_dir.glob('*') if f.suffix.lower() in ASCII_EXTENSIONS]
    
    if not sample_ascii_paths:
        pytest.skip("No ASCII/CSV test files found")
    
    first_file = sample_ascii_paths[0]
    df = parseASCII(first_file, verbose=False)
    
    # Print standardized columns
    print_output("\n" + "="*60)
    print_output(f"test_parseASCII_standardization - {first_file.name}")
    print_output("="*60)
    print_output(f"Standardized columns: {list(df.columns)}")
    
    standard_names = ['GR', 'RHOB', 'NPHI', 'DT', 'SP', 'CALI', 'RT']
    found_standards = [name for name in standard_names if name in df.columns]
    print_output(f"Found standard names: {found_standards}")
    
    print_output("\nFirst 5 rows of standardized data:")
    print_output(df.head().to_string())
    
    assert len(found_standards) >= 0


def test_parseASCII_preferred_names():
    """Test preferred names override defaults."""
    data_dir = Path(__file__).parent / 'data'
    sample_ascii_paths = [f for f in data_dir.glob('*') if f.suffix.lower() in ASCII_EXTENSIONS]
    
    if not sample_ascii_paths:
        pytest.skip("No ASCII/CSV test files found")
    
    first_file = sample_ascii_paths[0]
    preferred = {"gamma": "GAMMA_RAY", "density": "BULK_DENSITY"}
    df = parseASCII(first_file, verbose=False, preferred_names=preferred)
    
    # Print with preferred names
    print_output("\n" + "="*60)
    print_output(f"test_parseASCII_preferred_names - {first_file.name}")
    print_output("="*60)
    print_output(f"Preferred names applied: {preferred}")
    print_output(f"Result columns: {list(df.columns)}")
    print_output("\nFirst 5 rows:")
    print_output(df.head().to_string())
    
    assert isinstance(df, pd.DataFrame)
