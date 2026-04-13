# Scryfall-Card-Imager
Utility for reading a file containing MTG deck information and downloading the respective card images from Scryfall.
This utility's import utilizes the same format as Moxfield's export feature, allowing the user to easily pull from
their deck lists.
##### Example
```
...
1 Grand Coliseum (TMC) 68
1 Growth Spiral (DSC) 88
1 Guadosalam, Farplane Gateway (FIN) 281
1 Heroic Intervention (CMM) 295
1 Horizon of Progress (M3C) 78
1 Il Mheg Pixie (FIN) 57
1 Indatha Triome (IKO) 248
...
```

### Required packages
`Scrython` and `requests` are required to run this utility.  
They can be installed with
```
pip install scrython
pip install requests
```

### Usage
SFCardDL.py [-h] [-d DIR] [-l LOGFILE] filename
- -h: Displays help information
- DIR: Optional argument which allows the user to set a relative path to a directory that the images will be saved to
- LOGFILE: Optional argument for renaming the generated logfile

Credit to Nanda Scott for the Scrython module (https://github.com/NandaScott/Scrython)
