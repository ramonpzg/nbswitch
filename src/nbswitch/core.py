from count_tokens.count import count_tokens_in_string
from litellm import completion
from openai import OpenAI
from instructor import Instructor
import instructor
import os
from .models import ProviderDetails, ListOfCells
from pydantic import Field



def create_client(
    ProviderDetails
) -> Instructor:
    if provider == "OpenAI":
        return instructor.from_litellm(
            completion, api_key=api_key if api_key else os.getenv("OPENAI_API_KEY"),
        )
    elif provider == "OpenAI":
        return instructor.from_litellm(
            completion, api_key=api_key if api_key else os.getenv("OPENAI_API_KEY"),
        )
    elif provider == "Ollama":
        return instructor.from_openai(
            OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",
            )
        )
    else:
        return instructor.from_litellm(
            completion, api_key=api_key if api_key else os.getenv("ANTHROPIC_API_KEY"),
        )


def number_of_passes(messages: list[dict[str, str]]):
    token_count = token_counter(messages=messages)
    if token_count > 4_096:
        

def first_pass(
    model: str,
    client: Instructor,
    system_prompt: str,
    prompt: str,
    output_model: ListOfCells,
    max_tokens: int,
    max_retries: int = Field(..., le=10, ge=0),
) -> ListOfCells:
    return client.chat.completions.create(
        model=model,
        system=system_prompt,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
        max_retries=max_retries,
        response_model=output_model
    )


def second_pass():
    return client.chat.completions.create(
        model=sonnet,
        system=SYSTEM_PROMPT,
        max_tokens=4096,
        messages=[{"role": "user", "content": PROMPT_2}],
        max_retries=3,
        response_model=FullNotebook
    )
