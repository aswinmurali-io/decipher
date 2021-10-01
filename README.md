# Decipher
An 💻open-source tool for 🔓 cracking cipher-encrypted files.

![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![numpy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
</br>
[![CodeQL](https://github.com/aswinmurali-io/decipher/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/aswinmurali-io/decipher/actions/workflows/codeql-analysis.yml)
![Generic badge](https://img.shields.io/badge/welcome-decipher-green.svg)
[![GitHub License](https://img.shields.io/github/license/aswinmurali-io/decipher.svg)](https://github.com/aswinmurali-io/decipher/blob/master/LICENSE)
[![Maintenance](https://img.shields.io/badge/maintained-yes-green.svg)](https://github.com/aswinmurali-io/decipher/graphs/commit-activity)
[![GitHub Branches](https://badgen.net/github/branches/aswinmurali-io/decipher)](https://github.com/aswinmurali-io/decipher/)
[![GitHub Contributors](https://img.shields.io/github/contributors/aswinmurali-io/decipher.svg)](https://github.com/aswinmurali-io/decipher/badges/graphs/contributors/)
</br>
Do you like the project? :)</br>
[![GitHub stars](https://img.shields.io/github/stars/aswinmurali-io/decipher.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/aswinmurali-io/decipher.svg/stargazers/)

## Cracking

To decrypt a string. Use the `--input` to command to specify the input string.

```bash
python -m decipher --input "Encrypted text here"
```

```bash
python -m decipher -i "Encrypted text here"
```

To decrypt a text file. Use the `--input-file` to command to specify the file path.

```bash
python -m decipher --input-file test.txt
```

<!-- cannot annotate lang parameter here -if highlighted-->
```
python -m decipher -if test.txt
```

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

### Using custom word list

By default `decipher` will use `nltk.corpus`. You can specify different word file by
passing the `--word-list` arg with a file name.

```bash
git clone https://github.com/dwyl/english-words
python -m decipher --generate-dataset --word-list english-words/words_alpha.txt
```

## Training

To train the model for `decipher`. Use the `--train` argument. This will scan for
dataset and start the training process.

```bash
python -m decipher --train
```

### Speed up training

To speed up the training process use the `--quick-train` argument. The will reduce
the training complexity to make the process faster. Useful for training large
dataset with limited computational power.

```bash
python -m decipher --train --quick-train
```

## Usage

```

An 💻 open-source tool for 🔓 cracking cipher-encrypted files.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         display verbose-level information
  -g, --generate-dataset
                        generates the dataset for training
  -qt, --quick-train    quickly train the model by reducing complexity
  -t, --train-model     train the model (uses model_v1)
  -w PATH, --word-list PATH
                        specify the word list file, default is nltk.corpus
  -if PATH, --input-file PATH
                        specify the file 📄 to crack 🔑
  -i TEXT, --input TEXT
                        specify the text 🅰 to crack 🔑

Enjoy deciphering! 😄
```
