import typer
from rich.console import Console
from .core import transform_notebook
from .server import run_server
from typing import Optional, Literal
from .prompts import *
# from pydantic.types import Literal
from pathlib import Path


# app = typer.Typer()
console = Console()

# @app.command()
def transform(
    input_file: str = typer.Option(..., "--in", help="Input notebook file"),
    prompt: str = typer.Option(..., "--in", help="Prompt with your use case or langu"),
    output_file: Optional[str] | None = typer.Option(None, "--out", help="Output notebook file"),
    model_1: Optional[str] = typer.Option("Sonnet", "--model", help="Model to use for transformation"),
    model_2: Optional[str] = typer.Option("Sonnet", "--model", help="Model to use for transformation"),
    provider: str | Path= typer.Option("Anthropic", "--model", help="Model Provider to..."),
    api_key: Optional[str] = typer.Option(),
    temperature: Optional[float] = typer.Option("",),
    task: Literal["recreate", "translate", "enhance"] = "recreate"

):
    """Transform a Jupyter notebook."""
    client = create_client(provider)
    notebook, num_of_cells = read_doc(input_file)
    notebook = enumerate_document(notebook)
    if switch:
        first_nb = first_pass(
            client=client, model=model_1, prompt=prompt, notebook=notebook
        )
        second_nb = second_pass(
            client=client, model=model_2, prompt=prompt,
            notebook=notebook, cells_to_change=first_nb
        )
        new_nb = merge_nbs(notebook, second_nb)
        save_doc(new_nb, output_file=output_file)
        transform_notebook(input_file, output_file, model)
        console.print(f"[green]Notebook transformed successfully: {output_file}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@app.command()
def server():
    """Start the nbswitch server."""
    run_server()

if __name__ == "__main__":
    app()
