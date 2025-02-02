FROM python

WORKDIR /app

# Accept secret as a build argument
ARG STORAGE_ID

# Set the secret as an environment variable inside the container
ENV STORAGE_ID=${STORAGE_ID}

# Copy local files
COPY . .

# Install required dependencies
RUN pip install -r requirements.txt

# Download Google Drive file using a script
RUN bash -c 'curl -L -o test.json "https://drive.google.com/uc?export=download&id=${STORAGE_ID}"'

# Define the container's default command (run tests at runtime)
CMD ["pytest", "app.py", "--html=report.html", "--self-contained-html"]
