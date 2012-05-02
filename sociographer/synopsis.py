# Generates the synopsis data structures, for creating the intermediate data
# structure used with the relation graph generator.

import json
import re
import sys

HIGHLIGHT_EXPR = re.compile(r"^(?P<nick>.*?)[:,]? .*$")

def generate_nicks(f, fmt, **ctx):
    # Generate the set of nicknames from the file.
    nicks = set([])

    n_lines = 0
    for nick, _ in fmt.parse_lines(f, **ctx):
        nicks.add(nick)
        n_lines += 1

    sys.stderr.write("Collated {} nicks from {} lines.\n".format(len(nicks), n_lines))
    return nicks

def generate_relations(f, fmt, nicks, **ctx):
    # Generate the dictionary of relations from the file, using the given nicks.
    relations = {}

    n_lines = 0
    for nick, message in fmt.parse_lines(f, **ctx):
        for alt_nick in nicks:
            if alt_nick in HIGHLIGHT_EXPR.findall(message):
                if alt_nick == nick:
                    continue
                relations[nick, alt_nick] = relations.get((nick, alt_nick), 0) + 1
        n_lines += 1
        if n_lines % 1000 == 0:
            sys.stderr.write("{}... ".format(n_lines))

    sys.stderr.write("Collated {} relations from {} lines.\n".format(len(relations), n_lines))

    return relations

def generate_synopsis(relations):
    # Generate the synopsis file.
    synopsis = []

    for (from_, to), count in relations.iteritems():
        synopsis.append({
            'from': from_,
            'to': to,
            'count': count
        })

    return synopsis

def generate_json(fmt, input_fn, output_fn=None, **ctx):
    # Dump relations to a JSON file.
    with open(input_fn, "r") as f:
        nicks = generate_nicks(f, fmt, **ctx)

    with open(input_fn, "r") as f:
        relations = generate_relations(f, fmt, nicks, **ctx)

    synopsis = generate_synopsis(relations)

    if output_fn is None:
        print(json.dumps(synopsis))
    else:
        with open(output_fn, "w") as f:
            json.dump(synopsis, f)

