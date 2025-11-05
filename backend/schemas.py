from pydantic import BaseModel, Field


class TextModel(BaseModel):
    text: str


class AIAgentRequestModel(TextModel):
    pass


class AIAgentResponseModel(TextModel):
    is_success: bool = Field(default=True)
