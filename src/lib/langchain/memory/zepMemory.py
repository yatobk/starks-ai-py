from langchain_community.chat_message_histories import ZepChatMessageHistory
from langchain.memory import ConversationBufferMemory
import os

def zepMemory(memoryKey: str):
    zep_chat_history = ZepChatMessageHistory(
        session_id=memoryKey,
        url=os.getenv("ZEP_BASE_URL"), 
        api_key= os.getenv("ZEP_API_KEY")
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history", chat_memory=zep_chat_history, return_messages=True 
    )
    
    return memory