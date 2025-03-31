# syntax=docker/dockerfile:1

##
## Build
##
# Go-Image mit Debian Bullseye als Build-Umgebung
FROM golang:1.24-bullseye AS build 

# Aktualisiert Paketlisten u. installiert updates
RUN apt-get update && apt-get upgrade -y

# Setzt das Arbeitsverzeichnis auf /app
WORKDIR /app

# Kopiert den Inhalt des lokalen src-Ordners ins Arbeitsverzeichnis
COPY src ./
# Lädt alle Go-Abhängigkeiten herunter u. Baut das Projekt u. erstellt binary unter /recipe-api
RUN go mod download \
    && go build -o /recipe-api

##
## Deploy
##
# Erstellt eine neue (minimale) Laufzeitumgebung (ohne Go)
FROM debian:bullseye-slim

# Erstellt einen neuen Benutzer namens "recipe" mit bash als shell
RUN useradd -s /bin/bash recipe

# Setzt das Arbeitsverzeichnis auf das Root-Verzeichnis
WORKDIR /
# Kopiert das zuvor erstellte Binary in diesen Container
COPY --from=build /recipe-api /recipe-api
# Gibt Port 8080 Frei
EXPOSE 8080

# Führt den Container unter dem Nutzer "recipe" aus
USER recipe

# Setzt das Standard-Startkommando auf "/recipe-api" (Führt die Binary aus)
ENTRYPOINT ["/recipe-api"]
# Übergibt das Argument "serve" an die Binary (für Serverstart)
CMD [ "serve" ]
