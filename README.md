# Sociographer: Generate Awesome Social Graph Visualizations

Ever wanted a cool representation of social graphs from conversation logs?
Probably not, but check it out:

![Social Graph of #haskell @ irc.freenode.net](http://i.imgur.com/CpZUZ.jpg)

Pretty neat, huh?

## Getting Started

First, you'll need a config file. Check out the `configs` directory for
examples of these. Once you have one, you can run:

    $ sociographer -c config.json synopsis -o synopsis.json logfile.log

This will generate a synopsis file, which summarizes relations between users
for faster processing.

Next, you can generate the `.dot` graph with:

    $ sociographer -c config.json graph -o graph.dot synopsis.json

The graph can then be rendered using Graphviz (the `fdp` tool does the best job
at it):

    $ fdp -Tpng -ograph.png graph.dot

Ta-da!

