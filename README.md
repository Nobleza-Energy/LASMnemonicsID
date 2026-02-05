# LASMnemonicsID

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

## Features

- **Multi-format support**: LAS, DLIS, ASCII/CSV/TXT/DAT
- **Automatic mnemonic standardization**: GR, RHOB, NPHI, DT, SP, CALI, RT, etc.
- **Batch processing**: Parse entire directories recursively
- **Customizable naming**: Override default standard names
- **Case-insensitive extensions**: Works with .las/.LAS, .dlis/.DLIS, .csv/.CSV, etc.
- **Pandas integration**: Returns clean DataFrames ready for analysis

---

## Installation

```bash
pip install lasmnemonicsid
```

This installs support for **all formats** (LAS, DLIS, ASCII/CSV/TXT).

---

## Quick Start

### LAS Files

```python
from LASMnemonicsID import parseLAS

# Parse single LAS file
df = parseLAS("well.las")
print(df.head())

# Parse directory
data = parseLAS("/path/to/las/files/")
for filename, df in data.items():
    print(f"{filename}: {df.shape}")
```

### DLIS Files

```python
from LASMnemonicsID import parseDLIS

# Parse single DLIS file
df = parseDLIS("well.dlis")
print(df.columns)

# Parse directory
data = parseDLIS("/path/to/dlis/files/")
```

### ASCII/CSV/TXT Files

```python
from LASMnemonicsID import parseASCII

# Parse CSV
df = parseASCII("well_log.csv", depth_col="DEPTH")

# Parse tab-separated TXT
df = parseASCII("well_log.txt", delimiter="\t")

# Parse directory
data = parseASCII("/path/to/csv/files/")
```

---

## Advanced Usage

### Custom Preferred Names

```python
preferred = {
    "deepres": "RT",
    "deepres_preferred_original": "AT90",
    "gamma": "GR"
}

df = parseLAS("well.las", preferred_names=preferred)
```

### Batch Processing

```python
from pathlib import Path

dir_path = Path("/data/wells/")
data = parseLAS(dir_path, verbose=True, preferred_names=preferred)

for fname, df in data.items():
    print(f"{fname}: {df.shape}")
    print(df.head(3))
```

### Mixed Format Directories

```python
las_data = parseLAS("/data/wells/")
dlis_data = parseDLIS("/data/wells/")
ascii_data = parseASCII("/data/wells/")

all_data = {**las_data, **dlis_data, **ascii_data}
```

---

## Supported Mnemonics

The package automatically standardizes these curve types:

| Curve Type | Standard Name | Example Aliases |
|------------|---------------|-------------|
| Gamma Ray | `GR` | gr, cggr, cgr, gam, gamma, gammaray, grc, grd, hgr, sgr, lgr, pgr |
| Spontaneous Potential | `SP` | sp, idsp, spr, spl, spdl, spdhp, spc, sp0, sp1, cgsp, dlsp |
| Caliper | `CALI` | caliper, calip, cal, dcal, acal, cala, cald, cale, calh, hcal, xcal, ycal |
| Deep Resistivity | `RT` | rt, rtao, rt90, ild, idph, rild, rd, ae90, at90, atrt, lld, lldc, res, resd |
| Shallow Resistivity | `RXO` | rxo, rxoz, msfl, mcfl, sflcc, mgl, m1rx, r40o, aht10 |
| Density | `RHOB` | rhob, rhoz, den, denb, denc, hrho, hrhob, zden, hden, denf, denn |
| Density Correction | `DRHO` | dcor, dcorr, dc, decr, drh, zcor, zcorr, hhdr, denscorr |
| Neutron Porosity | `NPHI` | cn, phin, cnc, cns, hnphi, nphi, npor, cncc, nprl, neut, neutpor |
| Sonic (Compressional) | `DT` | dt, dtc, dtco, dtcomp, deltat, slow, slowness, tt, ac, acco, delt, dtcomp |
| Sonic (Shear) | `DTS` | dts, dtsh, dtsm, dtsc, dtsd, dtsqi, dtshear, deltas, tts, stt, dtshear |
| Photoelectric Factor | `PEF` | pe, pef, pefz, pdpe, pedf, pedn, hpedn, pe2, pef8, lpe |


---

## Testing

```bash
pytest tests/ -v
pytest tests/test_las.py -v
pytest tests/test_dlis.py -v
pytest tests/test_ascii.py -v
```

---

## API Reference

### parseLAS(input_path, verbose=True, preferred_names=None)

Parse LAS file(s) and standardize mnemonics.

**Parameters:**
- input_path (str/Path): LAS file or directory
- verbose (bool): Print parsing info
- preferred_names (dict): Custom name mappings

**Returns:** DataFrame (single file) or dict (multiple files)

### parseDLIS(input_path, verbose=True, preferred_names=None)

Parse DLIS file(s) and standardize mnemonics.

**Parameters:**
- input_path (str/Path): DLIS file or directory
- verbose (bool): Print parsing info
- preferred_names (dict): Custom name mappings

**Returns:** DataFrame (single file) or dict (multiple files)

### parseASCII(input_path, verbose=True, preferred_names=None, depth_col="DEPTH", delimiter=",")

Parse ASCII/CSV/TXT file(s) and standardize mnemonics.

**Parameters:**
- input_path (str/Path): ASCII file or directory
- verbose (bool): Print parsing info
- preferred_names (dict): Custom name mappings
- depth_col (str): Name of depth column
- delimiter (str): Field separator

**Returns:** DataFrame (single file) or dict (multiple files)

---

## How to Cite

**APA**

> Nobleza Energy. (2026). LASMnemonicsID: Well log mnemonic identification for LAS, DLIS, and ASCII formats [Software]. GitHub. https://github.com/Nobleza-Energy/LASMnemonicsID

**BibTeX**

```bibtex
@software{LASMnemonicsID,
  author = {Nobleza Energy},
  title = {LASMnemonicsID: Well log mnemonic identification for LAS, DLIS, and ASCII formats},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/Nobleza-Energy/LASMnemonicsID}
}
```

---

## License

MIT License - see [LICENSE](LICENSE) file.

---

## Contributing

Contributions welcome! Submit a Pull Request.

---

## Support

- **Issues:** [GitHub Issues](https://github.com/Nobleza-Energy/LASMnemonicsID/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Nobleza-Energy/LASMnemonicsID/discussions)

---

<p align="center">
  Made with ❤️ by <a href="https://nobleza-energy.com">Nobleza Energy</a>
</p>
