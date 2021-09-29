# Decipher

(Work in progress)

An 💻Open-Source tool for 🔓 cracking cipher-encrypted files.

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
