FROM graphblas/pygraphblas-minimal:latest
ARG regex
ENV regex ${regex}
ARG string
ENV string ${string}

RUN mkdir /formalLanguageTheory
WORKDIR /formalLanguageTheory
COPY . /formalLanguageTheory

RUN pip3 install -r requirements.txt
RUN echo $regex
RUN echo $string
RUN python3 -m pytest -v -s
CMD python3 main.py --regex $regex --string $string

