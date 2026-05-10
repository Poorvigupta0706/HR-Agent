from pydantic import BaseModel


class OverrideValidationModel(BaseModel):
    is_reasonable: bool = True
    ai_comment: str = ""
