FROM golang:1.24 as builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o recipe .
FROM alpine:latest
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
RUN apk add --no-cache ca-certificates libc6-compat
COPY --from=builder /app/recipe /app/recipe
RUN chown -R appuser:appgroup /app
USER appuser
EXPOSE 8080
CMD ["./recipe", "serve"]

