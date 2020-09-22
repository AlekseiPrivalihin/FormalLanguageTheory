# FormalLanguageTheory
### Practical assignments for the formal language theory course at SPBU
 - PR build results avaliable at 
[![Build Status](https://travis-ci.org/github/AlekseiPrivalihin/FormalLanguageTheory/pull_requests)](https://travis-ci.org/github/AlekseiPrivalihin/FormalLanguageTheory/pull_requests)
 - Only Docker and git are required to run the tests (they are being run as a part of the docker build process) and the utility itself
  - First, clone this repo by running
    `git clone https://github.com/AlekseiPrivalihin/FormalLanguageTheory.git`
  - Then go to the repo folder and build the docker image by running
    `docker build -t formal_language_theory --build-arg graph=<path to graph file> --build-arg regex=<path to regex file> [--build-arg initial=<path to initial set file>] [--build-arg destination=<path to destination set file>] .`
  - All files must be within repo folder or its subfolders!
  - Lastly, run the image using
    `docker run formal_language_theory`
  - To run multiple queries on a single graph, copy all regex files into <repo_dir>/regexes and use --build-arg regex='ALL' when building the Docker image
  - To reduce excessive output it is also recommended to use an empty text file as --build-arg initial
  - The output now contains information about time spent on different tasks