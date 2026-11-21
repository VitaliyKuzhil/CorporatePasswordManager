from pydantic import BaseModel

class UserResponse(BaseModel):
    user_id: int
    full_name: str | None = None
    login: str | None = None
    avatar_url: str | None = None
    role: str | None = None
    status: str | None = None

    class Config:
        from_attributes = True


class GrantAccessRequest(BaseModel):
    user_id: int
