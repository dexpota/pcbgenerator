[license]: https://opensource.org/licenses/MIT
[license-badge]: https://img.shields.io/github/license/dexpota/pcbgenerator.svg?style=for-the-badge

# pcbgenerator

> An utility to generate a PCB starting from DXF files.

[![License: MIT][license-badge]][license]

## Requirements

Its main dependency is the module *pcbnew* provided by *KiCad*, this means that you must have *Python 2.7* and *KiCad* 
installed on the system. You can follow these instructions:

- On *Ubuntu* simply run these commands and after the installation the module *pcbnew* will be available to the 
*Python 2.7* interpreter:
    
    ```bash 
    sudo apt install python2.7 kicad
    python2.7 -m pcbnew && echo "pcbnew installed!"
    ```
    
    - If you are going to use a virtual environment be sure to inherit this package from the global installation;