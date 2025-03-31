# Definiert eine "default" Gruppe
group "default" {
    targets = ["app"] # beinhaltet das Ziel "app"
}

# Definiert das Ziel "app"
target "app" {
    context    = "." # aktuelles Verzeichnis (Dort wo das Dockerfile liegt)
    dockerfile = "Dockerfile" # Unser Dockerfile
    tags       = ["ue1-app:latest", "ue1-app:1.0"] # Tags für das erstelle Docker-Image
    platforms  = ["linux/amd64", "linux/arm64"] # Plattformen, für die gebaut werden soll
    output     = ["type=image"]     # Gibt an, dass das Build-Ergebnis ein Image ist
}
