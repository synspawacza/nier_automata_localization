#!/usr/bin/python3

from io import TextIOWrapper

# java .properties file subset:
# no comments
# key has only ASCII characters
# : and = are not allowed in key, even escaped
# = is always key-value separator
# no multiline (no escaping endline terminator)
# all non-ASCII characters are escaped (keep_non_ascii=True will use UTF-8 rather than ASCII encoding)
# there are no characters outside Unicode BMP (no surogate pairs/32-bit characters)


def parse_properties(reader):
    result = dict()
    reader.seek(0)
    text_reader = TextIOWrapper(reader)
    for line in text_reader.readlines():
        key, sep, value = (
            line.rstrip("\r\n").encode("utf-8").decode("unicode_escape").partition("=")
        )
        result[key] = value

    return result


# escape manually, as python will use \xhh rather than \u00hh
def escape_nonascii(text, keep_non_ascii=False):
    result = ""
    for c in text:
        if ord(c) >= 0x10000:
            raise Exception("Unsupported character: U+{:x}".format(ord(c)))
        if ord(c) >= 0x7F and not keep_non_ascii:
            result += "\\u{:04x}".format(ord(c))
        elif c == "\t":
            result += "\\t"
        elif c == "\n":
            result += "\\n"
        elif c == "\r":
            result += "\\r"
        elif c == "\\":
            result += "\\\\"
        elif ord(c) <= 0x1F:
            result += "\\u{:04x}".format(ord(c))
        else:
            result += c
    if result[-1] == "\\":
        result += "<removeme>"  # Workaround for Omega-T
    return result


def serialize_properties(kv, keep_non_ascii=False):
    result = bytearray()
    for key, value in kv.items():
        result += (escape_nonascii(key + "=" + value, keep_non_ascii) + "\n").encode(
            "utf-8"
        )
    return result
