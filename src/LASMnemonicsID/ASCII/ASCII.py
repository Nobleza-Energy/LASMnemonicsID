
import LASMnemonicsID.utils.mnemonics as mnm
from LASMnemonicsID.utils.mnemonics import (
    gamma_names,
    sp_names,
    caliper_names,
    deepres_names,
    rxo_names,
    density_names,
    density_correction_names,
    neutron_names,
    dtc_names,
    dts_names,
    pe_names,
)
import os
import pandas as pd
from pathlib import Path

# Import helper functions from LAS module
from ..LAS.LAS import create_mnemonic_dict, _standardize_all_curves


def parseASCII(input_path, verbose=True, preferred_names=None, depth_col="DEPTH", delimiter=","):
    """
    Parse ASCII/CSV/TXT well log file or all in directory → DataFrame or {filename: df}.
    
    Args:
        input_path (str/Path): ASCII/CSV/TXT file or directory
        verbose (bool): Print info
        preferred_names (dict, optional): Mapping of curve types to preferred column names.
            Example: {"deepres": "RT", "gamma": "GR"}
            If not provided, defaults to standard petrophysical names.
        depth_col (str): Name of depth column (default: "DEPTH")
        delimiter (str): CSV delimiter (default: ",")
        
    Returns:
        DataFrame (single) or dict {filename: df} (multiple/dir)
    """
    input_path = Path(input_path)
    
    # Define default standard names
    std_names = {
        "gamma": "GR",
        "sp": "SP",
        "caliper": "CALI",
        "deepres": "RT",
        "rxo": "RXO",
        "density": "RHOB",
        "density_correction": "DRHO",
        "neutron": "NPHI",
        "dtc": "DT",
        "dts": "DTS",
        "pe": "PEF"
    }
    
    # Update with user preferences if provided
    if preferred_names:
        std_names.update(preferred_names)
    
    # All supported ASCII extensions (case-insensitive)
    ascii_extensions = ['.csv', '.txt', '.asc', '.dat', '.ascii']
    
    # Case 1: Single File
    if input_path.is_file() and input_path.suffix.lower() in ascii_extensions:
        df = _read_single_ascii(input_path, verbose, std_names, depth_col, delimiter)
        return df if df is not None else None
    
    # Case 2: Directory (Recursive) - CASE-INSENSITIVE
    ascii_files = [f for f in input_path.rglob("*") if f.suffix.lower() in ascii_extensions]
    if not ascii_files:
        if verbose:
            print(f"No ASCII/CSV files found in {input_path}")
        return {}
    
    ascii_dict = {}
    for ascii_file in ascii_files:
        df = _read_single_ascii(ascii_file, verbose, std_names, depth_col, delimiter)
        if df is not None:
            filename = ascii_file.name
            ascii_dict[filename] = df
    
    # Return single DF if only 1 file found, else dict
    if len(ascii_dict) == 1:
        return next(iter(ascii_dict.values()))
    
    return ascii_dict


def _read_single_ascii(ascii_file_path, verbose, std_names, depth_col, delimiter):
    """Read single ASCII/CSV file to DataFrame and standardize ALL curves."""
    try:
        # Try reading the file
        df = pd.read_csv(ascii_file_path, delimiter=delimiter)
        
        if df.empty:
            if verbose:
                print(f"✗ Empty DataFrame: {ascii_file_path.name}")
            return None
        
        # Handle depth column (case-insensitive)
        depth_cols = [col for col in df.columns if col.upper() == depth_col.upper()]
        if depth_cols:
            df.set_index(depth_cols[0], inplace=True)
        else:
            # Use first column as depth
            df.set_index(df.columns[0], inplace=True)
        
        # Ensure index is float
        df.index = df.index.astype(float)
        df.index.name = "DEPTH"
        
        # Create fake las_data object for standardization
        class FakeLASData:
            pass
        
        fake_las = FakeLASData()
        
        # Standardize ALL curves (GR, RHOB, NPHI, etc.)
        _standardize_all_curves(fake_las, df, std_names)
        
        if verbose:
            print(f"✓ {ascii_file_path.name}")
        return df
        
    except Exception as e:
        if verbose:
            print(f"✗ Error in {ascii_file_path.name}: {type(e).__name__}: {e}")
    return None


def _get_well_name(ascii_file_path):
    """Extract well name from ASCII file (use filename)"""
    return ascii_file_path.stem
