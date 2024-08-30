import typer
from rich.console import Console
from .core import transform_notebook
from .server import run_server
from typing import Optional, Literal
from .prompts import *
# from pydantic.types import Literal
from pathlib import Path
from typing import Annotated

# app = typer.Typer()
# console = Console()

# @app.command()
def main(
    in_file: Annotated[
        Path | str,
        typer.Argument(help="The notebook you want to modify.")
    ],
    prompt: Annotated[
        str,
        typer.Argument(
            "--prompt",
            "-p",
            help="Describe a use case, language or tone you'd like to apply to your notebook."
        )
    ],
    mode: Annotated[str, typer.Argument()] = "switch",
    provider: str = "Anthropic",
    model: str = "claude-3-5-sonnet-20240620",
    api_key: str | None = None,
    output_file: Path | str | None = None,
    base_url: str | None = None,
    system_prompt: str = SYSTEM_PROMPT,
    fpass_prompt: str = PROMPT_1,
    switch_prompt: str = PROMPT_2,
    translate_prompt: str = PROMPT_3,
    flip_prompt: str = PROMPT_4,
    enhance_prompt: str = PROMPT_5,
    max_tokens: int = Field(4_096, ge=20),
    max_retries: int = Field(default=3, le=10, ge=0),
    joke: Annotated[str, typer.Option(prompt="Would you like to hear jokes while you wait?")],
    animation: Annotated[str, typer.Option(prompt="Would you like to see a cool show while you wait?")],

    # input_file: str = typer.Option(..., "--in", help="Input notebook file"),
    # prompt: str = typer.Option(..., "--in", help="Prompt with your use case or langu"),
    # output_file: Optional[str] | None = typer.Option(None, "--out", help="Output notebook file"),
    # model_1: Optional[str] = typer.Option("Sonnet", "--model", help="Model to use for transformation"),
    # model_2: Optional[str] = typer.Option("Sonnet", "--model", help="Model to use for transformation"),
    # provider: str | Path= typer.Option("Anthropic", "--model", help="Model Provider to..."),
    # api_key: Optional[str] = typer.Option(),
    # temperature: Optional[float] = typer.Option("",),
    # task: Literal["recreate", "translate", "enhance"] = "recreate"

):
    """Transform a Jupyter notebook."""
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


if __name__ == "__main__":
    typer.run(main)
