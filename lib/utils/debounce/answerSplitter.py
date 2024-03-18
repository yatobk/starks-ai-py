def answer_messages(messages): 
    responses = [{"message": message} for message in messages]
    return responses

def split_text(text): 
    toSplit = f"""{text}"""
    messages = toSplit.split('\n\n')
    messages = [message.strip() for message in messages if message.strip()]

    return answer_messages(messages)
