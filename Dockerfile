FROM python:3.8-buster
RUN apt-get update
COPY catProject .
RUN make requirements
RUN make migration
RUN make migrate
RUN make superuser
CMD make run
