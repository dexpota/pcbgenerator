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
    
    - If you are going to use a virtual environment be sure to inherit this package from the global installation, if you
      use `pipenv` simply add `--site-packages` option when installing the virtual environment:
        ```bash
        pipenv --site-packages install
        ``` 
    
## Usage

This repository contains two modules **dxfgenerator**, used to generate the *dxf* files for each face of the given 
solid, and **pcbgenerator** for the generation of the *pcb* designs from the *dxf* files. The two modules are designed 
to be used in a pipeline where the output of the first one can be used as input of the second module.

### Generate DXF files

Starting from an *obj* representation of the solid you first use **dxfgenerator** to create a *dxf* file for each face 
of the solid.

```bash
python -m dxfgenerator
```

## Limitations

**dxfgenerator** currently is able to generate *dxf* files for just one type of octahedron and all parameters are statically
included inside the script.