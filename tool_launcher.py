#!/usr/bin/env python26

"""
Helper script to launch tools.
"""

import os
import sys

sys.path.insert(1, "tools")

tools = filter(lambda t: os.path.isfile(os.path.join("tools", t)), os.listdir("tools"))

toolnum = -1

if len(sys.argv) > 1:
	if sys.argv[1] in tools:
		toolnum = tools.index(sys.argv[1])
		del sys.argv[1]
	else:
		print "Tool '%s' was not found" % sys.argv[1]
else:
	print "Lost Sky Tools Environment Launcher\n"
	print "Select a tool from the list:\n"

	for n, t in enumerate(tools):
		print "%d. %s" % (n + 1, t)

	print "\nIf you require command line arguments, you may pass the tool name as the first argument followed by the " \
	"tool specific arguments."

	try:
		toolnum = int(raw_input("\n> ")) - 1
	except ValueError:
		pass

if 0 <= toolnum < len(tools):
	print "Launching '%s' in the Lost Sky tools environment..." % tools[toolnum]
	execfile(os.path.join("tools", tools[toolnum]))
else:
	print "Failed to launch tool!"