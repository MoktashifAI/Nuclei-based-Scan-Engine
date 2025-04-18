# Stage 1: Build Nuclei
FROM golang:1.21-alpine AS builder
RUN apk add --no-cache git
RUN go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Stage 2: Final image
FROM python:3.9-alpine
LABEL maintainer="Mohamed Khattab <motahakhatttab98@gmail.com>"

# Copy Nuclei binary from builder
COPY --from=builder /go/bin/nuclei /usr/local/bin/nuclei

# Install runtime dependencies
RUN apk add --no-cache --virtual .runtime-deps \
    libstdc++ \
    openssl \
    ca-certificates \
    && update-ca-certificates

# Install build dependencies (temporary)
RUN apk add --no-cache --virtual .build-deps \
    g++ \
    make \
    libffi-dev \
    openssl-dev \
    && pip install --no-cache-dir flask requests \
    && apk del .build-deps

# Copy application files
WORKDIR /app
COPY Scanner_Nuclei/ /app/

# Verify installations
RUN nuclei -version

# Expose and run
EXPOSE 5000
CMD ["python", "ScanEngine_Nuclei_API.py"]
