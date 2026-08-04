from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="guest")
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)

    archive_items = relationship("ArchiveItem", back_populates="owner")
    documents = relationship("Document", back_populates="owner")
    historical_entries = relationship("HistoricalEntry", back_populates="author")
    songs = relationship("Song", back_populates="owner")
    recipes = relationship("Recipe", back_populates="owner")
    links = relationship("Link", back_populates="owner")


class BlockedEmail(Base):
    __tablename__ = "blocked_emails"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)

class BlockedIP(Base):
    __tablename__ = "blocked_ips"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, unique=True, index=True, nullable=False)



class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    archive_items = relationship("ArchiveItem", back_populates="category")
    documents = relationship("Document", back_populates="category")
    historical_entries = relationship("HistoricalEntry", back_populates="category")
    songs = relationship("Song", back_populates="category")
    recipes = relationship("Recipe", back_populates="category")


class ArchiveItem(Base):
    __tablename__ = "archive_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    item_type = Column(String, default="Postkarte")
    approved = Column(Boolean, default=True, nullable=False)
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    category = relationship("Category", back_populates="archive_items")
    owner = relationship("User", back_populates="archive_items")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    file_url = Column(String, nullable=False)
    transcription = Column(Text, nullable=True)
    date = Column(Date, nullable=True)
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    category = relationship("Category", back_populates="documents")
    owner = relationship("User", back_populates="documents")


class HistoricalEntry(Base):
    __tablename__ = "historical_entries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    event_date = Column(Date, nullable=True)
    approved = Column(Boolean, default=True, nullable=False)
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    author_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    category = relationship("Category", back_populates="historical_entries")
    author = relationship("User", back_populates="historical_entries")

class Song(Base):
    __tablename__ = "songs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, nullable=True)
    origin = Column(String, nullable=True)
    language = Column(String, nullable=True)
    lyrics = Column(Text, nullable=True)
    history = Column(Text, nullable=True)
    audio_url = Column(String, nullable=True)
    sheet_music_url = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    approved = Column(Boolean, default=True, nullable=False)
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    
    category = relationship("Category", back_populates="songs")
    owner = relationship("User", back_populates="songs")

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    ingredients = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    history = Column(Text, nullable=True)
    year = Column(Integer, nullable=True)
    country = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    approved = Column(Boolean, default=True, nullable=False)
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    
    category = relationship("Category", back_populates="recipes")
    owner = relationship("User", back_populates="recipes")

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    url = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    owner = relationship("User", back_populates="links")

class GuestbookEntry(Base):
    __tablename__ = "guestbook_entries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, default="")
    message = Column(Text, nullable=False)
    created_at = Column(String, nullable=False)
    approved = Column(Boolean, default=True, nullable=False)


