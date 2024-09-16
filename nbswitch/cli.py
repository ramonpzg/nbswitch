import typer
from rich.console import Console
from .core import NbSwitch
# from .server import run_server
from typing import Optional, Literal
from .prompts import *
# from pydantic.types import Literal
from pathlib import Path
from typing import Annotated

app = typer.Typer(rich_markup_mode="rich")
console = Console()

@app.command(epilog="Made with :heart: in the [blue]D[/blue][red]R[/red]")
def switch(
    file: Annotated[
        str,
        typer.Option("--file", "-f", help="The notebook you want to modify.")
    ],
    prompt: Annotated[
        str,
        typer.Option(
            "--prompt",
            "-p",
            help="Describe a use case, language or tone you'd like to apply to your notebook."
        )
    ],
    # mode: Annotated[str, typer.Argument()] = "switch",
    provider: str = "Anthropic",
    model: str = "claude-3-5-sonnet-20240620",
    # api_key: str | None = None,
    # output_file: Path | str | None = None,
    # base_url: str | None = None,
    # system_prompt: str = SYSTEM_PROMPT,
    # fpass_prompt: str = PROMPT_1,
    # switch_prompt: str = PROMPT_2,
    # translate_prompt: str = PROMPT_3,
    # flip_prompt: str = PROMPT_4,
    # enhance_prompt: str = PROMPT_5,
    # max_tokens: int = Field(4_096, ge=20),
    # max_retries: int = Field(default=3, le=10, ge=0),
    # joke: Annotated[str, typer.Option(prompt="Would you like to hear jokes while you wait?")] = None,
    # animation: Annotated[str, typer.Option(prompt="Would you like to see a cool show while you wait?")] = None,

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
    """Switch the context of a Jupyter notebook."""
    try:
        nb = NbSwitch(file=file, prompt=prompt, provider=provider, model=model)
        nb.create_client()
        nb.read_doc()
        nb.enumerate_document()
        nb.first_pass()
        nb.cells_token_counter()
        nb.cells_token_count
        nb.second_pass()
        nb.merge_nbs()
        nb.save_doc()
        console.print(f"[green]Notebook transformed successfully: {nb.new_notebook_path}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


# @app.command()
# def translate() -> None:
#     pass


# @app.command()
# def server(
#     port: int = 8000,
#     host: str = "localhost",
#     base_url: str | None = None,
#     api_key: str | None = None,
#     system_prompt: str = SYSTEM_PROMPT,
#     fpass_prompt: str = PROMPT_1,
#     switch_prompt: str = PROMPT_2,
# ) -> None:
#     """Run a local server."""
#     run_server(port, host, base_url, api_key, system_prompt, fpass_prompt, switch_prompt)




# if __name__ == "__main__":
#     app()
