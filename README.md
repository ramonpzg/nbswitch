# NbSwitch

> NbSwitch let's you bring a notebook with educational content, describe a new use case, and change the original one to that using Claude Sonnet 3.5!

![alt text](images/image.png)

There are thousands of incredible educational notebooks out there that could be shown some love, so, what if that meant that, in the 
case of data-related topics, we could change the use case of any given notebook to a completely new one? That's what NbSwitch is for. :sunglasses:

As of now, the app works in the following way:
1. Select your notebook and write a prompt (there is no order for this at the moment). Press the wide green button.
2. Claude will go through the notebook and, based on a template prompt and your written one, it will evaluate which cells need to change and which don't and 
then return a list with the index of each of the cells that will need to be changed.
1. The second pass through Claude includes:
   1. A slightly different prompt template
   2. your prompt again
   3. the list of cells that need to be changed
2. Then the endpoint returns HTML back to the front-end with both the new and the original notebook
3. Scroll down for a button to download your `.ipynb` file.

The app can be found [live here](https://nbswitch.fly.dev/). 

**Limitations**
- Make sure your notebook has not been run before you upload it.
- Don't add overly long notebooks, e.g., those requiring more than `max_tokens=4_096`.
- Didn't test it on mobile (this might be more useful for markdown files for the obsidian lovers (myself included :smiley: ))

![alt text](images/image-1.png)

This project was created as part of Anthropic's June 2024 Hackathon and it was build using their Claude Sonnet 3.5 model.

While I made this app to participate in the Hackathon, I see a lot of value in this project and will continue to polish and host it for free 
for as long as I can. The code will remain open-source as well. :)

**Note:** The code in this repo is fresh out of the oven, meaning, its ugliness might offend people, its lack of tests might give 
some a cardiac arrest, and its lack of React or something similar in the front-end might... (I'll leave that last one to you).


## Set Up

Create an environment.

```sh
python -m venv venv
```
or

```sh
mamba create -n hackathon python=3.11
```

Activate your environment.

```sh
source venv/bin/activate
```

or 

```sh
mamba activate hackathon
```

Install the dependencies.

```sh
pip install -r requirements.txt
```

Run the app.

```sh
uvicorn main:app --reload
```


## Tech Stack

- `anthropic` - SDK to interact with Anthropic's suite of models.
- `instructor` - tool for enforcing structured output from LLMs using pydantic.
- `pydantic` - typescript for Python.
- `fastapi` - for processing and serving requests.
- `nbconvert` - to change notebooks from one format to another.
- `nbformat` - to manipulate the JSON structure of a notebook.
- `AlpineJS` - interactions in the front-end.
- `Pines UI` - Tailwind CSS and AlpineJS components.
- `HTMX` - for sending the request to the back-end.


## Roadmap

- [ ] (Important!) Optimize the process for generating the new notebooks, right now, it is relatively expensive to change one.
- [ ] (Important!) Add an error message in case the user does not add a notebook and only a prompt.
- [ ] Provide a way for users to input their own API key.
- [ ] Limit the usage (maybe to 10 notebooks per person and per month as I am paying for it)
- [ ] Add support for markdown files
- [ ] Add support for marimo files
- [ ] Add example notebooks
- [ ] Add more example prompts
- [ ] Add interactivity where, for example, the user could select a part of the notebook they didn't like and ask Claude to change it.
- [ ] Allow users to bring in notebooks with outputs