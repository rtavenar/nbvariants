#!/usr/bin/env python

import sys
from . import single_source_multi_output

def main_cli():
    if "-h" in sys.argv or "--help" in sys.argv or len(sys.argv) % 2 != 0:
        print("nbvariants is a command-line script\n  that generates "
              "variants of an input notebook\n  in which only code cells "
              "with the given tags are kept\n  and others are made blank.\n\n"
              "Calls should look like:\n")
        print("nbvariants input_notebook "
            "output_notebook1 tag1_0,tag1_1,tag1_2 "
            "[output_notebook2 tag2_0,tag2_1] ...\n")
        print("A list of tags equal to - means\n  all code cells should be blanked out.\n")
        sys.exit()

    input_notebook = sys.argv[1]
    tags_per_notebook = {}
    for i in range(2, len(sys.argv), 2):
        if i + 1 >= len(sys.argv):
            list_of_tags = []
        else:
            list_of_tags = sys.argv[i + 1].strip().split(",")
            if list_of_tags == ["-"]:
                list_of_tags = []
        tags_per_notebook[sys.argv[i].strip()] = list_of_tags
    single_source_multi_output(input_notebook, tags_per_notebook)