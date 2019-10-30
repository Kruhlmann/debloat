def gen_arrow_markers(source, pos_start, pos_end):
    result = ''

    # Calculate indices
    index_start = max(source.rfind('\n', 0, pos_start.index), 0)
    index_end = source.find('\n', index_start + 1)
    if index_end < 0: index_end = len(source)

    # Generate each line
    line_count = pos_end.line - pos_start.line + 1
    for i in range(line_count):
        # Calculate line columns
        line = source[index_start:index_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + "\n"
        result += " " * col_start + "^" * (col_end - col_start)

        # Re-calculate indices
        index_start = index_end
        index_end = source.find("\n", index_start + 1)
        if index_end < 0:
            index_end = len(source)

    return result.replace("\t", "")

class Error:
    def __init__(self, name, pos_start, pos_end, details):
        self.name = name
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.details = details

    def as_string(self):
        arrow_markers = gen_arrow_markers(self.pos_start.source, self.pos_start, self.pos_end)

        out = f"{self.name}: {self.details}\n"
        out += f"File {self.pos_start.fname} {self.pos_start.line + 1}:{self.pos_start.col + 1}"
        out += f"\n\n{arrow_markers}"
        return out

class IllegalTokenError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__("IllegalCharacterError", pos_start, pos_end, details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=""):
        super().__init__("InvalidSyntaxError", pos_start, pos_end, details)

class ExpectedSymbolError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__("ExpectedSymbolError", pos_start, pos_end, details)

class RuntimeError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__("RuntimeError", pos_start, pos_end, details)
        self.context = context

    def as_string(self):
        arrow_markers = gen_arrow_markers(self.pos_start.source, self.pos_start, self.pos_end)

        out = self.generate_traceback()
        out += f"{self.name}: {self.details}\n"
        out += f"\n\n{arrow_markers}"
        return out

    def generate_traceback(self):
        out = ""
        pos = self.pos_start
        ctx = self.context

        while ctx:
            out = f"\tFile {pos.fname} line {pos.line + 1} in {ctx.display_name}\n{out}"
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        return f"Stacktrace (oldest to newest):\n{out}"
