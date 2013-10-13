#!/usr/bin/env python

import re
import sys

for line in sys.stdin:
  sentence = line.strip()
  sentence = re.sub(r'[,.]', '', sentence)
  for word in sentence.split():
    print '%s\t%s' % (word, 1)
