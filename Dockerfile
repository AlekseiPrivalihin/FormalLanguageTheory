FROM graphblas/pygraphblas-minimal:v3.3.3
ARG script
ENV script ${script}

RUN mkdir /formalLanguageTheory
WORKDIR /formalLanguageTheory
COPY . /formalLanguageTheory

RUN pip3 install -r requirements.txt
RUN echo $script
RUN python3 -m pytest -v -s
CMD python3 main.py --script $script

