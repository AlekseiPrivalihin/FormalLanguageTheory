FROM graphblas/pygraphblas-minimal:latest
ARG graph
ENV graph ${graph}
ARG cfg
ENV cfg ${cfg}
ARG string
ENV string ${string}

RUN mkdir /formalLanguageTheory
WORKDIR /formalLanguageTheory
COPY . /formalLanguageTheory

RUN pip3 install -r requirements.txt
RUN echo $graph
RUN echo $regex
RUN echo $initial
RUN echo $destination
RUN python3 -m pytest -v -s
CMD python3 main.py --graph $graph --cfg $cfg --string $string

