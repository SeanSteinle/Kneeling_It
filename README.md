## Kneeling It: A Study of NFL Kickoffs

**Description**

My goal with this project is to answer a simple question: should NFL teams let every play touchback--thus starting their drive at the 25 yard line--or should they try to get more and return the ball?

There are two secondary goals to this project as well. First, this project is my first time using R, which I need to learn for a Data Science class next semester. Second, this will hopefully bear a nice kickoff statistics database for other NFL stat-heads.

There are a lot of things to consider in answering this question, but to start, we need clean and reliable data. I started out by cloning Ryan Yurko's repository of web-scraped NFL data, which contains game data, play-by-play data, roster data, and more. For the most part, we'll be looking at the play-by-play data (specifically the kickoff plays). You can find Ryan's repository at: https://github.com/ryurko/nflscrapR-data.

The endpoint for this project will be a Jupiter notebook, or other code/graph/text hybrid that lays out when, where, and why to kneel it.

**Methods**

For the most part, the data cleaning/engineering in this project will be done in Python, with the analysis being conducted in R. Although the play-by-play data has some statistics about kickoffs, they prove largely unreliable (check pbp_boxscores.ipynb). Thus, I used Python's *re* module to collect kickoff statistics from the boxscores. This is possible because the boxscores are written in a fairly regular way, with little deviation. More to come on methods in R.

**Directory**
1. *code/pbp_boxscores.ipynb* - this Jupiter Notebook explores Yurko's data, as well as creates a DF with the relevant kickoff statistics using Python's *re* module.
2. *code/generate_DF.py* - this python script runs through boxscores of every kickoff from 2009-2019 and generates 26 statistics for each play, outputted to a csv file.
3. *code/kickoff_statistics* - the database created in *generate_DF.py*.
4. *requirements.txt* - this file contains all of the necessary modules for running my code. install from the file with *pip install -r requirements.txt*