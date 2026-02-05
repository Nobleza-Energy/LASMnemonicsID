<h1 align="center">LASMnemonicsID©</h1>
<p align="center">
  <img src="https://github.com/Nobleza-Energy/LASMnemonicsID/blob/e44bfb606fef5cfc9c3df6e41c3d1bd0d7bb08ae/logo.png?raw=true" alt="LASMnemonicsID Logo" width="200"/>
</p>

<p align="center">
  <b>Well log mnemonic identification and standardization for LAS, DLIS, and ASCII formats</b>
</p>

<p align="center">
  <a href="https://pypi.org/project/lasmnemonicsid/"><img src="https://img.shields.io/pypi/v/lasmnemonicsid.svg" alt="PyPI"></a>
  <a href="https://pypi.org/project/lasmnemonicsid/"><img src="https://img.shields.io/pypi/pyversions/lasmnemonicsid.svg" alt="Python Versions"></a>
  <a href="https://github.com/Nobleza-Energy/LASMnemonicsID/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Nobleza-Energy/LASMnemonicsID.svg" alt="License"></a>
</p>

---

## 🚀 Features

- ✅ **Multi-format support**: LAS, DLIS, ASCII/CSV/TXT/DAT
- ✅ **Automatic mnemonic standardization**: GR, RHOB, NPHI, DT, SP, CALI, RT, etc.
- ✅ **Batch processing**: Parse entire directories recursively
- ✅ **Customizable naming**: Override default standard names
- ✅ **Case-insensitive extensions**: Works with .las/.LAS, .dlis/.DLIS, .csv/.CSV, etc.
- ✅ **Pandas integration**: Returns clean DataFrames ready for analysis

---

## 📦 Installation

\`\`\`bash
pip install lasmnemonicsid
\`\`\`

This installs support for **all formats** (LAS, DLIS, ASCII/CSV/TXT).

---

## 🧪 Quick Start

### LAS Files
\`\`\`python
from LASMnemonicsID import parseLAS

# Parse single LAS file (case-insensitive: .las, .LAS)
df = parseLAS("well.las")
df = parseLAS("WELL.LAS")  # Also works!
print(df.head())

# Parse directory → dict of {filename: DataFrame}
data = parseLAS("/path/to/las/files/")
for filename, df in data.items():
    print(f"{filename}: {df.shape}")
\`\`\`

### DLIS Files
\`\`\`python
from LASMnemonicsID import parseDLIS

# Parse single DLIS file (case-insensitive: .dlis, .DLIS)
df = parseDLIS("well.dlis")
df = parseDLIS("WELL.DLIS")  # Also works!
print(df.columns)  # ['GR', 'RHOB', 'NPHI', 'DT', ...]

# Parse directory
data = parseDLIS("/path/to/dlis/files/")
\`\`\`

### ASCII/CSV/TXT Files
\`\`\`python
from LASMnemonicsID import parseASCII

# Parse CSV (case-insensitive: .csv, .CSV)
df = parseASCII("well_log.csv", depth_col="DEPTH")
df = parseASCII("WELL_LOG.CSV")  # Also works!

# Parse tab-separated TXT
df = parseASCII("well_log.txt", delimiter="\t")

# Supported extensions (case-insensitive):
# .csv, .CSV, .txt, .TXT, .asc, .ASC, .dat, .DAT, .ascii, .ASCII
data = parseASCII("/path/to/mixed/files/")
\`\`\`

---

## 🎯 Advanced Usage

### Custom Preferred Names
\`\`\`python
preferred = {
    "deepres": "RT",
    "deepres_preferred_original": "AT90",
    "gamma": "GR"
}

df = parseLAS("well.las", preferred_names=preferred)
\`\`\`

### Batch Processing
\`\`\`python
from pathlib import Path

dir_path = Path("/data/wells/")
data = parseLAS(dir_path, verbose=True, preferred_names=preferred)

for fname, df in data.items():
    print(f"{fname}: {df.shape}")
\`\`\`

### Mixed Formats
\`\`\`python
las_data = parseLAS("/data/wells/")
dlis_data = parseDLIS("/data/wells/")
ascii_data = parseASCII("/data/wells/")

all_data = {**las_data, **dlis_data, **ascii_data}
\`\`\`

---

## 📊 Supported Mnemonics

| Curve Type | Standard Name | Common Aliases |
|------------|---------------|----------------|
| Gamma Ray | GR | GAMMA, GRD, GRC |
| Deep Resistivity | RT | AT90, ILD, LLD |
| Shallow Resistivity | RXO | RFOC, LLS |
| Density | RHOB | DENS, DEN |
| Neutron Porosity | NPHI | NPOR, NEU |
| Sonic | DT | DTC, AC |
| Spontaneous Potential | SP | SPT |
| Caliper | CALI | CAL |
| Photoelectric | PEF | PE |

---

## 📖 API Reference

### parseLAS(input_path, verbose=True, preferred_names=None)
Parse LAS file(s) and standardize mnemonics.

### parseDLIS(input_path, verbose=True, preferred_names=None)
Parse DLIS file(s) and standardize mnemonics.

### parseASCII(input_path, verbose=True, preferred_names=None, depth_col="DEPTH", delimiter=",")
Parse ASCII/CSV/TXT file(s) and standardize mnemonics.

---

## 📄 How to Cite

**APA**

> Nobleza Energy. (2026). LASMnemonicsID [Software]. GitHub. https://github.com/Nobleza-Energy/LASMnemonicsID

**BibTeX**

\`\`\`bibtex
@software{LASMnemonicsID,
  author = {Nobleza Energy},
  title = {LASMnemonicsID},
  year = {2026},
  url = {https://github.com/Nobleza-Energy/LASMnemonicsID}
}
\`\`\`

---

## 📜 License

MIT License - see LICENSE file.

---

<p align="center">
  Made with ❤️ by <a href="https://nobleza-energy.com">Nobleza Energy</a>
</p>
