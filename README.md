# GDK Decoder

> This tool is intended to fix a text file with corrupted Chinese characters.

## Table of Contents
* [General Info](#general-information)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [License](#license)

## General Information
When a simplified Chinese text file was saved with a non-GBK encoding, the characters are not readable.
This tool decodes the input file with GBK encoding to solve the problem.

## Setup
Run the PyInstaller to create and bundle the tool:

```commandline
pyinstaller.exe .\main.py -n gbk_decoder
```

## Usage
```commandline
gbk_decoder --infile <input_txt_file> --outfile <output_txt_file>
```

## Project Status
Project is _complete_.

## License
This project is open source and available under the BSD 2-Clause License.
