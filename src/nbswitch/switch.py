from instructor import Instructor
from pydantic import Field
from .models import ListOfCells, FullNotebook
from .prompts import SYSTEM_PROMPT, PROMPT_1
from nbformat.notebooknode import NotebookNode

def first_pass(
    client: Instructor,
    model: str,
    prompt: str,
    notebook: NotebookNode,
    system_prompt: str = SYSTEM_PROMPT,
    base_prompt: str = PROMPT_1,
    # output_model: ListOfCells,
    max_tokens: int = 4_096,#Field(default=4_096, ge=20),
    # max_retries: int = Field(default=3, le=10, ge=0),
    max_retries: int = 3,
) -> ListOfCells:
    if client.provider.name == "ANTHROPIC":
        return client.chat.completions.create(
            model=model,
            system=system_prompt,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": base_prompt.format(notebook=notebook, prompt=prompt)}],
            max_retries=max_retries,
            response_model=ListOfCells
        )
    else:
        return client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt}, 
                {"role": "user", "content": base_prompt.format(notebook=notebook, prompt=prompt)}
            ],
            max_retries=max_retries,
            response_model=ListOfCells
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
