# Hadoop Tutorial

## Install hadoop

1. Download hadoop tar ball from stable [hadoop release](http://hadoop.apache.org/releases.html) (1.2.1 was used with this example)
2. Unzip the downloaded package into `/usr/local` or somewhere else if you have a preference
3. Create symlink: `ln -s /user/local/hadoop-1.2.1 /usr/local/hadoop`
4. Export a several environment variables:
```
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin
```

## MapReduce (Streaming) with single node

In this section, we will run simple word count MapReduce job using Streaming under single node setup.

Our map function will break down a sentence into a word and emit each of them with value 1.
```python
# src/word_count_map.py
#!/usr/bin/env python

import re
import sys

for line in sys.stdin:
  sentence = line.strip()
  sentence = re.sub(r'[,.]', '', sentence)
  for word in sentence.split():
    print '%s\t%s' % (word, 1)
```

Our reduce function will count total occurence of each word.
```python
# src/word_count_reduce.py
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
```

Now we can run this MapReduce function using hadoop:
```
hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-*.jar \
-input data/sentences.txt \
-output output \
-mapper src/word_count_map.py \
-reducer src/word_count_reduce.py
```

If the job is successful, it should create `output` directory and `output/part-00000.txt`, which contains a result.

## Setup HDFS and MapReduce in pseudodistributed mode

1. On Mac OS X, make sure Remote Login (under System Preferences -> Sharing) is enabled for the current user
2. Make sure you can ssh to localhost: `ssh localhost`
3. Format a namenode of HDFS: `hadoop namenode -format`
4. Copy required pseudodistributed configs: `cp pseudodistributed/* $HADOOP_HOME/config`
5. Start HDFS (a namenode, a secondary namenode and a datanode): `start-dfs.sh` (You can check if it's successful by accessing http://localhost:50070/) 
6. Start MapReduce (a jobtracker and a task tracker): `start-mapred.sh` (You can check if it's successful by accessing http://localhost:50030/)

That's all. You are now running HDFS and MapReduce locally!
