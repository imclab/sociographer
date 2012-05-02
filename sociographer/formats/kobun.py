import re

def parse_lines(f, **ctx):
    # Parse lines in Kobun format.
    PARSE_EXPR = re.compile(r"^.*? \[KobunClient,client\] {channel} <(?P<nick>.*?)!.*?@.*?> (?P<message>.*)$".format(**ctx))

    for line in f:
        match = PARSE_EXPR.match(line.strip())
        if match is None:
            continue
        yield match.group("nick"), match.group("message")

