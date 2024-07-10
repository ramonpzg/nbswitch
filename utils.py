from nbconvert import HTMLExporter
from bs4 import BeautifulSoup

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