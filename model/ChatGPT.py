import time
from typing import Tuple

import backoff
import openai
import tiktoken


class ChatGPT:
    _api_key: str = ""

    def __init__(
        self, price_per_1k_tokens: float, max_context_tokens_length: int
    ) -> None:
        self.last_generate_time = None
        self._token_count = 0

        self.price_per_1k_tokens = price_per_1k_tokens
        self.max_context_tokens_length = max_context_tokens_length

    """
    設置 API Key 是全局設置的，不限於 Instance
    """

    @staticmethod
    def set_api_key(api_key: str) -> None:
        ChatGPT._api_key = api_key
        openai.api_key = ChatGPT._api_key

    @backoff.on_exception(backoff.expo, openai.error.APIError)
    @backoff.on_exception(backoff.expo, openai.error.ServiceUnavailableError)
    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    def generate_response(self, prompt: str) -> dict:
        # Check API Key setting
        if ChatGPT._api_key == "":
            raise Exception("Need to set API Key with ChatGPT.set_api_key()")

        """
        API 參數參考: https://platform.openai.com/docs/api-reference/chat/create#chat/create-max_tokens
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # max_tokens=128, # Completion 可產生的最大 token 數，預設是無限，輸入和輸出的總長受到 context length 的限制
            # temperature=1.0, # 0~2 較高的數值會讓回應更有變化，預設是 1
            # n=1, # 產生幾個回應，預設是 1
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        self.last_generate_time = time.time()
        self._token_count += response["usage"]["total_tokens"]

        return response

    def init_count_token_usage(self) -> None:
        self._token_count = 0

    def get_token_usage_and_cost(self) -> Tuple[int, float]:
        return self._token_count, self._token_count / 1000 * self.price_per_1k_tokens

    def count_message_token(self, message: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        encoded_message = encoding.encode(message)

        return len(encoded_message)

    def check_message_token_length_limit(self, message: str) -> bool:
        return self.count_message_token(message) <= self.max_context_tokens_length
