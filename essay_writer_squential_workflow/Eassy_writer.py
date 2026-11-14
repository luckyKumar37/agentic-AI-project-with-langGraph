import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph,START,END
from typing import TypedDict

# we are going to make a eassy writing agent which takes topic as input from the user using sequential workflow
# flow 
# topic -> first draft -> revise -> output

#llm 
load_dotenv()
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.9,
)

# state
class State(TypedDict):
    input_topic : str
    first_draft : str
    final_essay : str

# nodes
def first_draft(state : State):
    """ write the initial draft for the essay """

    prompt = f"""
    You are a professional essay writer.

    Write a detailed, well-structured essay on the following topic:

    Topic: {state['input_topic']}

    Requirements:
    - Start with an engaging introduction.
    - Explain the topic clearly and logically.
    - Divide the essay into meaningful sections with headings.
    - Include relevant examples wherever necessary.
    - Maintain a formal but easy-to-understand writing style.
    - End with a strong conclusion.
    - Avoid unnecessary repetition and irrelevant information.

    Generate only the essay. Do not include any additional commentary.
    """

    res = llm.invoke(prompt)

    return {'first_draft': res.content.strip()}

def revise(state : State):
    """ revise the initial draft to correct the initial mistakes and make the essay better """

    prompt = f"""
    You are an experienced essay editor.

    Your task is to review and improve the following essay.

    Original Topic: {state['input_topic']}

    First Draft:
    {state['first_draft']}

    Review the essay based on these criteria:

    1. Accuracy:
       Correct factual inaccuracies and misleading statements.

    2. Clarity:
       Improve sentences that are confusing or difficult to understand.

    3. Structure:
       Ensure ideas flow logically between paragraphs and sections.

    4. Grammar:
       Correct grammatical, spelling, and punctuation mistakes.

    5. Depth:
       Identify areas that need better explanations or relevant examples.

    6. Conciseness:
       Remove unnecessary repetition and irrelevant content.

    Produce a polished final essay while preserving the original topic
    and the main ideas.

    Do not include your review process or editing notes.
    Return only the revised essay.
    """

    res = llm.invoke(prompt)

    return {'final_essay' : res.content.strip()}

# graph
graph = StateGraph(State)

# add nodes
graph.add_node('first_draft',first_draft)
graph.add_node('revise_draft',revise)

# add edges
graph.add_edge(START,'first_draft')
graph.add_edge('first_draft','revise_draft')
graph.add_edge('revise_draft',END)

# compile graph
app = graph.compile()

result = app.invoke({
    'input_topic':'neural network'
})

print(f'Eassy\n{result['final_essay']}')





