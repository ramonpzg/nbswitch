from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from prompts import PROMPT_1, PROMPT_2, SYSTEM_PROMPT

from utils import *
import nbformat
import os

app = FastAPI()


@app.post("/process")
async def process_notebook(
    notebook: UploadFile = File(...),
    prompt: str = Form(...),
    model: str = "claude-3-5-sonnet-20240620"
) -> HTMLResponse:

    notebook = read_doc(notebook)
    old_html = notebook_to_html(notebook)
    notebook = enumerate_document(notebook)

    PROMPT_1 = PROMPT_1.format(one=notebook, two=prompt)

    cells_needed = old_cells_needed(notebook, first_pass)

    PROMPT_2 = PROMPT_2.format(one=notebook.cells, two=cells_needed, three=cells_needed, four=prompt)

    new_notebook = merge_nbs(notebook, second_pass)
    new_html_notebook = notebook_to_html(new_notebook)

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
