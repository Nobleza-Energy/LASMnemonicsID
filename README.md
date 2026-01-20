
![LASMnemonicsID Logo](logo.png)

# LASMnemonicsID

LASMnemonicsID is a Python package that identifies and processes well log mnemonics from LAS and DLIS/LIS files. It leverages Python dictionaries for mnemonic mapping, lasio for LAS files, and dlisio for DLIS/LIS files to load data directly into pandas DataFrames for analysis.[web:6][web:11][memory:1]

## Features

- Reads LAS files (versions 1.2 and 2.0) using lasio and converts to DataFrames.[web:6][web:7]
- Handles DLIS and LIS files with dlisio, extracting curves as structured numpy arrays or DataFrames.[web:11]
- Uses predefined dictionaries to identify and standardize mnemonics for reservoir engineering workflows.
- Supports petrophysical analysis, well log interpretation, and subsurface data processing.

## Installation

1. Ensure Python 3.8+ is installed.
2. Install dependencies via pip:

