from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from anthropic import Anthropic
import instructor

from pydantic.types import Literal, List, Union
from pydantic import BaseModel, Field
from utils import *
import nbformat
import os

app = FastAPI()

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


@app.post("/process")
async def process_notebook(notebook: UploadFile = File(...), prompt: str = Form(...)):
    content = await notebook.read()
    notebook = nbformat.reads(content.decode(), as_version=4)
    for i, cell in enumerate(notebook.cells):
        cell["metadata"] = {"index": i}

    old_html = notebook_to_html(notebook)
    sonnet = "claude-3-5-sonnet-20240620"
    client = instructor.from_anthropic(Anthropic(api_key=os.getenv("ANTRHOPIC_API_KEY")))

    PROMPT_1 = (
        "The following is a jupyter notebook with cells as dictionaries inside a Python list.\n\n"
        "{one}\n\n"
        "Inside the 'source' key is where any code or markdown goes in.\n"
        "Later on, your task will be to change the context of the lesson to the following prompt: {two}\n\n"
        "Right now you need to do the following four things:\n\n"
        "1. Read the entire notebook and reason through it. For example, evaluate the use case, what is good about it and how could it be improved and keep that knowledge to yourself.\n"
        "2. Go back to the beginning and pay attention to the number of each cell, which can be found inside the metadata key as 'index': number_of_the_cell.\n"
        "3. Determine which cells need to change to adapt the lesson to the use case described in the prompt above in both code and prose.\n"
        "4. Return a Python list with the numbers of ABSOLUTELY NECESSARY cells that need to be changed and nothing else. "
        "For example, if you are not going to change the tile of a section, don't pick it, as we can work on it together later. When in doubt, leave the cell be"
    )

    PROMPT_1 = PROMPT_1.format(one=notebook, two=prompt)

    SYSTEM_PROMPT = """You are an AI assistant specialized in modifying Jupyter notebooks 
    and markdown files. Your task is to take an existing educational notebook and change 
    its use case while \nmaintaining the overall structure and logic of the prose and code. 
    You always provide clear explanations \nfor any code you rewrite and you have a terse 
    but casual tone."""

    first_pass = client.messages.create(
        model=sonnet,
        system=SYSTEM_PROMPT,
        max_tokens=4096,
        messages=[{"role": "user", "content": PROMPT_1}],
        max_retries=1,
        response_model=ListOfCells
    )

    cells_needed = old_cells_needed(notebook, first_pass)

    PROMPT_2 = (
        "The following is jupyter notebook with cells as dictionaries inside a Python list.\n\n"
        "{one}\n\n"
        "Inside the 'source' key is where any code or markdown goes in.\n"
        "Your task will be to change the context of the lesson to the topic in this prompt: {four}\n\n"
        "You will do this task in the following step-by-step process:\n\n"
        "1. Read the entire notebook and reason through it. For example, evaluate the use case, what is good about it and how could it be improved when changing to the "
        "user's prompt above. You can use synthetic data for the code pieces, and, if you see quotes from authors or articles, feel free to come up with another kind of idea.\n"
        "2. Once you have read through it, your main task is to change and return ONLY THE CELLS with the following cell_type and indexes inside:\n\n{two}.\n\n"
        "Remember, pay attention to whether the cell is a 'markdown' or a 'code' and return the appropriate one. Also, please ONLY update and return the new cells based on those with the following 'cell_tags' and 'indexes' inside the metadata tag:\n\n{three}\n\n"
        "Lastly, be as concise as you possibly can to get the message across. Be terse and to the point but always keep a touch of dry humor in your tone. If you need to summarize the content a bit more to finish the job, do it."
    )

    PROMPT_2 = PROMPT_2.format(one=notebook.cells, two=cells_needed, three=cells_needed, four=prompt)

    second_pass = client.messages.create(
        model=sonnet,
        system=SYSTEM_PROMPT,
        max_tokens=4096,
        messages=[{"role": "user", "content": PROMPT_2}],
        max_retries=3,
        response_model=FullNotebook
    )

    new_notebook = merge_nbs(notebook, second_pass)
    new_html_notebook = notebook_to_html(new_notebook)

    new_notebook_path = os.path.join(os.path.dirname(__file__), f"new_placeholder.ipynb")
    with open(new_notebook_path, 'w') as f:
        nbformat.write(new_notebook, f)

    return HTMLResponse(content=f"""
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6 mb-4">
        <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Notebooks</h2>
        <div id="notebook-diff" class="notebook-container">
            <div class="flex notebook-content">
                <div class="w-1/2 pr-2">
                    <h3 class="text-lg font-semibold mb-2 text-gray-800 dark:text-white">Original</h3>
                    <div id="old-content" class="bg-gray-100 p-4 rounded-md overflow-x-auto text-sm">{old_html}</div>
                </div>
                <div class="w-1/2 pl-2">
                    <h3 class="text-lg font-semibold mb-2 text-gray-800 dark:text-white">Modified</h3>
                    <div id="new-content" class="bg-gray-100 p-4 rounded-md overflow-x-auto text-sm">{new_html_notebook}</div>
                </div>
            </div>
        </div>
    </div>
    <div id="old-notebook" class="hidden">{content.decode()}</div>
    <div id="new-notebook" class="hidden">{nbformat.writes(new_notebook)}</div>
    """)


app.mount("/", StaticFiles(directory="static", html=True), name="static")