A very basic AI agent that schedules google meets according to the available appointments.

To build and run the container, follow these steps:
1. Build the Docker image:
    ```bash
    docker build -t [your_dockerhub_username]/email-scheduling-agent .
    ```

2. Prepare your configuration: Create a directory to store your configuration files:
    ```bash
    mkdir -p docker-config
    cp config/config.yaml docker-config/
    cp credentials.json docker-config/
    # If you have token.json, copy it too
    cp token.json docker-config/ # (if exists)
    ```

3. Run the container:
    ```bash
    docker run -d \
    --name email-agent \
    -v $(pwd)/docker-config:/app/config \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/docker-config/credentials.json:/app/credentials.json \
    -v $(pwd)/docker-config/token.json:/app/token.json \
    -e EMAIL_ADDRESS="your-email@example.com" \
    -e EMAIL_PASSWORD="your-email-password" \
    -e OPENAI_API_KEY="your-openai-api-key" \
    [your_dockerhub_username]/email-scheduling-agent
    ```