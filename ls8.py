#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
file_path = "Users/alxander44/Desktop/cs_unit/sprint_6/Computer-Architecture/Sprint-Challenge--Computer-Architecture/sctest.txt"
cpu.load(file_path)
cpu.run()
