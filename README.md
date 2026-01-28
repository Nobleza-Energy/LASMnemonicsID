<p align="center">
  <img src="https://raw.githubusercontent.com/Nobleza-Energy/LASMnemonicsID/main/logo.png" alt="LASMnemonicsID Logo" width="200"/>
</p>

<h1 align="center">LASMnemonicsID©</h1>

<p align="center">
  <b>Well log mnemonic identification using lasio, dlisio, pandas and custom oil and gas mnemonics for triple combo</b>
</p>

<p align="center">
  <a href="https://pypi.org/project/lasmnemonicsid/"><img src="https://img.shields.io/pypi/v/lasmnemonicsid.svg" alt="PyPI"></a>
  <a href="https://pypi.org/project/lasmnemonicsid/"><img src="https://img.shields.io/pypi/pyversions/lasmnemonicsid.svg" alt="Python Versions"></a>
  <a href="https://github.com/Nobleza-Energy/LASMnemonicsID/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Nobleza-Energy/LASMnemonicsID.svg" alt="License"></a>
</p>

---

## 📦 Installation

```bash
pip install lasmnemonicsid
```

## 🧪 Test with your Data: Multiple files will load into a dictionary 

```python

# define path of directory containing .las files, if multiple
dir = "/home/path/dir/"

# Parse all LAS files in a directory to be stored as dataframes within the data dictionary
data = parseLAS(dir, preferred_names=preferred)

# List all files names, as they are stored as the dictionary keys
print("Files:", list(data.keys()))

# Access a specific file's DataFrame head
for fname, df in data.items():
    print(f"\n{fname}:")
    print(df.columns.tolist())
    print(df.head(3))

# Dataframes
# define the path where your .las file is
path = 'path to file/file.las'

# you can optionally use preferred names for the standard mnemonic automatic match, in this case AT90, if present, will be renamed as the deep resistivity standard curve name "RT" (column name of the dataframe)
preferred = {
    "deepres_preferred_original": "AT90",
    "gamma": "GR"
}

# Parse a single LAS file
df = parseLAS(path, preferred_names=preferred)
# View the standardized/renamed columns
print(df_new.columns)
```

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Nobleza-Energy/LASMnemonicsID&type=Date)](https://star-history.com/#Nobleza-Energy/LASMnemonicsID&Date)


## 📄 How to Cite

If you use `LASMnemonicsID` in your research or project, please cite it as follows:

**APA**

> Nobleza Energy. (2026). LASMnemonicsID: Well log mnemonic identification using lasio and dlisio [Software]. GitHub. https://github.com/Nobleza-Energy/LASMnemonicsID

**BibTeX**

```bibtex
@software{LASMnemonicsID,
  author = {Nobleza Energy},
  title = {LASMnemonicsID: Well log mnemonic identification using lasio and dlisio},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  url = {https://github.com/Nobleza-Energy/LASMnemonicsID}
}
