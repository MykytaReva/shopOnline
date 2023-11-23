FROM ubuntu:latest


RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates

# Add the f**** certificate
ADD docker/zscaler.pem /usr/local/share/ca-certificates/zscaler.pem

# Update certificate store
RUN chmod 644 /usr/local/share/ca-certificates/zscaler.pem && update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/usr/local/share/ca-certificates/zscaler.pem

RUN apt-get update && apt-get install -y python3 python3-venv python3-pip

RUN python3 -m venv env

COPY requirements.txt .
RUN . env/bin/activate && pip install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt


COPY . .

WORKDIR /app

COPY ./docker/entrypoint.sh entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]
