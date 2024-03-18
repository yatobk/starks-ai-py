from dotenv import load_dotenv
from openai import OpenAI
load_dotenv() 

def describe_image(base64_img):
    client = OpenAI()
    description = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "O que tem nessa imagem?"},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_img}",
                    },
                ]
            }
        ],
        max_tokens= 150,
        temperature= 0.2,
        frequency_penalty=2.0,
        presence_penalty=2.0
    )

    return { 
            "responseText": description.choices[0].message.content, 
            "totalTokens": description.usage.total_tokens
        }
