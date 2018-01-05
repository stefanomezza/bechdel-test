# bechdel-test
Implementation of the Bechdel test on a subset of the IMSDB.
The project contains two files:

* **IMSDBParser.py**, which scrapes a subset of the IMSDB and returns a parsed representation of the scrape
* **BechdelTest.py**, which implements the Bechdel Test

plus a data folder containing two lists of male/female names respectively.
This project uses the latest versions of the following external libraries:

* {numpy}
* {lxml}
* {BeautifulSoup}

### IMSDBParser.py

This file contains the IMSDBParser class, which takes as input a number n and allows to obtain a list of n scraped movie scripts from the IMSDB.
The movie scripts are taken by checking on "http://www.imsdb.com/all\%20scripts/" the list of available scripts and then querying the corresponding URL directly.
Since the scripts are encoded in raw HTML without any particular markup, some assumptions were made when parsing:

* It was assumed that all the scripts are wrapped in a \<pre\> tag
* It was assumed that all the speakers in the script are indented at the same level
* It was also assumed that the speakers are also wrapped in \<b\> tags
* It was assumed that the indentation level containing the largest amount of human names in the text is the speakers' column. This was necessary,
          since there is no explicit representation of the speakers' column in the text and the indentation changes slightly from script to script
* It was assumed that the utterances from speakers always come right after the speaker line, and that comments (such as "breathes heavily") are wrapped
          in round brackets

Movies with less than 50 overall utterances were dropped, since they probably don't contain enough spoken dialogues to give a contribution to the statistic.
Also, this allows to remove movies with an unexpected format which sometimes populate the IMSDB.
Additional details on the implementation are included in the comments of the file

### BechdelTest.py

This file contains the implementation of the BechdelTest.
Two different implementations are provided:
* baseline_bechdel_test - which performs a simplified bechdel test (movies with two women talking are considered successful)
* complete_bechdel_test - which performs a complete bechdel test (movies with two women talking about something other than men are successful)

Movies are grouped into two arrays according to whether they passed or not the test.
Afterwards, some very simple statistics are provided on each array, such as average number of dialogue utterances, different speakers and male/female speakers.

### Data

The data used to determine if a name is male/female were taken from the NLP corpora of the CMU AI repository
(http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/areas/nlp/corpora/names/).

Copyright (c) January 1991 by Mark Kantrowitz.
