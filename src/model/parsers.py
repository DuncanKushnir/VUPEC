"""
file parsers
"""
import os
from model.common import ObjDict

COMMENT_DELIMITER = "#"
HINT_TO_PARSER = {}


def register_parser(hint, parser):
    global HINT_TO_PARSER
    if hint in HINT_TO_PARSER:
        print(f"{hint} already has a parser")
    HINT_TO_PARSER[hint] = parser


def read_file(filepath, parser=None):
    raw = []
    if parser is None:
        # Try from extension first
        parser = HINT_TO_PARSER.get(os.path.splitext(filepath)[-1], None)

    with open(filepath, "r") as f:
        for line in f.readlines():
            line = line.strip("\r\n\t")
            if line and not line.startswith(COMMENT_DELIMITER):
                if COMMENT_DELIMITER in line:
                    line = line.split(COMMENT_DELIMITER)[0]
                    line = line.strip("\t")

                # If specified, use that
                if "filetype" in line:
                    pass
                raw.append(line)

    if parser is not None:
        parser_obj = parser(raw, filepath)
        return parser_obj

    else:
        return raw


class LineParserBase:
    RESULT_CLASS = None

    def __init__(self, raw_lines=None, filepath=None):
        self.name = None
        self.filepath = "unknown" if filepath is None else filepath
        self.result = []

        if raw_lines is not None:
            self.parse(raw_lines)

    def parse(self, raw_lines):
        for idx, raw_line in enumerate(raw_lines):
            line = [item.lower() for item in raw_line.split()]
            command, args = line[0], line[1:]
            try:
                # need the item first.
                if command != "name" and not self.result:
                    raise SyntaxError("item must be the first command in a section")

                elif command.startswith("%"):
                    if not hasattr(self.result[-1], "_sub_objects"):
                        self.result[-1]._sub_objects = []
                    self.result[-1]._sub_objects.append((command[1:], args))

                elif command == "name":
                    self.new_result(args[0])

                elif (
                    self.RESULT_CLASS is not None
                    and hasattr(self.RESULT_CLASS, "META_FIELDS")
                    and command in self.RESULT_CLASS.META_FIELDS
                ):
                    self.key_to_metadata(line)
                else:
                    self.handle_line(line)
            except:
                print(
                    f"parse of {self.filepath} failed on line {idx+1} (following):\n"
                    f"'{raw_line}' \n..continuing.. "
                )
                raise

    def new_object_hook(self):
        pass

    def handle_line(self, line):
        raise NotImplementedError(f"handle_line must be implemented in {__class__}")

    def new_result(self, name):
        if self.RESULT_CLASS is None:
            raise NotImplementedError("must have a result class")
        self.result.append(self.RESULT_CLASS())
        self.result[-1].name = name
        self.new_object_hook()

    def key_to_metadata(self, line):
        key = line[0]
        data = line[1:]
        if len(data) == 1:
            data = data[0]
            if data.lower == "false":
                data = False
            elif data.lower == "true":
                data = True
        self.result[-1].metadata[key] = data


class DictParser(LineParserBase):
    RESULT_CLASS = ObjDict

    def new_object_hook(self):
        self.result[-1]["_include"] = ["default"]

    def handle_line(self, line):
        if line[0] == "include":
            self.result[-1]._include.append(line[1])
        else:
            if len(line) == 2:
                val = line[1]
                if val.lower() == "false":
                    val = False
                elif val.lower() == "true":
                    val = True
                else:
                    try:
                        val = float(val)
                    except:
                        pass
                self.result[-1][line[0]] = val
            else:
                self.result[-1][line[0]] = line[1:]


register_parser(".dat", DictParser)
