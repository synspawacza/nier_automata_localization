#!/usr/bin/python3

import argparse
import os

import format.smd as smd
import format.tmd as tmd
import format.bin as bin
import format.mcd as mcd
import format.pak as pak
import format.properties as properties


def extract_strings_to_file(
    input_filename, output_filename, lang="en", keep_non_ascii=False
):
    if lang not in {"jp", "en", "fr", "it", "de", "es"}:
        raise Exception("Language " + lang + " is not supported")

    file_ext = os.path.splitext(input_filename)[1]

    parsed = None
    with open(input_filename, "rb") as in_file:
        if file_ext == ".bin":
            parsed = bin.File.parse(in_file)
        elif file_ext == ".smd":
            parsed = smd.File.parse(in_file)
        elif file_ext == ".tmd":
            parsed = tmd.File.parse(in_file)
        elif file_ext == ".mcd":
            parsed = mcd.File.parse(in_file)
        elif file_ext == ".pak":
            parsed = pak.File.parse(in_file)
        else:
            raise Exception(
                "Unable to extract " + input_filename + ": unknown file extenstion"
            )

    with open(output_filename, "wb") as out_file:
        out_file.write(
            properties.serialize_properties(parsed.get_strings(lang), keep_non_ascii)
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="source file name")
    parser.add_argument("output", help="target file name (*.properties)")
    parser.add_argument(
        "--lang",
        help="source laguage (default: en, affects only .bin and .pak files)",
        default="en",
    )
    parser.add_argument(
        "--keep-non-ascii",
        help="keep non-ascii charater as UTF-8 instead of escaping them (will produce non-standard .properties file)",
        action="store_true",
    )

    args = parser.parse_args()
    extract_strings_to_file(args.input, args.output, args.lang, args.keep_non_ascii)
