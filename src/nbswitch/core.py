from count_tokens.count import count_tokens_in_string
from litellm import completion
from openai import OpenAI
from instructor import Instructor
import instructor
import os
# from models import ProviderDetails, ListOfCells
from pydantic import Field
from anthropic import Anthropic
from groq import Groq
from cohere import Client
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
import nbformat
from faker import Faker
from nbformat.notebooknode import NotebookNode
from pathlib import Path
from litellm import token_counter


def create_client(
    # details: ProviderDetails = ProviderDetails()
    provider: str,
    api_key: str = None,
    base_url: str = None
) -> Instructor:
    if provider == "OpenAI":
        return instructor.from_openai(
            OpenAI(), api_key=api_key if api_key else os.getenv("OPENAI_API_KEY"),
        )
    
    elif provider == "Cohere":
        return instructor.from_cohere(
            Client(), api_key=api_key if api_key else os.getenv("COHERE_API_KEY"),
        )
    
    elif provider == "Groq":
        return instructor.from_openai(
            Groq(api_key=api_key if api_key else os.getenv("GROQ_API_KEY"))
        )
    
    elif provider == "Ollama":
        return instructor.from_openai(
            OpenAI(
                base_url=base_url if base_url else "http://localhost:11434/v1",
                api_key="ollama",
            )
        )
    
    elif provider == "Anthropic":
        return instructor.from_anthropic(
            Anthropic(api_key=api_key if api_key else os.getenv("ANTHROPIC_API_KEY")),
        )
    
    else:
        raise ValueError(
            f'Sorry, the name {provider} is not a package. Please use one of the following names:'
            "Anthropic, OpenAI, Ollama, Cohere, HuggingFace, Groq, LlamaCPP"
        )


# def number_of_passes(messages: list[dict[str, str]]):
#     token_count = token_counter(messages=messages)
#     if token_count > 4_096:
        



def notebook_to_html(notebook):
    html_exporter = HTMLExporter()
    html_exporter.template_name = 'basic'
    (body, _) = html_exporter.from_notebook_node(notebook)

    soup = BeautifulSoup(body, 'html.parser')
    for cell in soup.find_all('div', class_='cell'):
        cell['class'] = cell.get('class', []) + ['notebook-cell']

    return str(soup)

def old_cells_needed(notebook, first_pass):
    cells_needed = []
    for i in notebook.cells:
        for num in first_pass.cells_of_interest:
            if i['metadata']['index'] == num:
                cells_needed.append(({"cell_type": i['cell_type'], 'metadata': {'index': num}}))
    return cells_needed

def merge_nbs(notebook, second_pass):
    for i in second_pass.full_nb:
        index = i.metadata['index']
        notebook.cells[index]['source'] = i.source
    return notebook


def save_doc(new_notebook):
    new_notebook_path = os.path.join(os.path.dirname(__file__), f"new_placeholder.ipynb")
    with open(new_notebook_path, 'w') as f:
        nbformat.write(new_notebook, f)

def read_doc(doc: Path | str) -> tuple[NotebookNode, int]:
    with open(doc, 'r') as f:
        notebook = nbformat.read(f, as_version=4)
        num_of_cells = len(notebook.cells)
    return notebook, num_of_cells

    # if ".ipynb" in doc:

    # content = doc.read()
    # # content = await doc.read()
    # return nbformat.reads(content.decode(), as_version=4)

def enumerate_document(nb):
    for i, cell in enumerate(nb.cells):
        cell["metadata"] = {"index": i}
    return nb

def split_nb(doc):
    count = token_counter(text=str(doc.cells))
    if count > 2_000 and count < 3_500:
        return 2
    elif count >= 3_500 and count < 5_500:
        return 3
    elif count >= 5_500 and count < 7_500:
        return 4
    elif count >= 7_500 and count < 10_000:
        return 5
    else:
        answer = input (f"Your notebook is quite large with roughly {count} tokens, are you sure you want to continue? (y/n) ")
        if answer == 'y':
            return 8
        elif answer == 'n':
            exit()
        else:
            ValueError(f"You answered {answer}, please select one of the following options: 'y' for 'yes' or 'n' for 'no'")
            split_nb()


def this():
    pass