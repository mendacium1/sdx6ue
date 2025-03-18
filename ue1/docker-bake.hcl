group "default" {
    targets = ["app"]
}

target "app" {
    context    = "."
    dockerfile = "Dockerfile"
    tags       = ["ue1-app:latest", "ue1-app:1.0"]
    platforms  = ["linux/amd64", "linux/arm64"]
    output     = ["type=image"]
}
