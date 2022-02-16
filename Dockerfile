FROM python:3.9-alpine

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev
WORKDIR /opt/oci_auto
COPY src/requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY src/ ./
CMD ["python", "main.py"]
