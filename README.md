# FormalLanguageTheory
### Practical assignments for the formal language theory course at SPBU
 - PR build results avaliable at 
[![Build Status](https://travis-ci.org/github/AlekseiPrivalihin/FormalLanguageTheory/pull_requests)](https://travis-ci.org/github/AlekseiPrivalihin/FormalLanguageTheory/pull_requests)
 - Only Docker and git are required to run the tests (they are being run as a part of the docker build process) and the utility itself
  - First, clone this repo by running
    `git clone https://github.com/AlekseiPrivalihin/FormalLanguageTheory.git`
  - Then go to the repo folder and build the docker image by running
    `docker build -t formal_language_theory --build-arg regex=<path to regex file> --build-arg string=<path to string file> .`
  - All files must be within repo folder or its subfolders!
  - Lastly, run the image using
    `docker run formal_language_theory`