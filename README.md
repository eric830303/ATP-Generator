# ATP Generator
The Python-based script is used to convert an Excel to input vectors (ATP files), for testing chips.
The protocol supported by the script:
- I2C
- SPI
- SMI (MDC/MDIO)

## Installation

It requires [Python](https://www.python.org/downloads/) v3.7+ and [Pandas](https://pandas.pydata.org/) to run.
No need to intall them individually. It is recommended to install [Anaconda](https://www.anaconda.com/distribution/), which has involved both of them.

## Run on Windows
Launch your Windows prompt and enter the directory where the script is located.
#### Help 
```zsh
$ python .\converter.py -h
```
#### I2C
Convert the Excel file based on I2C protocol
```sh
$ python .\converter.py -i2c -input pattern_example.xlsx
```
Convert the Excel file based on I2C protocol, with the specified output filename.
```sh
$ python .\converter.py -i2c -input pattern_example.xlsx -output output_i2c.atp
```
Convert the Excel file based on I2C protocol, with the specified output filename and the specified 5-bit control byte
```sh
$ python .\converter.py -i2c -input pattern_example.xlsx -output output_i2c.atp -ctrlbyte 1010111
```
#### SPI
Convert the Excel file based on SPI protocol
```sh
$ python .\converter.py -spi -input pattern_example.xlsx
```
Convert the Excel file based on SPI protocol, with the specified output filename.
```sh
$ python .\converter.py -spi -input pattern_example.xlsx -output output_spi.atp
```
#### SMI (MDC/MDIO)
Convert the Excel file based on SMI protocol
```sh
$ python .\converter.py -smi -input pattern_example.xlsx
```
Convert the Excel file based on SMI protocol, with the specified output filename.
```sh
$ python .\converter.py -smi -input pattern_example.xlsx -output output_smi.atp
```




