import logging
from aws_lambda_typing.events import SQSEvent
from aws_lambda_typing.context import Context

from src.domain.response import Response


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: SQSEvent, context: Context) -> Response:
    try:
        response = Response(status=200, message="Event processed successfully")
        return response.model_dump_json(exclude_none=True)
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        response = Response(status=500, message="Internal Server Error", details=str(e))
        return response.model_dump_json(exclude_none=True)


