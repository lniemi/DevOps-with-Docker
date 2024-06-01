# Use an official Ubuntu base image
FROM ubuntu:22.04

# Install curl
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Add the script file to the container
COPY script.sh /script.sh

# Give execution rights on the script
RUN chmod +x /script.sh

# Command to run on container start
CMD ["/script.sh"]
