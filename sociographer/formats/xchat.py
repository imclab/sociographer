import re

def parse_lines(f, **ctx):
    # Parse lines in X-Chat format.
    PARSE_EXPR = re.compile(r".*? <(?P<nick>.*?)>\t(?P<message>.*)$".format(**ctx))

    for line in f:
        match = PARSE_EXPR.match(line.strip())
        if match is None:
            continue
        yield match.group("nick"), match.group("message")

