FROM python

WORKDIR /app

# Set the secret as an environment variable inside the container
ENV STORAGE_ID=${STORAGE_ID}

# Copy local files
COPY . .

# Install required dependencies
RUN pip install -r requirements.txt


# Download Google Drive file and verify it exists
# RUN bash -c 'curl -L -o test.json "https://drive.google.com/uc?export=download&id=${STORAGE_ID}" && ls -lah test.json && cat test.json || echo "Download failed!"'

RUN wget -O test.json "https://drive.google.com/uc?export=download&id=${STORAGE_ID}" && cat test.json



# Install Google Chrome stable version
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

RUN pytest app.py --html=report.html --self-contained-html || true
