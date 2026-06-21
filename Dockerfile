FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl zip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/var/task
ENV AWS_LAMBDA_RUNTIME_API=""

WORKDIR /var/task

COPY pyproject.toml .
COPY uv.lock .

RUN uv export --format requirements.txt > requirements.txt && \
    uv pip install --system -r requirements.txt && \
    pip install --no-cache-dir awslambdaric

ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/local/bin/aws-lambda-rie
RUN chmod +x /usr/local/bin/aws-lambda-rie

COPY . .
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD [ "lambda_function.lambda_handler" ]
