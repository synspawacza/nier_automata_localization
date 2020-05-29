# Nier: Automata Localization Tool

Toolset for creating unofficial localization of Nier: Automata

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Bash
* Python 3.6 (or newer)
* ImageMagick

### Setup

1. Create [OmegaT](https://omegat.org/) project
2. Copy files from this repo to the OmegaT project
3. Unpack CRI packages from the game to `data/` directory. ([CriPakGUI](https://github.com/wmltogether/CriPakTools/releases) can be used)
4. Run `./prepare.sh` to unpack files and generate `source/` directory (this should be done only once)
5. Fonts
    1. Add missing characters in `fonts/`. Name of the character should be codepoint number as a 4-digit hex, e.g. `017a.png` for
       letter 'ź' (Latin Small Letter Z with Acute).
    2. Edit `./build_fonts.sh` to add missing characters
    2. Run `./build_fonts.sh` to generate font files
6. Translation
    1. Translate files and generate `target/` directory in OmegaT
    2. Run `./build_localization.sh` to generate `output/`
7. Copy files from `output/` to `<game directory>/data/`

### Directories structure

* `omegat/` - files used by OmegaT
* `data/` - \*.dat and \*.dtt files extracted from CRI packages (\*.cpk)
* `fonts/` - font data - glyph images
* `unpacked/` - untranslated raw files (\*.bin, \*.mcd, \*.smd, etc.) extracted from \*.dat and \*.dtt files. \*.dds textures are also extracted
* `source/` - source \*.properties and \*.txt files for translation
* `target/` - \*.properties and \*.txt files translated to target language
* `assembly/` - translated raw files (\*.bin, \*.mcd, \*.smd, etc.)
* `output/` - translated \*.dat and \*.dtt files

### Notes

OmegaT is not handling properly values in .properties files ending with backslash. Value `key=\\` is interpreted as escaping endline
rather than escaped backslash. For that reason dummy value `<removeme>` is added. It should be removed during translation.

Glyphs for some of the fonts have color data in transparent parts. Some image editors will lose this information when exporting to PNG.
Losing this data will cause these characters to render incorrectly. To get around this following ImageMagick commands can be used:
```
convert glyph.png -alpha extract glyph_alpha.png # extract alpha channel
convert glyph.png -alpha off glyph_color.png     # extract color channels
convert glyph_color.png glyph_alpha.png -alpha off -compose CopyOpacity -composite glyph.png # combine alpha and color
```

## Acknowledgments

Resources used during development:
* Russian translations by Rindera (https://steamcommunity.com/sharedfiles/filedetails/?id=1206296158) and The Miracle (https://steamcommunity.com/sharedfiles/filedetails/?id=889954753)
* General information on files formats: https://forum.xentax.com/viewtopic.php?t=16011
* DAT format: https://gist.github.com/Wunkolo/213aa61eb0c874172aec97ebb8ab89c2 and https://github.com/xxk-i/DATrepacker/blob/master/dat_utils.py
* MCD format: https://zenhax.com/viewtopic.php?t=1502&p=8181 and https://github.com/Kerilk/bayonetta_tools/tree/master/binary_templates
* WTA format: https://github.com/Kerilk/bayonetta_tools/blob/master/binary_templates/Nier%20Automata%20wta.bt
* mruby bytecode: https://github.com/mrubyc/mrubyc/ and https://github.com/mruby/mruby/
