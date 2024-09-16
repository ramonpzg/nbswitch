SYSTEM_PROMPT = """You are an AI assistant specializing in modifying, enhancing, translating, 
and reorganizing Jupyter notebooks and markdown files with educational content in them. 
Your task is to take an existing educational notebook and make a better version of it 
while maintaining the overall structure and logic of the prose and code. You always provide 
clear explanations for any code you rewrite and you have a terse but casual tone."""

PROMPT_1 = (
    "The following is a jupyter notebook with cells as dictionaries objects inside a Python list.\n\n"
    "{notebook}\n\n"
    "Inside the 'source' key is where any code or markdown goes in.\n"
    "Later on, your task will be to change the context of the lesson to the following prompt (or a different use case \n"
    "of your choosing if the user does not provide one): {prompt}\n\n"
    "Right now you need to do the following four things:\n\n"
    "1. Read the entire notebook and reason through it. For example, evaluate the context, what is good about it and how could it be improved and keep that knowledge to yourself.\n"
    "2. Go back to the beginning and pay attention to the number of each cell, which can be found inside the metadata key as 'index': number_of_the_cell.\n"
    "3. Determine which cells need to change to adapt the lesson to a Finance-related use case in both code and prose.\n"
    "4. Return a Python list with the numbers of ABSOLUTELY NECESSARY cells that need to be changed and nothing else. "
    "For example, sections titled Overview or Dependencies can stay the same."
)


PROMPT_2 = (
    "The following is a jupyter notebook with cells as dictionaries objects inside a Python list.\n\n"
    "{notebook}\n\n"
    "Inside the 'source' key is where any code or markdown goes in.\n"
    "Your task will be to change the context of the lesson to the topic in the following prompt (or a different use case \n"
    "of your choosing if the user does not provide one): {prompt}\n\n"
    "You will do this task in the following step-by-step process:\n\n"
    "1. Read the entire notebook and reason through it. For example, evaluate the context, what is good about it and "
    "how could it be improved when changing the use case described by the user. You can use "
    "synthetic data for the code pieces, and, if you see quotes from authors or articles, feel free to come up with another kind of idea.\n"
    "2. Once you have read through it, your main task is to change and return ONLY THE CELLS with the following indexes inside the metadata key:\n\n{index}.\n\n"
    "Remember, pay attention to whether the cell is a 'markdown' or a 'code' and return the appropriate one. Also, please ONLY update and return the new cells "
    "based on those with the following 'cell_tags' and 'indexes' inside the metadata tag:\n\n{index}\n\n"
    "Lastly, be as concise as you possibly can to get the message across. Be terse and to the point but always keep a touch of dry humor in your tone. If "
    "you need to summarize the content a bit more to finish the job, do it. "
    "Note that, if the notebook is to large, you will be helping the user iteratively so you might see "
    "below the cells that have a already been updated to the new use-case.\n\n {newer_cells}"
)

PROMPT_3 = (
    "The following is a jupyter notebook with cells as dictionaries objects inside a Python list.\n\n"
    "{notebook}\n\n"
    "Inside the 'source' key is where any code or markdown goes in.\n"
    "Your task will be to translate the content of the lesson to the following language: {language}\n\n"
    "You will do this task in the following step-by-step process:\n"
    "1. Read the entire notebook and reason through it. For example, evaluate the context, what is good "
    "about it and how could it be improved when translating it to the language specified by the user.\n"
    "2. If you see quotes from authors or articles, translate them as normal and keep the name of the author intact.\n"
    "3. Once you have read through it, your main task is to TRANSLATE and RETURN ONLY THE MARKDOWN CELLS with the following "
    "cells:\n\n{index}\n\n"
    "Remember, pay attention to whether the cell is a 'markdown' or a 'code' and return the appropriate one. "
    "Lastly, be as concise as you possibly can to get the message across. Be terse and to the point, and "
    "keep a touch of dry humor in your tone. If you can't remember how to translate a word to the language specified "
    "by the user, stop and think of a similar one that would provide the same kind of information."
)


PROMPT_4 = "Hi"

PROMPT_5 = "Mom!"