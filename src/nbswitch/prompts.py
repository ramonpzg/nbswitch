SYSTEM_PROMPT = """You are an AI assistant specialized in modifying Jupyter notebooks
and markdown files. Your task is to take an existing educational notebook and change
its use case while \nmaintaining the overall structure and logic of the prose and code.
You always provide clear explanations \nfor any code you rewrite and you have a terse
but casual tone."""

PROMPT_1 = (
    "The following is a jupyter notebook with cells as dictionaries inside a Python list.\n\n"
    "{one}\n\n"
    "Inside the 'source' key is where any code or markdown goes in.\n"
    "Later on, your task will be to change the context of the lesson to the following prompt: {two}\n\n"
    "Right now you need to do the following four things:\n\n"
    "1. Read the entire notebook and reason through it. For example, evaluate the use case, what is good about it and how could it be improved and keep that knowledge to yourself.\n"
    "2. Go back to the beginning and pay attention to the number of each cell, which can be found inside the metadata key as 'index': number_of_the_cell.\n"
    "3. Determine which cells need to change to adapt the lesson to a Finance-related use case in both code and prose.\n"
    "4. Return a Python list with the numbers of ABSOLUTELY NECESSARY cells that need to be changed and nothing else. "
    "For example, if you are not going to change the tile of a section, don't pick it, as we can work on it together later. When in doubt, leave the cell be"
)


PROMPT_2 = (
    "The following is jupyter notebook with cells as dictionaries inside a Python list.\n\n"
    "{one}\n\n"
    "Inside the 'source' key is where any code or markdown goes in.\n"
    "Your task will be to change the context of the lesson to the topic in this prompt: {four}\n\n"
    "You will do this task in the following step-by-step process:\n\n"
    "1. Read the entire notebook and reason through it. For example, evaluate the use case, what is good about it and how could it be improved when changing the use case to a "
    "Finance-related topic of your choosing. You can use synthetic data for the code pieces, and, if you see quotes from authors or articles, feel free to come up with another kind of idea.\n"
    "2. Once you have read through it, your main task is to change and return ONLY THE CELLS with the following cell_type and indexes inside:\n\n{two}.\n\n"
    "Remember, pay attention to whether the cell is a 'markdown' or a 'code' and return the appropriate one. Also, please ONLY update and return the new cells based on those with the following 'cell_tags' and 'indexes' inside the metadata tag:\n\n{three}\n\n"
    "Lastly, be as concise as you possibly can to get the message across. Be terse and to the point but always keep a touch of dry humor in your tone. If you need to summarize the content a bit more to finish the job, do it."
)
