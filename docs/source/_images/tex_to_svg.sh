#!/bin/bash

# Based on a short blog post by Paul R. Dixon
# http://www.lvcsr.com/typesetting-algorithms-in-restructuredtext.html

pdflatex algo.tex; pdf2svg algo.pdf algo.svg
