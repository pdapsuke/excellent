from pydantic import BaseModel

class IdTokenPostSchema(BaseModel):
    id_token: str