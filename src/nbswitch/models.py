from pydantic.types import Literal, List, Union, Optional
from pydantic import BaseModel, Field


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
    full_nb: List[Union[MDCell, CodeCell]]

class ListOfCells(BaseModel):
    cells_of_interest: List[int]



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
    provider: Literal[
        "Anthropic",
        "OpenAI",
        "Ollama",
        "Cohere",
        "HuggingFace",
        "LlamaCPP",
    ] = "Anthropic"
    api_key: Optional[str]
    url: Optional[str]