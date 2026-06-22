#!/bin/sh
set -eu

handler="${1:-lambda_function.lambda_handler}"

if [ -z "${AWS_LAMBDA_RUNTIME_API:-}" ]; then
  exec /usr/local/bin/aws-lambda-rie python -m awslambdaric "$handler"
fi

exec python -m awslambdaric "$handler"
