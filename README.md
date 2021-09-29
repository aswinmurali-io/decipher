# Decipher

(Work in progress)

An 💻Open-Source tool for 🔓 cracking cipher-encrypted files.

![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![numpy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
</br>
[![CodeQL](https://github.com/aswinmurali-io/decipher/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/aswinmurali-io/decipher/actions/workflows/codeql-analysis.yml)

## Setup

If you don't have `conda` install Miniconda from [here](https://docs.conda.io/en/latest/miniconda.html)

```bash
git clone https://github.com/aswinmurali-io/decipher.git
conda env create -f environment.yaml
python -m decipher [args]
```

The tool is capable of generating the `default` dataset to get things started. But
for this to work we need to use `nltk` dataset. To do this type the below code in the python interpreter.

```python
import nltk
nltk.download()
```

## Usage

```
usage: decipher [options] path

An 💻 Open-Source tool for 🔓 cracking cipher-encrypted files.    

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Display verbose-level information
  -g, --generate-dataset
                        generates the default dataset for training

Enjoy the program! 😄
```
