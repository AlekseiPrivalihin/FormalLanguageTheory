FROM graphblas/pygraphblas-minimal:latest

RUN mkdir /formalLanguageTheory
WORKDIR /formalLanguageTheory
COPY . /formalLanguageTheory

RUN pip3 install -r requirements.txt
CMD ["pytest"]