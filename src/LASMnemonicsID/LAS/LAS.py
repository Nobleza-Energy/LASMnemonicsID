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
import pathlib
import pandas as pd
import lasio
from os.path import join
from sys import stdout
from pathlib import Path

# Function that creates the mnemonic dictionary
def create_mnemonic_dict(
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
):
    """
    Function that creates the mnemonic dictionary with the mnemonics per log type.
    """
    mnemonic_dict = {
        "gamma": gamma_names,
        "sp": sp_names,
        "caliper": caliper_names,
        "deepres": deepres_names,
        "rxo": rxo_names,
        "density": density_names,
        "density_correction": density_correction_names,
        "neutron": neutron_names,
        "dtc": dtc_names,
        "dts": dts_names,
        "pe": pe_names,
    }
    return mnemonic_dict

def parseLAS(input_path, verbose=True, preferred_names=None):
    """
    Parse LAS file or all in directory → DataFrame or {filename: df}.
    
    Args:
        input_path (str/Path): LAS file or directory
        verbose (bool): Print info
        preferred_names (dict, optional): Mapping of curve types to preferred column names and preferred original columns.
            Example: {"deepres": "RT", "deepres_preferred_original": "AT90", "gamma": "GR"}
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
    
    # Case 1: Single File
    if input_path.is_file() and input_path.suffix.lower() == '.las':
        df = _read_single_las(input_path, verbose, std_names)
        return df if df is not None else None
    
    # Case 2: Directory (Recursive)
    las_files = list(input_path.rglob("*.las"))
    if not las_files:
        if verbose:
            print(f"No LAS files found in {input_path}")
        return {}
    
    las_dict = {}
    for las_file in las_files:
        df = _read_single_las(las_file, verbose, std_names)
        if df is not None:
            filename = las_file.name
            las_dict[filename] = df
    
    # Return single DF if only 1 file found, else dict
    if len(las_dict) == 1:
        return next(iter(las_dict.values()))
    
    return las_dict

def _read_single_las(las_file_path, verbose, std_names):
    """Read single LAS file to DataFrame and standardize ALL curves."""
    try:
        las_data = lasio.read(las_file_path)
        df = las_data.df()
        
        if df is None or df.empty:
            if verbose:
                print(f"✗ Empty DataFrame: {las_file_path.name}")
            return None
            
        # Ensure index is depth (float)
        df.index = df.index.astype(float)
        
        # Standardize ALL curves (GR, RHOB, NPHI, etc.)
        _standardize_all_curves(las_data, df, std_names)
        
        if verbose:
            print(f"✓ {las_file_path.name}")
        return df
        
    except lasio.exceptions.LASHeaderError as e:
        if verbose:
            print(f"✗ LASHeaderError in {las_file_path.name}: {e}")
    except Exception as e:
        if verbose:
            print(f"✗ Error in {las_file_path.name}: {type(e).__name__}: {e}")
    return None

def _get_well_name(las_file_path):
    """Extract well name from LAS file"""
    try:
        las_data = lasio.read(las_file_path)
        return str(las_data.well.WELL.value).strip()
    except:
        return las_file_path.stem

def _standardize_all_curves(las_data, df, std_names):
    """
    Rename ALL curves in the DataFrame to standard abbreviations 
    based on the mnemonic dictionary.
    """
    # 1. Get the dictionary of aliases
    mnem_dict = create_mnemonic_dict(
        gamma_names, sp_names, caliper_names, deepres_names, rxo_names,
        density_names, density_correction_names, neutron_names, 
        dtc_names, dts_names, pe_names
    )
    
    # 2. Track which columns we've already renamed to avoid duplicates
    renamed = set()

    # 3. For each curve type, find all aliases in the file
    for curve_type, aliases in mnem_dict.items():
        # Find all matching columns in df
        matching = [col for col in df.columns if col.lower() in [a.lower() for a in aliases]]
        
        if not matching:
            continue
        
        # Use standard name if provided, otherwise use curve_type.upper()
        target_name = std_names.get(curve_type, curve_type.upper())
        
        # If a preferred original column is specified, use it
        preferred_original = std_names.get(f"{curve_type}_preferred_original")
        
        if preferred_original and preferred_original in matching:
            # Rename preferred original to target_name
            df.rename(columns={preferred_original: target_name}, inplace=True)
            renamed.add(target_name)
        else:
            # Otherwise, pick the first matching alias
            df.rename(columns={matching[0]: target_name}, inplace=True)
            renamed.add(target_name)
        
        # Remove all other matching columns
        for col in matching:
            if col != target_name and col in df.columns:
                df.drop(columns=[col], inplace=True)

