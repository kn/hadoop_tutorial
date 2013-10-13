#!/usr/bin/env python

import sys

(last_word, count) = (None, 0)

for line in sys.stdin:
  (word, val) = line.strip().split('\t')
  if last_word and last_word != word:
    print '%s\t%s' % (last_word, count)
    (last_word, count) = (word, 1)
  else:
    (last_word, count) = (word, count + 1)

if last_word:
  print '%s\t%s' % (last_word, count)
