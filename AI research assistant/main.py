from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import tools_condition,ToolNode
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_tavily import TavilySearch


# user_input -> llm -> tools(if needed) -> from tools to llm again(if tools were called) -> reseach report


# llm 
load_dotenv()
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.9,
)

# tools 

# wikipedia
wiki_api_wrapper = WikipediaAPIWrapper(
    top_k_results=2,
    doc_content_chars_max=2000,
    lang='en',
)


wiki_tool = WikipediaQueryRun(api_wrapper=wiki_api_wrapper)

# tavily
tavily_search = TavilySearch(max_results = 2)

tools = [wiki_tool,tavily_search]

llm_with_tools = llm.bind_tools(tools)


# state
class State(TypedDict):
    topic: str
    messages: Annotated[list, add_messages]

# nodes
def assistant(state:State):
    """
    takes the user input and generates a research report uses tools if needed
    """
    system_prompt = SystemMessage(content=(
        "You are a research assistant. Answer the user's question clearly and "
        "use the available Wikipedia and Tavily tools when additional or "
        "current information would help."
    ))
    res = llm_with_tools.invoke([system_prompt, *state["messages"]])
    return {"messages": [res]}


# graph
graph = StateGraph(State)

# add nodes
graph.add_node('assistant',assistant)
graph.add_node('tools',ToolNode(tools))

# add edges
graph.add_edge(START,'assistant')
graph.add_conditional_edges('assistant',tools_condition)
graph.add_edge('tools','assistant')

# compile
agent = graph.compile()

# invoke
topic = "What is the Riemann hypothesis?"
result = agent.invoke({
    "topic": topic,
    "messages": [HumanMessage(content=topic)],
})

final_message = result["messages"][-1]
if isinstance(final_message, AIMessage):
    print(final_message.content)
else:
    print(final_message)












