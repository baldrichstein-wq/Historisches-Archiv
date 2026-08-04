from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class ArchiveItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: str
    year: Optional[int] = None
    item_type: str = "Postkarte"

class ArchiveItem(ArchiveItemBase):
    id: int
    category_id: Optional[int] = None
    category: Optional[Category] = None
    approved: bool = True
    class Config:
        from_attributes = True

class HistoricalEntryBase(BaseModel):
    title: str
    content: str
    event_date: Optional[date] = None

class HistoricalEntry(HistoricalEntryBase):
    id: int
    category_id: Optional[int] = None
    approved: bool = True
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class RecipeBase(BaseModel):
    title: str
    ingredients: Optional[str] = None
    instructions: Optional[str] = None
    history: Optional[str] = None
    year: Optional[int] = None
    country: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None

class RecipeCreate(RecipeBase):
    pass

class RecipeResponse(RecipeBase):
    id: int
    owner_id: Optional[int] = None
    approved: bool = True

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    captcha_answer: int
    captcha_expected: int

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    role: str
    ip_address: Optional[str] = None

    class Config:
        from_attributes = True

class UserRoleUpdate(BaseModel):
    role: str

class SongBase(BaseModel):
    title: str
    author: Optional[str] = None
    origin: Optional[str] = None
    language: Optional[str] = None
    lyrics: Optional[str] = None
    audio_url: Optional[str] = None
    sheet_music_url: Optional[str] = None
    history: Optional[str] = None
    year: Optional[int] = None

class SongCreate(SongBase):
    pass

class Song(SongBase):
    id: int
    category_id: Optional[int] = None
    owner_id: Optional[int] = None
    category: Optional[Category] = None
    owner: Optional[UserResponse] = None
    approved: bool = True
    class Config:
        from_attributes = True

class LinkBase(BaseModel):
    title: str
    url: str
    description: Optional[str] = None

class LinkResponse(LinkBase):
    id: int
    owner_id: Optional[int] = None
    class Config:
        from_attributes = True

class BlockedEmailCreate(BaseModel):
    email: str

class BlockedEmailResponse(BlockedEmailCreate):
    id: int
    class Config:
        from_attributes = True

class BlockedIPCreate(BaseModel):
    ip_address: str

class BlockedIPResponse(BlockedIPCreate):
    id: int
    class Config:
        from_attributes = True

class GuestbookCreate(BaseModel):
    name: str
    email: str
    message: str

class GuestbookResponse(GuestbookCreate):
    id: int
    created_at: str
    approved: bool = True

    class Config:
        from_attributes = True


