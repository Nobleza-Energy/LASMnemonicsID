import signal_petrophysics.utils.mnemonics as mnm
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




# Function that create the mnemonic dictionary
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
    Function that create the mnemonic dictionary with the mnemonics per log type in the utils module
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



def field_las_read(dir, verbose=True):
    well_logs_by_folder = {}
    directories = [dir]

    for current_dir in directories[:]:
        items = os.listdir(current_dir)
        for item in items:
            item_path = join(current_dir, item)
            if os.path.isdir(item_path):
                directories.append(item_path)
                subfolder_name = os.path.basename(item_path)
                well_logs_by_folder[subfolder_name] = {}
                
                las_files = [f for f in os.listdir(item_path) if f.lower().endswith(".las")]
                if verbose:
                    print(f"\nFolder: {subfolder_name}")
                    print(f"LAS files found: {las_files}")
                
                for file_name in las_files:
                    file_path = os.path.join(item_path, file_name)
                    try:
                        las_data = lasio.read(file_path)
                        df = las_data.df()
                        df.index = df.index.astype(float)
                        df.dropna(inplace=True)

                        # Convert to string and then strip to handle both string and numeric values
                        well_name = str(las_data.well.WELL.value).strip()
                        print(f"✓ Processing well: {well_name}")

                        for curve in las_data.curves:
                            mnemonic_lower = curve.mnemonic.lower()
                            if mnemonic_lower in gamma_names:
                                df.rename(
                                    columns={curve.mnemonic: "GR"}, inplace=True
                                )
                                break
                        well_logs_by_folder[subfolder_name][well_name] = df
                    except lasio.exceptions.LASHeaderError as e:
                        print(f"✗ LASHeaderError in {file_name}: {e}")
                    except KeyError as e:
                        print(f"✗ KeyError in {file_name}: Missing well info - {e}")
                    except Exception as e:
                        print(f"✗ Error in {file_name}: {type(e).__name__}: {e}")
    return well_logs_by_folder

## Function that reads in and parses the las files in a directory with them already classified and renames GR curves to "GR"
#def field_las_read(dir):
#    well_logs_by_folder = {}
#    directories = [dir]
#
#    for current_dir in directories[:]:  # Iterate over a copy of the list
#        items = os.listdir(current_dir)
#        for item in items:
#            item_path = join(current_dir, item)
#            if os.path.isdir(item_path):
#                directories.append(item_path)  # Add new directories to the list
#                subfolder_name = os.path.basename(item_path)
#                well_logs_by_folder[subfolder_name] = {}
#                for file_name in os.listdir(item_path):
#                    if file_name.endswith(".las"):
#                        file_path = os.path.join(item_path, file_name)
#                        try:
#                            las_data = lasio.read(file_path)
#                            df = las_data.df()
#                            df.index = df.index.astype(float)
#                            df.dropna(inplace=True)
#
#                            # Extract well name from the header
#                            well_name = las_data.well.WELL.value.strip()
#                            print(f"Processing well: {well_name}")
#
#                            for curve in las_data.curves:
#                                mnemonic_lower = curve.mnemonic.lower()
#                                if mnemonic_lower in gamma_names:
#                                    df.rename(
#                                        columns={curve.mnemonic: "GR"}, inplace=True
#                                    )
#                                    break
#                            well_logs_by_folder[subfolder_name][well_name] = df
#                        except lasio.exceptions.LASHeaderError:
#                            print(f"Warning: {file_name} needs revision")
#                        except Exception as e:
#                            print(f"Error processing {file_name}: {str(e)}")
#    return well_logs_by_folder
#
# Function that reads in and parses the las files of offset wells without dropping nan values rows
def field_las_read_offset(dir):
    well_logs_by_folder = {}
    directories = [dir]

    for current_dir in directories[:]:  # Iterate over a copy of the list
        items = os.listdir(current_dir)
        for item in items:
            item_path = join(current_dir, item)
            if os.path.isdir(item_path):
                directories.append(item_path)  # Add new directories to the list
                subfolder_name = os.path.basename(item_path)
                well_logs_by_folder[subfolder_name] = {}
                for file_name in os.listdir(item_path):
                    if file_name.endswith(".las"):
                        file_path = os.path.join(item_path, file_name)
                        try:
                            las_data = lasio.read(file_path)
                            df = las_data.df()
                            df.index = df.index.astype(float)
                            #df.dropna(inplace=True)

                            # Extract well name from the header
                            well_name = las_data.well.WELL.value.strip()
                            print(f"Processing well: {well_name}")

                            for curve in las_data.curves:
                                mnemonic_lower = curve.mnemonic.lower()
                                if mnemonic_lower in gamma_names:
                                    df.rename(
                                        columns={curve.mnemonic: "GR"}, inplace=True
                                    )
                                    break
                            well_logs_by_folder[subfolder_name][well_name] = df
                        except lasio.exceptions.LASHeaderError:
                            print(f"Warning: {file_name} needs revision")
                        except Exception as e:
                            print(f"Error processing {file_name}: {str(e)}")
    return well_logs_by_folder



def clean_gr_data(gr_dict):
    """
    Replaces -999.25 with NaN and drops rows with NaNs in the 'GR' column.
    
    Args:
        gr_dict (dict): A dictionary where values are dictionaries containing
                        'data' (a pandas DataFrame) and 'units'.

    Returns:
        dict: A new dictionary with the cleaned data.
    """
    gr_dict_clean = {}
    
    for filename, content in gr_dict.items():
        # Make a deep copy to avoid modifying the original dictionary
        cleaned_content = content.copy()
        df = cleaned_content['data'].copy()
        
        # Step 1: Replace the placeholder value with NaN
        df.replace(-999.25, np.nan, inplace=True)
        
        # Step 2: Identify the GR column(s) and drop rows with NaNs
        gr_columns = [col for col in df.columns if 'GR' in col.upper()]
        if gr_columns:
            df.dropna(subset=gr_columns, inplace=True)
            
        # Update the DataFrame in the new content dictionary
        cleaned_content['data'] = df
        gr_dict_clean[filename] = cleaned_content
        
    return gr_dict_clean

## --- How to use the function ---
## Assume gr_dict_one_per_well is the dictionary from the previous steps
#gr_dict_clean = clean_gr_data(gr_dict_one_per_well)
#
#print(f"Original dictionary has {len(gr_dict_one_per_well)} files.")
#print(f"Cleaned dictionary has {len(gr_dict_clean)} files.")
#
## To see the result for a specific file, for example:
#first_file_name = next(iter(gr_dict_clean))
#original_rows = len(gr_dict_one_per_well[first_file_name]['data'])
#cleaned_rows = len(gr_dict_clean[first_file_name]['data'])
#
#print(f"\nExample file: {first_file_name}")
#print(f"Original rows: {original_rows}")
#print(f"Cleaned rows: {cleaned_rows}")
