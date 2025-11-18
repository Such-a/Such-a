FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN echo '<h1>Hello from Docker container!</h1>' > index.html
CMD ["python3", "-m", "http.server", "80"]
