import typer
from rich.console import Console
from .core import transform_notebook
from .server import run_server
from typing import Optional, Literal
from .prompts import *
# from pydantic.types import Literal

app = typer.Typer()
console = Console()

@app.command()
def transform(
    input_file: str = typer.Option(..., "--in", help="Input notebook file"),
    output_file: Optional[str] = typer.Option(..., "--out", help="Output notebook file"),
    model: Optional[str] = typer.Option("Sonnet", "--model", help="Model to use for transformation"),
    api_key: Optional[str] = typer.Option(),
    temperature: Optional[float] = typer.Option("",),
    task: Literal["recreate", "translate", "enhance"] = "recreate"

):
    """Transform a Jupyter notebook."""
    try:
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
