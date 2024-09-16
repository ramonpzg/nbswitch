from pydantic.types import Literal, List, Union
from pydantic import BaseModel, Field, model_validator
from typing import Optional
from enum import Enum

class MDCell(BaseModel):
    cell_type: Literal['markdown'] = 'markdown'
    metadata: dict = Field(..., default_factory=dict)
    source: str

class CodeCell(BaseModel):
    cell_type: Literal['code'] = 'code'
    execution_count: Union[int, None]
    metadata: dict = Field(..., default_factory=dict)
    outputs: list = Field(..., default_factory=list)
    source: str

class FullNotebook(BaseModel):
    all_cells: List[Union[MDCell, CodeCell]]

class ListOfCells(BaseModel):
    cells_of_interest: List[int]


class Provider(str, Enum):
    ANTHROPIC = "Anthropic"
    OPENAI = "OpenAI"
    OLLAMA = "Ollama"
    COHERE = "Cohere"
    HUGGINGFACE = "HuggingFace"
    GROQ = "Groq"
    LLAMACPP = "LlamaCPP"
    LITELLM = "LiteLLM"

# class ModelDetails(BaseModel):
#     model: Literal[
#         "sonnet",
#         "haiku",
#         "opus",
#         "gpt-4o",
#         "gpt-4o-mini",
#     ] = "sonnet"
#     API_KEY: str

class ProviderDetails(BaseModel):
    provider: Provider = Provider.ANTHROPIC
    api_key: Optional[str] = None
    base_url: Optional[str] = None