FROM graphblas/pygraphblas-minimal:latest
ARG graph
ENV graph ${graph}
ARG regex
ENV regex ${regex}
ARG initial
ENV initial ${initial}
ARG destination
ENV destination ${destination}

RUN mkdir /formalLanguageTheory
WORKDIR /formalLanguageTheory
COPY . /formalLanguageTheory

RUN pip3 install -r requirements.txt
RUN echo $graph
RUN echo $regex
RUN echo $initial
RUN echo $destination
RUN python3 -m pytest -v -s
CMD if [ "x$initial" = "x" ] ; then python3 main.py --graph $graph --regex $regex ; else if [ "x$destination" = "x" ] ; then python3 main.py --graph $graph --regex $regex --initial $initial ; else python3 main.py --graph $graph --regex $regex --initial $initial --destination $destination ; fi ; fi