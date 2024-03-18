from pydantic import BaseModel, Field, ValidationError
import os

class EnvConfig(BaseModel):
    OPENAI_API_KEY: str = Field(min_lenght=1)
    ZEP_BASE_URL: str = Field(min_lenght=1)
    ZEP_API_KEY: str = Field(min_lenght=1)

try:
    env = EnvConfig(
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
        ZEP_BASE_URL=os.getenv("ZEP_BASE_URL"),
        ZEP_API_KEY=os.getenv("ZEP_API_KEY")
    )

except KeyError as e:
    print(f"Variável de ambiente faltando: {e}")
except ValidationError as e:
    print(f"Erro de validação das variáveis de ambiente: {e}")
