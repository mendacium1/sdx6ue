# syntax=docker/dockerfile:1

##
## Build
##
FROM golang:1.24-bullseye AS build

RUN apt-get update && apt-get upgrade -y

WORKDIR /app

COPY src ./
RUN go mod download \
    && go build -o /recipe-api

##
## Deploy
##
FROM debian:bullseye-slim

RUN useradd -s /bin/bash recipe

WORKDIR /
COPY --from=build /recipe-api /recipe-api
EXPOSE 8080

USER recipe

ENTRYPOINT ["/recipe-api"]
CMD [ "serve" ]
