
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
import dlisio
from pathlib import Path

# Import helper functions from LAS module
from ..LAS.LAS import create_mnemonic_dict, _standardize_all_curves


def parseDLIS(input_path, verbose=True, preferred_names=None):
    """
    Parse DLIS file or all in directory → DataFrame or {filename: df}.
    
    Args:
        input_path (str/Path): DLIS file or directory
        verbose (bool): Print info
        preferred_names (dict, optional): Mapping of curve types to preferred column names.
            Example: {"deepres": "RT", "gamma": "GR"}
            If not provided, defaults to standard petrophysical names.
        
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
    
    # Case 1: Single File (case-insensitive)
    if input_path.is_file() and input_path.suffix.lower() == '.dlis':
        df = _read_single_dlis(input_path, verbose, std_names)
        return df if df is not None else None
    
    # Case 2: Directory (Recursive) - CASE-INSENSITIVE
    dlis_files = [f for f in input_path.rglob("*") if f.suffix.lower() == '.dlis']
    if not dlis_files:
        if verbose:
            print(f"No DLIS files found in {input_path}")
        return {}
    
    dlis_dict = {}
    for dlis_file in dlis_files:
        df = _read_single_dlis(dlis_file, verbose, std_names)
        if df is not None:
            filename = dlis_file.name
            dlis_dict[filename] = df
    
    # Return single DF if only 1 file found, else dict
    if len(dlis_dict) == 1:
        return next(iter(dlis_dict.values()))
    
    return dlis_dict


def _read_single_dlis(dlis_file_path, verbose, std_names):
    """Read single DLIS file to DataFrame and standardize ALL curves."""
    try:
        with dlisio.dlis.load(str(dlis_file_path)) as (f, *rest):
            if not f.frames:
                if verbose:
                    print(f"✗ No frames: {dlis_file_path.name}")
                return None
            
            # Use first frame (typically contains main log data)
            frame = f.frames[0]
            curves_data = frame.curves()
            
            # Get channel names
            channels = [ch.name for ch in frame.channels]
            
            # Create DataFrame
            df = pd.DataFrame(curves_data, columns=channels)
            
            if df.empty:
                if verbose:
                    print(f"✗ Empty DataFrame: {dlis_file_path.name}")
                return None
            
            # Set depth index (typically first column or frame.index)
            if frame.index:
                index_name = frame.index
                if index_name in df.columns:
                    df.set_index(index_name, inplace=True)
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
                print(f"✓ {dlis_file_path.name}")
            return df
            
    except Exception as e:
        if verbose:
            print(f"✗ Error in {dlis_file_path.name}: {type(e).__name__}: {e}")
    return None


def _get_well_name(dlis_file_path):
    """Extract well name from DLIS file"""
    try:
        with dlisio.dlis.load(str(dlis_file_path)) as (f, *rest):
            if f.origins:
                return str(f.origins[0].well_name).strip()
    except:
        pass
    return dlis_file_path.stem
