from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
import nbformat
from faker import Faker

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

def read_doc(doc):
    content = await doc.read()
    return nbformat.reads(content.decode(), as_version=4)

def enumerate_document(doc):
    for i, cell in enumerate(doc.cells):
        cell["metadata"] = {"index": i}
    return doc
