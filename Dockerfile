FROM python:3.8-buster
RUN apt-get update
COPY catProject .
RUN make requirements
CMD make run
