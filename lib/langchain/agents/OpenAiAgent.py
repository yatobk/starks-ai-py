from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI
#from langchain.chains import LLMMathChain
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from lib.utils.ai.model import llm_model_name
from lib.langchain.memory.zepMemory import zepMemory
from lib.langchain.tools.passwordGenerator import PasswordGenerator
from lib.langchain.prompts import animePrompt
from lib.utils.debounce.answerSplitter import split_text
    
def createAgent(userInput: str, memoryKey: str):
    llm = ChatOpenAI(
        model=llm_model_name,
        max_tokens=300,
        temperature=0.8,
        tiktoken_model_name="cl100k_base",
        tags=["test1@nutri", "test2@nutri"]
    )

    #llm_math = LLMMathChain(llm=llm)
    """
    tools = [
        Tool(
        name="math",
        func=llm_math.run,
        description="Useful when you need to do maths"
    )]
    """

    #tools.append(test_tools)

    tools = [PasswordGenerator()]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", animePrompt.anime),
            MessagesPlaceholder("chat_history", optional=False),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ]
    )
    
    openaiAgent = create_openai_functions_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=openaiAgent, tools=tools, memory=zepMemory(memoryKey), verbose=False)

    response = agent_executor.invoke(
        {
            "input": userInput,
            "chat_history": [],
        }
    )    
    return response

def answer(userInput: str, memoryKey: str):
    ai_answer = createAgent(userInput, memoryKey)['output']
    return split_text(ai_answer)

# DEBUG ONLY
def main():
    with get_openai_callback() as cb:
        while True:
            userInput = input(">>> ")
            if userInput == "q":
                print("bye")
                break
            else: 
                res = createAgent(userInput=userInput, memoryKey="hello38202389829")
                print(res['output'])
                
                #print(cb)
        exit(1)

if __name__ == "__main__":
    print(main())
    """
    calculator = TokenCostCalculator()
    input_cost = calculator.input_cost(1000)
    output_cost = calculator.output_cost(1000)
    print("Custo de entrada:", input_cost)
    print("Custo de saída:", output_cost)
    """