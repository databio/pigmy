#!/usr/bin/env python

from __future__ import print_function
from argparse import ArgumentParser
import yaml

parser = ArgumentParser(description='Bam processor')

parser.add_argument('-g', '--grant_source',
    help="Grants source yaml file", default=None,
    required=True)

parser.add_argument('-s', '--status',
    help="Filter status", nargs="+", default=None)

parser.add_argument('-d', '--document-template',
    help="Document with liquid-like status tags", default=None)

parser.add_argument('-f', '--format-template',
    help="Text file with output format template",
    default="formats/no_amounts.txt")

parser.add_argument('-e', '--effort',
    help="Convert effort to cal. months?", default=False,
    action="store_true")

args = parser.parse_args()

if args.document_template and args.status:
    print("Status options are ignored if a document template is provided.")

import sys
grants = yaml.safe_load(file(args.grant_source, 'r'))

with open(args.format_template, "r") as f:
    outformat = f.read() 


def simple_format(string, vars):
    try:
        result = string.format(**vars)
    except KeyError as e:
        key = e.args[0]
        print("Warning, adding missing key: " + key, file=sys.stderr)
        vars[key] = ""
        return simple_format(string, vars)
    return result


def format_grants(grants, outformat, status_list=None):
    # Set up a list to accumulate grants
    formatted_grants = []
    for g in grants:
        # print(g)
        if not "PI" in g.keys() and g["role"] == "PI":
            g["PI"] = "Sheffield"

        g["namePlusPI"] = "{name} ({PI})".format(**g)
        
        if status_list:
            if not g["status"] in status_list:
                continue
        if args.effort:
            try: 
                g["effort"] = str(float(g["effort"]) * 12) + " calendar months"
            except ValueError:
                g["effort"] = ""
        else:
            try:
                g["effort"] = str(int(float(g["effort"]) * 100)) + "%"
            except ValueError:
                g["effort"] = "0%"
        # Use a weird character we expect NOT to be there for padding,
        # because we will replace it momentarily
        g["char"] = "`"
        formatted = simple_format(outformat, g)
        formatted = formatted.replace("`", "&#02; ")
        formatted_grants.append(formatted)

    totalout = '\n'.join(formatted_grants)
    return(totalout)


if args.document_template:
    with open(args.document_template, "r") as f:
        doctemplate = f.read()

    doc = doctemplate.format(   active=format_grants(grants, outformat, "active"), 
                                pending=format_grants(grants, outformat, "pending"),
                                rejected=format_grants(grants, outformat, "rejected"))

    print(doc)


else:
    print(format_grants(grants, outformat, args.status))
