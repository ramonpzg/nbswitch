from count_tokens.count import count_tokens_in_string
from litellm import completion
from openai import OpenAI
from instructor import Instructor
import instructor
import os
# from models import ProviderDetails, ListOfCells
from pydantic import Field, validate_call
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
from .models import ListOfCells, FullNotebook
from .prompts import *
import math

class NbSwitch:

    @validate_call(config=dict(arbitrary_types_allowed=True))
    def __init__(
        self,
        in_file: Path | str,
        prompt: str,
        mode: str = "switch",
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
    ) -> None:
        self.in_file          = in_file
        self.prompt           = prompt
        self.mode             = mode
        self.provider         = provider
        self.model            = model
        self.api_key          = api_key
        self.output_file      = output_file
        self.base_url         = base_url
        self.system_prompt    = system_prompt
        self.fpass_prompt     = fpass_prompt
        self.switch_prompt    = switch_prompt
        self.translate_prompt = translate_prompt
        self.flip_prompt      = flip_prompt
        self.enhance_prompt   = enhance_prompt
        self.max_tokens       = max_tokens
        self.max_retries      = max_retries

    def create_client(
        self,
    ) -> Instructor:
        if self.provider == "OpenAI":
            self.client = instructor.from_openai(
                OpenAI(), api_key=self.api_key if self.api_key else os.getenv("OPENAI_API_KEY"),
            )
        
        elif self.provider == "Cohere":
            self.client = instructor.from_cohere(
                Client(), api_key=self.api_key if self.api_key else os.getenv("COHERE_API_KEY"),
            )
            
        elif self.provider == "Groq":
            self.client = instructor.from_openai(
                Groq(api_key=self.api_key if self.api_key else os.getenv("GROQ_API_KEY"))
            )
            
        elif self.provider == "Ollama":
            self.client = instructor.from_openai(
                OpenAI(
                    base_url=base_url if base_url else "http://localhost:11434/v1",
                    api_key="ollama",
                )
            )
            
        elif self.provider == "Anthropic":
            self.client = instructor.from_anthropic(
                Anthropic(api_key=self.api_key if self.api_key else os.getenv("ANTHROPIC_API_KEY")),
            )
            
        else:
            raise ValueError(
                f'Sorry, the name {self.provider} is not a package. Please use one of the following names:'
                "Anthropic, OpenAI, Ollama, Cohere, HuggingFace, Groq, LlamaCPP"
            )
        
        return self.client

    def read_doc(self, doc: Path | str = None) -> tuple[NotebookNode, int]:
        if doc:
            self.in_file = doc
        with open(self.in_file, 'r') as f:
            self.notebook = nbformat.read(f, as_version=4)
            self.num_of_cells = len(self.notebook.cells)
        return self.notebook, self.num_of_cells   
    
    def enumerate_document(self):
        for i, cell in enumerate(self.notebook.cells):
            cell["metadata"] = {"index": i}
        return self.notebook

    def first_pass(self) -> ListOfCells:
        if self.client.provider.name == "ANTHROPIC":
            self.cells_to_change = self.anthropic_call(base_prompt=self.fpass_prompt, response_model=ListOfCells)
        else:
            self.cells_to_change = self.openai_call(base_prompt=self.fpass_prompt, response_model=ListOfCells)
        return self.cells_to_change

    def cells_token_counter(self):
        if not hasattr(self, 'cells_to_change'):
            raise RuntimeError("Please run 'first_pass' before running 'second_pass'")
        self.cells_needed = []
        for i in self.notebook.cells:
            for num in self.cells_to_change.cells_of_interest:
                if i['metadata']['index'] == num:
                    self.cells_needed.append(i)
        self.cells_token_count = token_counter(text=str(self.cells_needed))
        
        if self.cells_token_count < 3_800:
            self.passes = 1
        elif self.cells_token_count >= 3_800 and self.cells_token_count < 6_500:
            self.passes = 2
        elif self.cells_token_count >= 6_500 and self.cells_token_count < 9_500:
            self.passes = 3
        elif self.cells_token_count >= 9_500 and self.cells_token_count < 13_000:
            self.passes = 4
        else:
            answer = input (f"Your notebook is quite large with roughly {count} tokens that need to be changed, are you sure you want to continue? (y/n) ")
            if answer == 'y':
                self.passes = 5
            elif answer == 'n':
                exit()
            else:
                ValueError(f"You answered {answer}, please select one of the following options: 'y' for 'yes' or 'n' for 'no'")
                cells_token_counter()



    def second_pass(self) -> FullNotebook:
        if not hasattr(self, 'cells_to_change'):
            raise RuntimeError("Please run 'first_pass' before running 'second_pass'")
        
        if self.passes > 1:
            self.new_cells = FullNotebook(all_cells=[])
            split_of_cells = math.ceil(len(self.cells_to_change.cells_of_interest) / self.passes)
            for i in range(self.passes):
                api_call = self.anthropic_call(
                    base_prompt=self.switch_prompt, 
                    response_model=FullNotebook, 
                    index=self.cells_to_change.cells_of_interest[i*split_of_cells:(i+1)*split_of_cells],
                    newer_cells=self.new_cells.all_cells
                ).all_cells if self.client.provider.name == "ANTHROPIC" else self.openai_call(
                    base_prompt=self.switch_prompt, 
                    response_model=FullNotebook, 
                    index=self.cells_to_change.cells_of_interest[i*split_of_cells:(i+1)*split_of_cells],
                    newer_cells=self.new_cells.all_cells
                ).all_cells
                self.new_cells.all_cells.extend(api_call)
        else:
            try:
                if self.client.provider.name == "ANTHROPIC":
                    self.new_cells = self.anthropic_call(base_prompt=self.switch_prompt, response_model=FullNotebook, index=self.cells_to_change.cells_of_interest)
                else:
                    self.new_cells = self.openai_call(base_prompt=self.switch_prompt, response_model=FullNotebook, index=self.cells_to_change.cells_of_interest)
            except:
                self.passes = 2
                self.second_pass()
        return self.new_cells, self.passes

    def merge_nbs(self):
        for i in self.new_cells.all_cells:
            index = i.metadata['index']
            self.notebook.cells[index]['source'] = i.source
        return self.notebook

    def save_doc(self):
        if self.output_file:
            self.new_notebook_path = os.path.join(os.path.dirname(__file__), f"{self.output_file}.ipynb")
        else:
            fake = Faker()
            self.new_notebook_path = os.path.join(os.path.dirname(__file__), f"{'_'.join(fake.bs().split())}.ipynb")
        with open(self.new_notebook_path, 'w') as f:
            nbformat.write(self.notebook, f)


    def anthropic_call(
        self,
        base_prompt,
        response_model,
        newer_cells=None,
        **kwargs
    ):
        return self.client.chat.completions.create(
            model=self.model,
            system=self.system_prompt,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": base_prompt.format(notebook=self.notebook.cells, prompt=self.prompt, newer_cells=newer_cells, **kwargs)}],
            max_retries=self.max_retries,
            response_model=response_model
        )
    
    def openai_call(
        self,
        base_prompt,
        response_model,
        **kwargs
    ):
        return self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": self.system_prompt}, 
                {"role": "user", "content": base_prompt.format(notebook=self.notebook.cells, prompt=self.prompt, **kwargs)}
            ],
            max_retries=self.max_retries,
            response_model=response_model
        )

    # def run_switch(self):
    #     self.create_client()

    #     self.first_pass()
    #     self.first_pass()
    #     self.merge_nbs()


    # def run_switch(self):
    #     self.create_client()

    #     self.first_pass()
    #     self.cells_token_counter()
    #     self.second_pass()
    #     self.merge_nbs()



    # def calculate_approximate_cost(self):
    #     pass

    # @validate_call(config=dict(arbitrary_types_allowed=True))
    # def get_markdown(
    #     notebook: NotebookNode
    # ) -> list[dict]:
    #     list_of_md_cells = []
    #     for nbcell in notebook.cells:
    #         if nbcell['cell_type'] == "markdown":
    #             list_of_md_cells.append(nbcell)
    #     return list_of_md_cells


    # @validate_call(config=dict(arbitrary_types_allo wed=True))
    # def translate_doc(
    #     client: Instructor,
    #     model: str,
    #     language: str,
    #     notebook: NotebookNode,
    #     cells_to_change,
    #     system_prompt: str = SYSTEM_PROMPT,
    #     base_prompt: str = PROMPT_3,
    #     # output_model: FullNotebook,
    #     max_tokens: int = Field(4_096, ge=20),
    #     max_retries: int = Field(default=3, le=10, ge=0),
    # ) -> FullNotebook:222
    #     if client.provider.name == "ANTHROPIC":
    #         return client.chat.completions.create(
    #             model=model,
    #             system=system_prompt,
    #             max_tokens=max_tokens,
    #             messages=[{
    #                 "role": "user", 
    #                 "content": base_prompt.format(
    #                     notebook=notebook.cells, language=language, index=cells_to_change 
    #                 )
    #             }],
    #             max_retries=max_retries,
    #             response_model=FullNotebook
    #         )
    #     else:
    #         return client.chat.completions.create(
    #             model=model,
    #             max_tokens=max_tokens,
    #             messages=[
    #                 {"role": "system", "content": system_prompt}, 
    #                 {
    #                     "role": "user", 
    #                     "content": base_prompt.format(
    #                         notebook=notebook.cells, language=language, index=cells_to_change 
    #                     )
    #                 }
    #             ],
    #             max_retries=max_retries,
    #             response_model=FullNotebook
    #         )


    # def notebook_to_html(notebook):
    #     html_exporter = HTMLExporter()
    #     html_exporter.template_name = 'basic'
    #     (body, _) = html_exporter.from_notebook_node(notebook)

    #     soup = BeautifulSoup(body, 'html.parser')
    #     for cell in soup.find_all('div', class_='cell'):
    #         cell['class'] = cell.get('class', []) + ['notebook-cell']

    #     return str(soup)






        # if ".ipynb" in doc:

        # content = doc.read()
        # # content = await doc.read()
        # return nbformat.reads(content.decode(), as_version=4)



    # def split_nb(doc):
    #     count = token_counter(text=str(doc.cells))
    #     if count > 2_000 and count < 3_500:
    #         return 2
    #     elif count >= 3_500 and count < 5_500:
    #         return 3
    #     elif count >= 5_500 and count < 7_500:
    #         return 4
    #     elif count >= 7_500 and count < 10_000:
    #         return 5
    #     else:
    #         answer = input (f"Your notebook is quite large with roughly {count} tokens, are you sure you want to continue? (y/n) ")
    #         if answer == 'y':
    #             return 8
    #         elif answer == 'n':
    #             exit()
    #         else:
    #             ValueError(f"You answered {answer}, please select one of the following options: 'y' for 'yes' or 'n' for 'no'")
    #             split_nb()


    # def count_all_tokens(
        
    # ):
    #     pass

    # def this():
    #     pass

    # def while_waiting():
    #     answer = input("Want to hear a joke while you wait 😌: (yes/no)")
    #     if answer == 'yes':
