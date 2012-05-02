# Generate the graph data structures.

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

import binascii
import json
import math

def generate_counts_and_connections(synopsis,
                                    synonyms=None,
                                    case_insensitive=True,
                                    strip_trailing_underscores=False):
    if synonyms is None:
        synonyms = {}

    connections = {}
    counts = {}

    if case_insensitive:
        nick_mappings = {}

    def process_nick(nick):
        if strip_trailing_underscores:
            nick = nick.rstrip('_')
        return nick

    for d in synopsis:
        from_, to = sorted((process_nick(d['from']), process_nick(d['to'])))

        from_ = synonyms.get(from_, from_)
        if case_insensitive:
            from_ = nick_mappings.setdefault(from_.lower(), from_)

        to = synonyms.get(to, to)
        if case_insensitive:
            to = nick_mappings.setdefault(to.lower(), to)

        if from_ == to:
            continue

        counts[from_] = counts.get(from_, 0) + d['count']
        counts[to] = counts.get(to, 0) + d['count']
        connections[from_, to] = connections.get((from_, to), 0) + d['count']

    return counts, connections

def generate_graph(counts, connections, **ctx):
    max_count = max(*connections.values())

    style = ctx['style']
    palette = style['palette']

    buf = StringIO()
    buf.write('graph {{ graph [K=0.8 bgcolor="{background_color}"]; node [shape=none fontname="{font}"];\n'.format(
        font=style["font"],
        background_color=style["background_color"]
    ))
    for nick, count in counts.iteritems():
        buf.write('"{nick}" [fontsize="{size}px" fontcolor="{color}"];\n'.format(
            nick=nick,
            size=int(style['nick_size_minimum'] + style['nick_size_multiplier'] * math.log(count, style['nick_size_log_base'])),
            color=palette[(binascii.crc32(nick.lower()) & 0xffffffff) % len(palette)]
        ))

    for (from_, to), count in connections.iteritems():
        t = count / max_count

        alpha_range = style['relation_max_alpha'] - style['relation_min_alpha']
        fac = style['relation_min_alpha'] + int(t ** style['relation_alpha_exponent'] * alpha_range)
        color = "%.2x" % fac

        buf.write('"{from_}" -- "{to}" [color="#ffffff{color}" penwidth={width}];\n'.format(
            from_=from_,
            to=to,
            color=color,
            width=style['relation_size_minimum'] + style['relation_size_multipler'] * math.log(count, style['relation_size_log_base'])
        ))

    buf.write("}")
    buf.seek(0)
    return buf.read()

def generate_dot(input_fn, output_fn=None, **ctx):
    with open(input_fn, "r") as f:
        synopsis = json.load(f)

    counts, connections = generate_counts_and_connections(
        synopsis,
        ctx['synonyms'],
        ctx['case_insensitive'],
        ctx['strip_trailing_underscores']
    )

    graph = generate_graph(counts, connections, **ctx)

    if output_fn is None:
        print graph
    else:
        with open(output_fn, "w") as f:
            f.write(graph)


