# FormalLanguageTheory
### Practical assignments for the formal language theory course at SPBU
 - PR build results avaliable at 
[![Build Status](https://travis-ci.org/github/AlekseiPrivalihin/FormalLanguageTheory/pull_requests)](https://travis-ci.org/github/AlekseiPrivalihin/FormalLanguageTheory/pull_requests)
 - Only Docker and git are required to run the tests (they are being run as a part of the docker build process) and the utility itself
  - First, clone this repo by running
    `git clone https://github.com/AlekseiPrivalihin/FormalLanguageTheory.git`
  - Then go to the repo folder and build the docker image by running
    `docker build -t flt --build-arg script="script.txt" .
  - All files must be within repo folder or its subfolders!
  - Lastly, run the image using
    `docker run formal_language_theory`
  - The first line of output is the result of CYK for given script (whether the script is correct within defined syntax)
### Database query syntax
  - The script must be a sequence of statements separated by semicolons
  - The number of whitespace characters does not matter
  - Double quotes, however, are mandatory where specified
  - Only characters [a-z], [0-9], '.', '/' and '_' are supported for identifiers (database and graph names) and strings
  - Only two statements are currently supported:
    - connect to "<database_name>"
    - select <objective> from <graph>
  - Objective can be specified as 'edges' or 'count edges'
  - Graph can be specified via its name: 
    - select edges from graph "<graph_name>"
  - Or as a pattern (regex) query:
    - select count edges from query "<pattern>"
  - Or as an intersection of graphs:
    - select edges from graph "graph" intersect with "other_graph"
  - Patterns support brackets, Kleene star (\*), alternatives (|), concatenation, optional characters (?) and the + operator (one or more entries)
    For example: a|b*(abc)+d?
