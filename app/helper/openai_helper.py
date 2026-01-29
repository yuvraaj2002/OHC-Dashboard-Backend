import logging
import traceback
from openai import OpenAI
from pydantic import BaseModel
from tenacity import (retry,stop_after_attempt,wait_exponential,retry_if_exception_type)
from app.core.config import settings

logger = logging.getLogger(__name__)

def _before_sleep(retry_state):
    """Log traceback before each retry."""
    if retry_state.outcome and retry_state.outcome.failed:
        exc = retry_state.outcome.exception()
        logger.warning(
            "OpenAI API call failed (attempt %s/%s). Retrying with exponential backoff.\n%s",
            retry_state.attempt_number,
            5,
            "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
        )


class OpenAIHelper:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=60),
        retry=retry_if_exception_type(Exception),
        before_sleep=_before_sleep,
        reraise=True,
    )
    def structured_inference(
        self, model: str, input: list, temperature: float, text_format: BaseModel,input_token_cost: float,output_token_cost: float):
        response = self.client.responses.parse(
            model=model,
            temperature=temperature,
            input=input,
            text_format=text_format,
        )
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost = self.calculate_cost(input_tokens, output_tokens, input_token_cost, output_token_cost)
        return response.output_parsed,cost


    @staticmethod
    def calculate_cost(input_tokens: int,output_tokens: int,input_token_cost: float,output_token_cost: float) -> float:
        """Calculate total cost based on token counts and cost per million tokens."""
        input_cost = (input_tokens / 1_000_000) * input_token_cost
        output_cost = (output_tokens / 1_000_000) * output_token_cost
        return input_cost + output_cost