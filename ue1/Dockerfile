# Use the correct Go version (1.24)
FROM golang:1.24 as builder

WORKDIR /app

# Copy go.mod and go.sum
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the entire project
COPY . .

# Build the application
RUN go build -o recipe .

# Final minimal runtime image
FROM alpine:latest  

WORKDIR /app

# Install required packages for PostgreSQL compatibility
RUN apk add --no-cache ca-certificates libc6-compat

# Copy recipe from the builder
COPY --from=builder /app/recipe /app

# Expose port
EXPOSE 8080

# Run the application
CMD ["./recipe", "serve"]
