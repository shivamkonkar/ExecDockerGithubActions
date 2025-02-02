FROM python
WORKDIR /app

# Copy local file
COPY . .

# Install Google Chrome stable version
# RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
#     && apt-get update && apt-get install -y google-chrome-stable \
#     && rm -rf /var/lib/apt/lists/*

# Download Google Drive file
# Curl doesn't follow redirects unless you add the -L option
# To save the contents of your download to a file, add the `-o' option followed by the filename
RUN curl -L -o test.json "https://drive.google.com/uc?export=download&id=${STORAGE_ID}"

RUN pip install -r requirements.txt

RUN pytest app.py --html=report.html --self-contained-html || true



