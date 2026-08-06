from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, Base, engine, SessionLocal
import models
import schemas
from auth import verify_password, get_password_hash, create_access_token, get_current_user, get_current_user_optional, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta, date, datetime
from typing import Optional
import shutil
import json
import os
import uuid
from pydantic import BaseModel
from email_service import send_verification_email, send_admin_notification

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
# Create the tables in the database (for development purposes)
Base.metadata.create_all(bind=engine)
try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE users ADD COLUMN ip_address VARCHAR"))
        conn.commit()
except Exception:
    pass

app = FastAPI(title="Historisches Archiv API")

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Add CORS middleware to allow the React frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def block_ip_middleware(request: Request, call_next):
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.client.host if request.client else None

    if client_ip:
        db = SessionLocal()
        try:
            blocked = db.query(models.BlockedIP).filter(models.BlockedIP.ip_address == client_ip).first()
            if blocked:
                return JSONResponse(status_code=403, content={"detail": "Access Denied. Your IP is blocked."})
        finally:
            db.close()
            
    response = await call_next(request)
    return response

def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "Unbekannt"

@app.post("/api/login", response_model=schemas.Token)
def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bitte bestätige zuerst deine E-Mail-Adresse."
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    client_ip = get_client_ip(request)
    if user.ip_address != client_ip:
        user.ip_address = client_ip
        db.commit()
    return {"access_token": access_token, "token_type": "bearer"}

def check_role(required_roles: list[str]):
    def role_checker(current_user: models.User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker

@app.post("/api/register", response_model=schemas.UserResponse)
def register_user(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.captcha_answer != user.captcha_expected:
        raise HTTPException(status_code=400, detail="CAPTCHA inkorrekt")

    blocked = db.query(models.BlockedEmail).filter(models.BlockedEmail.email == user.email).first()
    if blocked:
        raise HTTPException(status_code=400, detail="Diese E-Mail-Adresse ist blockiert.")

    db_user = db.query(models.User).filter((models.User.username == user.username) | (models.User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    hashed_password = get_password_hash(user.password)
    verification_token = str(uuid.uuid4())
    client_ip = get_client_ip(request)
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
        role="guest",
        is_verified=False,
        verification_token=verification_token,
        ip_address=client_ip
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Send emails
    send_verification_email(new_user.email, verification_token)
    send_admin_notification(new_user.email, new_user.username)
    
    return new_user

class VerifyRequest(BaseModel):
    token: str

@app.post("/api/verify")
def verify_email(req: VerifyRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.verification_token == req.token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Ungültiger oder abgelaufener Token.")
    
    user.is_verified = True
    user.verification_token = None
    db.commit()
    return {"message": "E-Mail erfolgreich bestätigt."}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Historisches Archiv API"}

@app.post("/api/upload")
def upload_image(file: UploadFile = File(...), current_user: models.User = Depends(check_role(["admin", "moderator", "user"]))):
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_location = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"url": f"/archiv/uploads/{unique_filename}"}

@app.get("/api/users/me", response_model=schemas.UserResponse)
def get_users_me(request: Request, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    client_ip = get_client_ip(request)
    if current_user.ip_address != client_ip:
        current_user.ip_address = client_ip
        db.commit()
        db.refresh(current_user)
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "role": current_user.role,
        "ip_address": current_user.ip_address if current_user.role in ["admin", "moderator"] else None
    }

@app.get("/api/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator"]))):
    return db.query(models.User).all()

@app.put("/api/users/{user_id}/role", response_model=schemas.UserResponse)
def update_user_role(user_id: int, role_update: schemas.UserRoleUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator"]))):
    if role_update.role not in ["admin", "moderator", "user", "guest"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if current_user.role == "moderator":
        if role_update.role in ["admin", "moderator"]:
            raise HTTPException(status_code=403, detail="Moderatoren dürfen keine Admin- oder Moderator-Rollen vergeben.")
        if db_user.role in ["admin", "moderator"]:
            raise HTTPException(status_code=403, detail="Moderatoren dürfen die Rolle von Admins oder Moderatoren nicht ändern.")
            
    db_user.role = role_update.role
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.role == "admin" and db_user.username == "David":
        raise HTTPException(status_code=400, detail="Haupt-Admin kann nicht gelöscht werden.")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.get("/api/blocked-emails", response_model=list[schemas.BlockedEmailResponse])
def get_blocked_emails(db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    return db.query(models.BlockedEmail).all()

@app.post("/api/blocked-emails", response_model=schemas.BlockedEmailResponse)
def block_email(blocked_email: schemas.BlockedEmailCreate, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    db_blocked = db.query(models.BlockedEmail).filter(models.BlockedEmail.email == blocked_email.email).first()
    if db_blocked:
        raise HTTPException(status_code=400, detail="E-Mail ist bereits blockiert")
    new_blocked = models.BlockedEmail(email=blocked_email.email)
    db.add(new_blocked)
    db.commit()
    db.refresh(new_blocked)
    return new_blocked

@app.delete("/api/blocked-emails/{id}")
def unblock_email(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    db_blocked = db.query(models.BlockedEmail).filter(models.BlockedEmail.id == id).first()
    if not db_blocked:
        raise HTTPException(status_code=404, detail="Blockierte E-Mail nicht gefunden")
    db.delete(db_blocked)
    db.commit()
    return {"message": "Blockierung aufgehoben"}

@app.get("/api/blocked-ips", response_model=list[schemas.BlockedIPResponse])
def get_blocked_ips(db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    return db.query(models.BlockedIP).all()

@app.post("/api/blocked-ips", response_model=schemas.BlockedIPResponse)
def block_ip(blocked_ip: schemas.BlockedIPCreate, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    db_blocked = db.query(models.BlockedIP).filter(models.BlockedIP.ip_address == blocked_ip.ip_address).first()
    if db_blocked:
        raise HTTPException(status_code=400, detail="IP ist bereits blockiert")
    new_blocked = models.BlockedIP(ip_address=blocked_ip.ip_address)
    db.add(new_blocked)
    db.commit()
    db.refresh(new_blocked)
    return new_blocked

@app.delete("/api/blocked-ips/{id}")
def unblock_ip(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    db_blocked = db.query(models.BlockedIP).filter(models.BlockedIP.id == id).first()
    if not db_blocked:
        raise HTTPException(status_code=404, detail="Blockierte IP nicht gefunden")
    db.delete(db_blocked)
    db.commit()
    return {"message": "IP-Blockierung aufgehoben"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}

@app.get("/api/archive", response_model=list[schemas.ArchiveItem])
def get_archive(db: Session = Depends(get_db)):
    return db.query(models.ArchiveItem).filter(models.ArchiveItem.approved == True).all()

@app.get("/api/archive/{item_id}", response_model=schemas.ArchiveItem)
def get_archive_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.ArchiveItem).filter(models.ArchiveItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.post("/api/archive", response_model=schemas.ArchiveItem)
def create_archive_item(item: schemas.ArchiveItemBase, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator", "user"]))):
    cat = db.query(models.Category).filter(models.Category.name == "Postkarten").first()
    is_approved = current_user.role in ["admin", "moderator"]
    db_item = models.ArchiveItem(**item.model_dump(), category_id=cat.id if cat else None, owner_id=current_user.id, approved=is_approved)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/api/archive/{item_id}", response_model=schemas.ArchiveItem)
def update_archive_item(item_id: int, item: schemas.ArchiveItemBase, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator"]))):
    db_item = db.query(models.ArchiveItem).filter(models.ArchiveItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/api/archive/{item_id}")
def delete_archive_item(item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    db_item = db.query(models.ArchiveItem).filter(models.ArchiveItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}

@app.get("/api/timeline", response_model=list[schemas.HistoricalEntry])
def get_timeline(db: Session = Depends(get_db)):
    return db.query(models.HistoricalEntry).filter(
        models.HistoricalEntry.approved == True,
        models.HistoricalEntry.event_date >= date(1800, 1, 1),
        models.HistoricalEntry.event_date <= date(1925, 12, 31)
    ).order_by(models.HistoricalEntry.event_date).all()

@app.get("/api/timeline/{entry_id}", response_model=schemas.HistoricalEntry)
def get_timeline_entry(entry_id: int, db: Session = Depends(get_db)):
    db_entry = db.query(models.HistoricalEntry).filter(models.HistoricalEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return db_entry

@app.post("/api/timeline", response_model=schemas.HistoricalEntry)
def create_timeline_entry(entry: schemas.HistoricalEntryBase, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator", "user"]))):
    if entry.event_date < date(1800, 1, 1) or entry.event_date > date(1925, 12, 31):
        raise HTTPException(status_code=400, detail="Das Datum muss zwischen 1800 und 1925 liegen.")
    cat = db.query(models.Category).filter(models.Category.name == "Ereignisse").first()
    is_approved = current_user.role in ["admin", "moderator"]
    db_entry = models.HistoricalEntry(**entry.model_dump(), category_id=cat.id if cat else None, author_id=current_user.id, approved=is_approved)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@app.put("/api/timeline/{entry_id}", response_model=schemas.HistoricalEntry)
def update_timeline_entry(entry_id: int, entry: schemas.HistoricalEntryBase, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator"]))):
    if entry.event_date < date(1800, 1, 1) or entry.event_date > date(1925, 12, 31):
        raise HTTPException(status_code=400, detail="Das Datum muss zwischen 1800 und 1925 liegen.")
    db_entry = db.query(models.HistoricalEntry).filter(models.HistoricalEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    for key, value in entry.model_dump().items():
        setattr(db_entry, key, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@app.delete("/api/timeline/{entry_id}")
def delete_timeline_entry(entry_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    db_entry = db.query(models.HistoricalEntry).filter(models.HistoricalEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(db_entry)
    db.commit()
    return {"message": "Entry deleted successfully"}

@app.get("/api/songs", response_model=list[schemas.Song])
def get_songs(db: Session = Depends(get_db)):
    return db.query(models.Song).filter(models.Song.approved == True).all()

@app.get("/api/songs/{song_id}", response_model=schemas.Song)
def get_song(song_id: int, db: Session = Depends(get_db)):
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if not db_song:
        raise HTTPException(status_code=404, detail="Song not found")
    return db_song

@app.post("/api/songs", response_model=schemas.Song)
def create_song(song: schemas.SongBase, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator", "user"]))):
    cat = db.query(models.Category).filter(models.Category.name == "Lieder").first()
    is_approved = current_user.role in ["admin", "moderator"]
    db_song = models.Song(**song.model_dump(), category_id=cat.id if cat else None, owner_id=current_user.id, approved=is_approved)
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

@app.put("/api/songs/{song_id}", response_model=schemas.Song)
def update_song(song_id: int, song: schemas.SongBase, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator"]))):
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if not db_song:
        raise HTTPException(status_code=404, detail="Song not found")
    for key, value in song.model_dump().items():
        setattr(db_song, key, value)
    db.commit()
    db.refresh(db_song)
    return db_song

@app.delete("/api/songs/{song_id}")
def delete_song(song_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if not db_song:
        raise HTTPException(status_code=404, detail="Song not found")
    db.delete(db_song)
    db.commit()
    return {"message": "Song deleted successfully"}

@app.get("/api/recipes", response_model=list[schemas.RecipeResponse])
def get_recipes(db: Session = Depends(get_db)):
    return db.query(models.Recipe).filter(models.Recipe.approved == True).all()

@app.get("/api/recipes/{recipe_id}", response_model=schemas.RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe

@app.post("/api/recipes", response_model=schemas.RecipeResponse)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator", "user"]))):
    cat = db.query(models.Category).filter(models.Category.name == "Rezepte").first()
    is_approved = current_user.role in ["admin", "moderator"]
    db_recipe = models.Recipe(**recipe.dict(), category_id=cat.id if cat else None, owner_id=current_user.id, approved=is_approved)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.put("/api/recipes/{recipe_id}", response_model=schemas.RecipeResponse)
def update_recipe(recipe_id: int, recipe: schemas.RecipeCreate, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator"]))):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    for key, value in recipe.dict().items():
        setattr(db_recipe, key, value)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.delete("/api/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(db_recipe)
    db.commit()
    return {"message": "Recipe deleted successfully"}
@app.get("/api/links", response_model=list[schemas.LinkResponse])
def get_links(db: Session = Depends(get_db)):
    return db.query(models.Link).all()

@app.get("/api/links/{link_id}", response_model=schemas.LinkResponse)
def get_link(link_id: int, db: Session = Depends(get_db)):
    db_link = db.query(models.Link).filter(models.Link.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    return db_link

@app.post("/api/links", response_model=schemas.LinkResponse)
def create_link(link: schemas.LinkBase, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    db_link = models.Link(**link.dict(), owner_id=current_user.id)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

@app.put("/api/links/{link_id}", response_model=schemas.LinkResponse)
def update_link(link_id: int, link: schemas.LinkBase, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    db_link = db.query(models.Link).filter(models.Link.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    for key, value in link.dict().items():
        setattr(db_link, key, value)
    db.commit()
    db.refresh(db_link)
    return db_link

@app.delete("/api/links/{link_id}")
def delete_link(link_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin"]))):
    db_link = db.query(models.Link).filter(models.Link.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    db.delete(db_link)
    db.commit()
    return {"message": "Link deleted successfully"}

@app.get("/api/guestbook", response_model=list[schemas.GuestbookResponse])
def get_guestbook_entries(db: Session = Depends(get_db)):
    return db.query(models.GuestbookEntry).filter(models.GuestbookEntry.approved == True).order_by(models.GuestbookEntry.id.desc()).all()

@app.post("/api/guestbook", response_model=schemas.GuestbookResponse)
def create_guestbook_entry(entry: schemas.GuestbookCreate, db: Session = Depends(get_db), current_user: Optional[models.User] = Depends(get_current_user_optional)):
    if not entry.name or not entry.name.strip() or not entry.email or not entry.email.strip() or not entry.message or not entry.message.strip():
        raise HTTPException(status_code=400, detail="Fehler: Bitte füllen Sie alle Felder (Name, E-Mail-Adresse und Nachricht) vollständig aus.")
    if "@" not in entry.email or "." not in entry.email:
        raise HTTPException(status_code=400, detail="Fehler: Bitte geben Sie eine gültige E-Mail-Adresse ein.")
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    is_approved = (current_user is not None and current_user.role in ["admin", "moderator"])
    db_entry = models.GuestbookEntry(name=entry.name.strip(), email=entry.email.strip(), message=entry.message.strip(), created_at=now_str, approved=is_approved)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@app.delete("/api/guestbook/{id}")
def delete_guestbook_entry(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator"]))):
    db_entry = db.query(models.GuestbookEntry).filter(models.GuestbookEntry.id == id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Eintrag nicht gefunden")
    db.delete(db_entry)
    db.commit()
    return {"message": "Eintrag gelöscht"}

@app.get("/api/admin/pending")
def get_pending_moderation(db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator"]))):
    guestbook = db.query(models.GuestbookEntry).filter(models.GuestbookEntry.approved == False).all()
    archive = db.query(models.ArchiveItem).filter(models.ArchiveItem.approved == False).all()
    timeline = db.query(models.HistoricalEntry).filter(models.HistoricalEntry.approved == False).all()
    songs = db.query(models.Song).filter(models.Song.approved == False).all()
    recipes = db.query(models.Recipe).filter(models.Recipe.approved == False).all()
    return {
        "guestbook": [schemas.GuestbookResponse.model_validate(item) for item in guestbook],
        "archive": [schemas.ArchiveItem.model_validate(item) for item in archive],
        "timeline": [schemas.HistoricalEntry.model_validate(item) for item in timeline],
        "songs": [schemas.Song.model_validate(item) for item in songs],
        "recipes": [schemas.RecipeResponse.model_validate(item) for item in recipes]
    }

@app.put("/api/admin/approve/{category}/{id}")
def approve_pending_item(category: str, id: int, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator"]))):
    model_map = {
        "guestbook": models.GuestbookEntry,
        "archive": models.ArchiveItem,
        "timeline": models.HistoricalEntry,
        "songs": models.Song,
        "recipes": models.Recipe
    }
    if category not in model_map:
        raise HTTPException(status_code=400, detail="Ungültige Kategorie")
    model = model_map[category]
    item = db.query(model).filter(model.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Eintrag nicht gefunden")
    item.approved = True
    db.commit()
    return {"message": f"Eintrag in {category} (ID {id}) erfolgreich freigegeben."}

@app.delete("/api/admin/reject/{category}/{id}")
def reject_pending_item(category: str, id: int, db: Session = Depends(get_db), current_user: models.User = Depends(check_role(["admin", "moderator"]))):
    model_map = {
        "guestbook": models.GuestbookEntry,
        "archive": models.ArchiveItem,
        "timeline": models.HistoricalEntry,
        "songs": models.Song,
        "recipes": models.Recipe
    }
    if category not in model_map:
        raise HTTPException(status_code=400, detail="Ungültige Kategorie")
    model = model_map[category]
    item = db.query(model).filter(model.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Eintrag nicht gefunden")
    db.delete(item)
    db.commit()
    return {"message": f"Eintrag in {category} (ID {id}) erfolgreich abgelehnt und gelöscht."}

@app.post("/api/seed")
def seed_database(db: Session = Depends(get_db)):
    # Seed admin user
    admin_user = db.query(models.User).filter(models.User.username == "David").first()
    if not admin_user:
        hashed_pw = get_password_hash("Cleanhunter01")
        admin_user = models.User(username="David", email="david@archiv.local", hashed_password=hashed_pw, role="admin", is_verified=True)
        db.add(admin_user)
        db.commit()

    second_admin = db.query(models.User).filter(models.User.username == "admin").first()
    if not second_admin:
        hashed_pw_admin = get_password_hash("admin123")
        second_admin = models.User(username="admin", email="admin@archiv.local", hashed_password=hashed_pw_admin, role="admin", is_verified=True)
        db.add(second_admin)
        db.commit()

    test_user = db.query(models.User).filter(models.User.username == "testuser").first()
    if not test_user:
        hashed_pw_test = get_password_hash("testuser123")
        test_user = models.User(username="testuser", email="testuser@archiv.local", hashed_password=hashed_pw_test, role="user", is_verified=True)
        db.add(test_user)
        db.commit()

    # Check if data already exists to avoid duplication
    if db.query(models.Category).count() > 0:
        return {"message": "Database already seeded (Admin checked)"}

    # Create Categories
    cat_postcards = models.Category(name="Postkarten", description="Alte Postkarten")
    cat_events = models.Category(name="Ereignisse", description="Historische Ereignisse")
    cat_songs = models.Category(name="Lieder", description="Historische Lieder und Texte")
    cat_recipes = models.Category(name="Rezepte", description="Historische Rezepte")
    db.add(cat_postcards)
    db.add(cat_events)
    db.add(cat_songs)
    db.add(cat_recipes)
    db.commit()

    # Create Songs
    song1 = models.Song(
        title="Die Wacht am Rhein",
        author="Max Schneckenburger",
        origin="Deutsches Kaiserreich",
        language="Deutsch",
        sheet_music_url="/archiv/uploads/wacht_am_rhein_noten.jpg",
        lyrics="""Es braust ein Ruf wie Donnerhall,
Wie Schwertgeklirr und Wogenprall:
Zum Rhein, zum Rhein, zum deutschen Rhein,
Wer will des Stromes Hüter sein?

Lieb' Vaterland, magst ruhig sein,
Fest steht und treu die Wacht, die Wacht am Rhein!
Fest steht und treu die Wacht, die Wacht am Rhein!

Durch Hunderttausend zuckt es schnell,
Und Aller Augen blitzen hell,
Der deutsche Jüngling, fromm und stark,
Beschirmt die heil'ge Landesmark.

Lieb' Vaterland, magst ruhig sein,
Fest steht und treu die Wacht, die Wacht am Rhein!
Fest steht und treu die Wacht, die Wacht am Rhein!

Er blickt hinauf in Himmelsau'n,
Wo Heldengeister niederschau'n,
Und schwört mit stolzer Kampfeslust:
»Du Rhein bleibst deutsch wie meine Brust.«

Lieb' Vaterland, magst ruhig sein,
Fest steht und treu die Wacht, die Wacht am Rhein!
Fest steht und treu die Wacht, die Wacht am Rhein!

»Und ob mein Herz im Tode bricht,
Wirst du doch drum ein Welscher nicht;
Reich wie an Wasser deine Flut
Ist Deutschland ja an Heldenblut.«

Lieb' Vaterland, magst ruhig sein,
Fest steht und treu die Wacht, die Wacht am Rhein!
Fest steht und treu die Wacht, die Wacht am Rhein!

»Solang ein Tropfen Blut noch glüht,
Noch eine Faust den Degen zieht,
Und noch ein Arm die Büchse spannt,
Betritt kein Feind hier deinen Strand.«

Lieb' Vaterland, magst ruhig sein,
Fest steht und treu die Wacht, die Wacht am Rhein!
Fest steht und treu die Wacht, die Wacht am Rhein!

Der Schwur erschallt, die Woge rinnt,
Die Fahnen flattern hoch im Wind:
Zum Rhein, zum Rhein, zum deutschen Rhein!
Wir Alle wollen Hüter sein!

Lieb' Vaterland, magst ruhig sein,
Fest steht und treu die Wacht, die Wacht am Rhein!
Fest steht und treu die Wacht, die Wacht am Rhein!""",
        year=1840,
        category_id=cat_songs.id
    )
    db.add(song1)
    
    song2 = models.Song(
        title="Das Lied der Deutschen",
        author="August Heinrich Hoffmann von Fallersleben",
        origin="Helgoland",
        language="Deutsch",
        lyrics="""Deutschland, Deutschland über alles,
Über alles in der Welt,
Wenn es stets zu Schutz und Trutze
Brüderlich zusammenhält.
Von der Maas bis an die Memel,
Von der Etsch bis an den Belt,
Deutschland, Deutschland über alles,
Über alles in der Welt!

Deutsche Frauen, deutsche Treue,
Deutscher Wein und deutscher Sang
Sollen in der Welt behalten
Ihren alten schönen Klang,
Uns zu edler Tat begeistern
Unser ganzes Leben lang.
Deutsche Frauen, deutsche Treue,
Deutscher Wein und deutscher Sang!

Einigkeit und Recht und Freiheit
Für das deutsche Vaterland!
Danach lasst uns alle streben
Brüderlich mit Herz und Hand!
Einigkeit und Recht und Freiheit
Sind des Glückes Unterpfand;
Blüh' im Glanze dieses Glückes,
Blühe, deutsches Vaterland!""",
        year=1841,
        category_id=cat_songs.id
    )
    db.add(song2)

    song3 = models.Song(
        title="Heil dir im Siegerkranz",
        author="Heinrich Harries",
        origin="Königreich Preußen",
        language="Deutsch",
        lyrics="""Heil dir im Siegerkranz,
Herrscher des Vaterlands!
Heil, Kaiser, dir!
Fühl in des Thrones Glanz
Die hohe Wonne ganz,
Liebling des Volks zu sein!
Heil, Kaiser, dir!

Nicht Roß und Reisige
Sichern die steile Höh',
Wo Fürsten steh'n:
Liebe des Vaterlands,
Liebe des freien Manns,
Gründen den Herrschers Thron
Wie Fels im Meer.

Heilige Flamme, glüh',
Glüh' und erlösche nie
Fürs Vaterland!
Wir alle stehen dann
Mutig für einen Mann,
Kämpfen und bluten gern
Für Thron und Reich!""",
        year=1790,
        category_id=cat_songs.id
    )
    db.add(song3)

    song4 = models.Song(
        title="Preußenlied",
        author="Bernhard Thiersch",
        origin="Königreich Preußen",
        language="Deutsch",
        lyrics="""Ich bin ein Preuße, kennt ihr meine Farben?
Die Fahne schwebt mir weiß und schwarz voran;
Daß für die Freiheit meine Väter starben,
Das deuten, merkt es, meine Farben an.
Nie werd ich bang verzagen,
Wie jene will ich's wagen
Sei's trüber Tag, sei's heitrer Sonnenschein,
Ich bin ein Preuße, will ein Preuße sein.

Mit Lieb und Treue nah ich mich dem Throne,
Von welchem mild zu mir ein Vater spricht;
Und wie der Vater treu mit seinem Sohne,
So steh ich treu mit ihm und wanke nicht.
Fest sind der Liebe Bande,
Heil meinem Vaterlande!
Des Königs Ruf dringt in das Herz mir ein:
Ich bin ein Preuße, will ein Preuße sein.""",
        year=1830,
        category_id=cat_songs.id
    )
    db.add(song4)
    
    db.commit()

    # Load 30 additional songs from JSON
    try:
        with open("songs_data.json", "r", encoding="utf-8") as f:
            additional_songs = json.load(f)
            for s_data in additional_songs:
                new_song = models.Song(
                    title=s_data.get("title"),
                    author=s_data.get("author"),
                    origin=s_data.get("origin"),
                    language=s_data.get("language"),
                    lyrics=s_data.get("lyrics"),
                    year=s_data.get("year"),
                    sheet_music_url=s_data.get("sheet_music_url"),
                    history=s_data.get("history"),
                    category_id=cat_songs.id
                )
                db.add(new_song)
        db.commit()
    except Exception as e:
        print(f"Failed to load songs_data.json: {e}")

    # Create ArchiveItems
    p1 = models.ArchiveItem(
        title="Das Herz am Rhein", 
        description='Transkription: "Das Herz am Rhein. Es liegt eine Leier im grünen Rhein, Gezaubert von Gold und von Edelstein, Und wer sie erhebt vom tiefen Grund, Dem strömen die Lieder begeistert vom Mund."', 
        image_url="/archiv/uploads/pc_14.jpg",
        year=1914, 
        item_type="Postkarte",
        category_id=cat_postcards.id
    )
    p2 = models.ArchiveItem(
        title="Feldpostkarte aus Lorentzweiler (12.08.1914)", 
        description='Transkription: "Lorentzweiler, den 12.8.14. Liebe Liesel! Wie heute Nachmittag nochmal zum Abendessen das Telegramm. Dienst in Treuen; bin noch gesund u. munter was ich auch von Dir hoffe, und von Papa. Heute wurde ausgerufen, daß noch keine Post von Hause ausgegeben ist. Hoffentlich erhalte ich bald ein Lebenszeichen von Dir. So nimm nun für heute die herzlichsten Grüße von Deinem Walther. (Absender: Bf. Uffz. W. Krause 6/118, 50 Brigade 25 Division, 18 Armeekorps)"', 
        image_url="/archiv/uploads/pc1.jpg",
        year=1914, 
        item_type="Postkarte",
        category_id=cat_postcards.id
    )
    p3 = models.ArchiveItem(
        title="Feldpostkarte aus Fresnoy-le-Roye (25.11.1914)", 
        description='Transkription: "Fresnoy-le-Roye, den 25.11.14. Mein Lisel! Die besten Grüße heute am Geburtstag unseres Landesherrn, sendet dir und den Deinigen, Dein Walther. Auf baldiges Wiedersehen."', 
        image_url="/archiv/uploads/pc2.jpg",
        year=1914, 
        item_type="Postkarte",
        category_id=cat_postcards.id
    )
    p4 = models.ArchiveItem(
        title="Postkarte aus Bettenburg (08.08.1914)", 
        description='Transkription: "Bettenburg, d. 8.8.14. Mein Lisel! Ich habe hier nun das schönste Wetter, gerade wie im Juli. Vielmals grüßt Dich & Vater, Dein Walther. Lass bitte auch bald mal ein Lebenszeichen von Dir sehen. Nochmals viel tausend Grüße, Walther."', 
        image_url="/archiv/uploads/pc3.jpg",
        year=1914, 
        item_type="Postkarte",
        category_id=cat_postcards.id
    )
    p5 = models.ArchiveItem(
        title="Feldpostkarte aus Fresnoy-le-Roye (24.11.1914)", 
        description='Transkription: "Fresnoy-le-Roye, den 24.11.1914. Mein Lisel! Soeben Dein liebes Paket erhalten und danke dir vielmals dafür. Hatte Dir gestern nochmal geschrieben, weil ich mir einbildete, dass Pakete schon ins Feld geschickt worden sind. Bin noch froh, gesund und munter, was ich auch von Dir hoffe. So sei nun mit Papa vieltausendmal herzlich gegrüßt von Deinem Walther."', 
        image_url="/archiv/uploads/pc6.jpg",
        year=1914, 
        item_type="Postkarte",
        category_id=cat_postcards.id
    )
    p6 = models.ArchiveItem(
        title="Postkarte aus Bettenburg (06.08.1914)", 
        description='Transkription: "Bettenburg, den 6.8.14. Mein Lisel! Bin noch froh und munter, was ich auch von Dir hoffe. Haben bis jetzt noch nichts mitgemacht. Tausend Grüße an Vater u. Dich, Dein Walther. (Absender: Bf. Uffz. W. Krause 6/118, 50 Brig. 25 Division, 8 Armeekorps)"', 
        image_url="/archiv/uploads/pc5.jpg",
        year=1914, 
        item_type="Postkarte",
        category_id=cat_postcards.id
    )
    p7 = models.ArchiveItem(
        title="Fräulein Leutnant!", 
        description='Transkription: "Fräulein Leutnant! Donnerwetter tadellos!"', 
        image_url="/archiv/uploads/pc0.jpg",
        year=1914, 
        item_type="Postkarte",
        category_id=cat_postcards.id
    )
    p8 = models.ArchiveItem(
        title="Postkarte vom 10.08.1914", 
        description='Transkription: "Liebe Lisel! Augenblicklich ist für mich hier im Geschäft wenig zu machen. Werde wohl bald nach Hause kommen. Vielmals grüßt Dich Dein Walther. Herzliche Grüße an Papa. Grüße sendet Chef."', 
        image_url="/archiv/uploads/pc8.jpg",
        year=1914, 
        item_type="Postkarte",
        category_id=cat_postcards.id
    )
    db.add_all([p1, p2, p3, p4, p5, p6, p7, p8])

    vordrucke = []
    for i in range(3, 18):
        idx = str(i).zfill(4)
        vordrucke.append(models.ArchiveItem(
            title=f"Vordruck für eiserne Rationen ({i - 2})",
            description="Vordruck für eiserne Rationen",
            image_url=f"/archiv/uploads/IMG-20251228-WA{idx}.jpg",
            year=1914,
            item_type="Vordruck",
            category_id=cat_postcards.id
        ))
    db.add_all(vordrucke)

    # Create Historical Entries
    events = [
        models.HistoricalEntry(
            title="Kriegszustand", 
            content="Kaiser Wilhelm II. erklärt den Kriegszustand für das Deutsche Reich.", 
            event_date=date(1914, 7, 31), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Kriegserklärung an Russland", 
            content="Das Deutsche Reich erklärt Russland den Krieg. Die allgemeine Mobilmachung beginnt.", 
            event_date=date(1914, 8, 1), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Einmarsch in Luxemburg", 
            content="Deutsche Truppen marschieren in das neutrale Luxemburg ein.", 
            event_date=date(1914, 8, 2), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Kriegserklärung an Frankreich", 
            content="Deutschland erklärt Frankreich offiziell den Krieg. Beginn des Schlieffen-Plans.", 
            event_date=date(1914, 8, 3), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Burgfriedenspolitik", 
            content="Der Reichstag, einschließlich der SPD, stimmt den Kriegskrediten zu. Kaiser Wilhelm II. verkündet den Burgfrieden.", 
            event_date=date(1914, 8, 4), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Schlacht bei Tannenberg (Beginn)", 
            content="Deutsche Truppen unter Hindenburg und Ludendorff beginnen die Einkesselung der russischen 2. Armee.", 
            event_date=date(1914, 8, 26), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Sieg bei Tannenberg", 
            content="Entscheidender deutscher Sieg an der Ostfront. Hindenburg wird zum Nationalhelden.", 
            event_date=date(1914, 8, 30), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Septemberprogramm", 
            content="Reichskanzler Bethmann Hollweg formuliert die weitreichenden Kriegsziele des Deutschen Reiches.", 
            event_date=date(1914, 9, 9), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Seegefecht bei Coronel", 
            content="Deutsches Ostasiengeschwader unter Admiral von Spee besiegt britische Einheiten vor der Küste Chiles.", 
            event_date=date(1914, 11, 1), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Schlacht bei den Falklandinseln", 
            content="Das deutsche Kreuzergeschwader wird von der Royal Navy fast vollständig vernichtet.", 
            event_date=date(1914, 12, 8), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Rationen eingeführt", 
            content="Erste Brotmarken werden eingeführt, um der Lebensmittelknappheit im Deutschen Reich zu begegnen.", 
            event_date=date(1915, 1, 25), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Erster Giftgaseinsatz", 
            content="Deutsche Truppen setzen in der Zweiten Flandernschlacht bei Ypern erstmals Chlorgas ein.", 
            event_date=date(1915, 4, 22), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Versenkung der RMS Lusitania", 
            content="Das deutsche U-Boot U 20 versenkt das britische Passagierschiff Lusitania, was zu starken Protesten der USA führt.", 
            event_date=date(1915, 5, 7), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Gründung der Spartakusgruppe", 
            content="Rosa Luxemburg, Karl Liebknecht und andere gründen die marxistische Spartakusgruppe.", 
            event_date=date(1915, 8, 28), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Schlacht um Verdun (Beginn)", 
            content="Deutsche Offensive gegen die französische Festung Verdun beginnt. Die Schlacht wird zum Inbegriff des Materialkriegs.", 
            event_date=date(1916, 2, 21), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Sussex-Gelöbnis", 
            content="Nach dem Angriff auf den Passagierdampfer Sussex sagt Deutschland den USA zu, Passagierschiffe nicht mehr ohne Warnung anzugreifen.", 
            event_date=date(1916, 5, 4), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Skagerrakschlacht", 
            content="Die größte Seeschlacht des Krieges zwischen der deutschen Hochseeflotte und der britischen Grand Fleet.", 
            event_date=date(1916, 5, 31), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="3. Oberste Heeresleitung", 
            content="Paul von Hindenburg und Erich Ludendorff übernehmen faktisch die militärische und politische Führung des Reiches.", 
            event_date=date(1916, 8, 29), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Friedensangebot der Mittelmächte", 
            content="Deutschland und seine Verbündeten machen den Entente-Mächten ein Friedensangebot, das jedoch abgelehnt wird.", 
            event_date=date(1916, 12, 12), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Steckrübenwinter", 
            content="Im Winter 1916/17 kommt es in Deutschland zu katastrophalen Hungersnöten. Die Steckrübe wird zum Hauptnahrungsmittel.", 
            event_date=date(1916, 12, 15), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Uneingeschränkter U-Boot-Krieg", 
            content="Deutschland nimmt den uneingeschränkten U-Boot-Krieg wieder auf, was die USA in den Krieg zwingt.", 
            event_date=date(1917, 2, 1), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Gründung der USPD", 
            content="In Gotha spaltet sich die kriegskritische USPD von der SPD ab.", 
            event_date=date(1917, 4, 6), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Friedensresolution des Reichstags", 
            content="Die Mehrheitsparteien im Deutschen Reichstag fordern einen Verständigungsfrieden ohne Annexionen.", 
            event_date=date(1917, 7, 19), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Gründung der Deutschen Vaterlandspartei", 
            content="Die rechtsextreme DVP wird gegründet, um für einen radikalen Siegfrieden und gegen die Friedensresolution zu mobilisieren.", 
            event_date=date(1917, 9, 2), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Januarstreik", 
            content="Über eine Million Rüstungsarbeiter in ganz Deutschland streiken für Frieden und bessere Lebensbedingungen.", 
            event_date=date(1918, 1, 28), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Friede von Brest-Litowsk", 
            content="Deutschland diktiert Sowjetrussland harte Friedensbedingungen und sichert sich weite Gebiete in Osteuropa.", 
            event_date=date(1918, 3, 3), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Frühjahrsoffensive", 
            content="Mit dem 'Unternehmen Michael' startet Deutschland einen letzten großen Vorstoß an der Westfront.", 
            event_date=date(1918, 3, 21), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Schwarzer Tag des deutschen Heeres", 
            content="Erfolgreicher alliierter Panzerangriff bei Amiens. Die deutsche Niederlage wird unausweichlich.", 
            event_date=date(1918, 8, 8), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Forderung nach Waffenstillstand", 
            content="Die OHL unter Ludendorff fordert überraschend von der Politik die sofortige Einleitung von Waffenstillstandsverhandlungen.", 
            event_date=date(1918, 9, 29), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Oktoberreformen", 
            content="Das Deutsche Reich wird durch Verfassungsänderungen faktisch zu einer parlamentarischen Monarchie.", 
            event_date=date(1918, 10, 28), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Kieler Matrosenaufstand", 
            content="Matrosen verweigern den Befehl zum Auslaufen. Der Aufstand weitet sich zur Novemberrevolution aus.", 
            event_date=date(1918, 11, 4), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Ausrufung der Republik", 
            content="Kaiser Wilhelm II. dankt faktisch ab. Philipp Scheidemann (SPD) und Karl Liebknecht (Spartakus) rufen in Berlin die Republik aus.", 
            event_date=date(1918, 11, 9), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Waffenstillstand von Compiègne", 
            content="Matthias Erzberger unterzeichnet den Waffenstillstand. Der Erste Weltkrieg ist beendet.", 
            event_date=date(1918, 11, 11), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Besetzung Luxemburgs", 
            content="Die deutsche Armee schließt die Besetzung des neutralen Luxemburgs ab.", 
            event_date=date(1914, 8, 2), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Einmarsch in Belgien", 
            content="Deutsche Truppen marschieren gemäß dem Schlieffen-Plan in Belgien ein.", 
            event_date=date(1914, 8, 4), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Besetzung von Brüssel", 
            content="Deutsche Truppen besetzen die belgische Hauptstadt Brüssel.", 
            event_date=date(1914, 8, 20), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Schlacht an den Masurischen Seen", 
            content="Beginn der Schlacht, die zur Vertreibung der russischen Armee aus Ostpreußen führt.", 
            event_date=date(1914, 9, 6), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Rückzug von der Marne", 
            content="Das deutsche Heer zieht sich nach der Marneschlacht zurück. Der Schlieffen-Plan ist gescheitert.", 
            event_date=date(1914, 9, 14), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Erste Flandernschlacht", 
            content="Beginn der verlustreichen Kämpfe bei Ypern (Ursprung des 'Mythos von Langemarck').", 
            event_date=date(1914, 10, 18), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Weihnachtsfrieden", 
            content="Spontane, informelle Waffenstillstände zwischen deutschen und britischen Soldaten an der Westfront.", 
            event_date=date(1914, 12, 25), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Kriegsgebiet um Großbritannien", 
            content="Deutschland erklärt die Gewässer um Großbritannien und Irland zum Kriegsgebiet.", 
            event_date=date(1915, 2, 4), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Schlacht von Gorlice-Tarnów", 
            content="Ein erfolgreicher Durchbruch der Mittelmächte an der Ostfront beginnt.", 
            event_date=date(1915, 5, 2), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Einnahme Warschaus", 
            content="Deutsche Truppen nehmen Warschau ein und drängen die russische Armee weiter zurück.", 
            event_date=date(1915, 8, 5), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Plesser Abkommen", 
            content="Zentralisierung der militärischen Führung der Mittelmächte unter deutscher Dominanz.", 
            event_date=date(1915, 9, 6), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Verschärfung der Wehrpflicht", 
            content="Das Deutsche Reich dehnt die allgemeine Wehrpflicht auf alle wehrfähigen Männer von 17 bis 45 Jahren aus.", 
            event_date=date(1916, 2, 9), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Angriff auf Mort Homme", 
            content="Schwere Kämpfe um die strategisch wichtige Höhe 'Toter Mann' bei Verdun.", 
            event_date=date(1916, 3, 21), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Schlacht an der Somme", 
            content="Beginn der britisch-französischen Großoffensive an der Somme. Extrem verlustreich auch für Deutschland.", 
            event_date=date(1916, 7, 1), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Kriegserklärung Rumäniens", 
            content="Rumänien tritt auf Seiten der Entente in den Krieg ein und zwingt Deutschland zu einem Zweifrontenkrieg im Osten.", 
            event_date=date(1916, 8, 27), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Wilsons Friedensnote", 
            content="US-Präsident Wilson fordert die kriegführenden Parteien auf, ihre Friedensbedingungen zu nennen. Deutschland zögert.", 
            event_date=date(1916, 12, 20), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Russische Februarrevolution", 
            content="Die Revolution in Russland entlastet die deutsche Ostfront erheblich.", 
            event_date=date(1917, 3, 15), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Schlacht von Arras", 
            content="Britische Offensive an der Westfront. Einsatz neuartiger Taktiken führt zu deutschen Verlusten.", 
            event_date=date(1917, 4, 9), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Einsatz von Senfgas", 
            content="Deutsche Truppen setzen bei Ypern erstmals das tödliche Senfgas (Gelbkreuz) ein.", 
            event_date=date(1917, 7, 12), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Offensive an der Piave", 
            content="Deutsche und österreichische Truppen zwingen die italienische Armee am Isonzo zum Rückzug.", 
            event_date=date(1917, 10, 24), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Olmützer Punktation", 
            content="Preußen muss unter russischem und österreichischem Druck seine Pläne für eine Erfurter Union aufgeben.", 
            event_date=date(1850, 11, 29), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Bismarck wird Ministerpräsident", 
            content="Otto von Bismarck wird vom preußischen König Wilhelm I. zum Ministerpräsidenten ernannt.", 
            event_date=date(1862, 9, 23), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Deutsch-Dänischer Krieg", 
            content="Preußen und Österreich besiegen Dänemark im Streit um die Herzogtümer Schleswig und Holstein.", 
            event_date=date(1864, 4, 18), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Schlacht bei Königgrätz", 
            content="Entscheidender preußischer Sieg im Deutschen Krieg gegen Österreich. Der Deutsche Bund löst sich auf.", 
            event_date=date(1866, 7, 3), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Gründung des Norddeutschen Bundes", 
            content="Unter preußischer Führung wird der Norddeutsche Bund als erster deutscher Bundesstaat gegründet.", 
            event_date=date(1867, 7, 1), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Emser Depesche", 
            content="Bismarcks redigierte Veröffentlichung der Emser Depesche führt zur französischen Kriegserklärung.", 
            event_date=date(1870, 7, 13), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Reichsgründung in Versailles", 
            content="König Wilhelm I. von Preußen wird im Spiegelsaal von Versailles zum Deutschen Kaiser proklamiert.", 
            event_date=date(1871, 1, 18), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Friedensvertrag von Frankfurt", 
            content="Der Deutsch-Französische Krieg endet. Frankreich muss Elsaß-Lothringen abtreten und Reparationen zahlen.", 
            event_date=date(1871, 5, 10), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Gründerkrach", 
            content="Ein massiver Börsenkrach beendet die spekulativen 'Gründerjahre' des neuen Deutschen Kaiserreichs.", 
            event_date=date(1873, 5, 9), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Sozialistengesetz", 
            content="Bismarck lässt ein Gesetz gegen die 'gemeingefährlichen Bestrebungen der Sozialdemokratie' verabschieden.", 
            event_date=date(1878, 10, 19), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Zweibund", 
            content="Das Deutsche Reich und Österreich-Ungarn schließen ein Defensivbündnis (später Dreibund mit Italien).", 
            event_date=date(1879, 10, 7), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Spartakusaufstand", 
            content="Der linksextreme Spartakusaufstand in Berlin wird von Regierungstruppen und Freikorps blutig niedergeschlagen. Rosa Luxemburg und Karl Liebknecht werden ermordet.", 
            event_date=date(1919, 1, 5), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Weimarer Nationalversammlung", 
            content="Die verfassungsgebende Nationalversammlung tritt in Weimar zusammen, abseits der Unruhen in Berlin.", 
            event_date=date(1919, 2, 6), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Versailler Vertrag unterzeichnet", 
            content="Deutschland unterzeichnet unter Protest den Friedensvertrag von Versailles.", 
            event_date=date(1919, 6, 28), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Kapp-Putsch", 
            content="Rechtsgerichtete Militärs und Freikorps versuchen die Weimarer Republik zu stürzen. Ein Generalstreik vereitelt den Putsch.", 
            event_date=date(1920, 3, 13), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Ruhraufstand", 
            content="Als Reaktion auf den Kapp-Putsch erheben sich linksgerichtete Arbeiter im Ruhrgebiet (Rote Ruhrarmee).", 
            event_date=date(1920, 3, 15), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Reichsdeputationshauptschluss", 
            content="Das letzte bedeutende Gesetz des Heiligen Römischen Reiches führt zur Säkularisation und Mediatisierung.", 
            event_date=date(1803, 2, 25), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Ende des Heiligen Römischen Reiches", 
            content="Kaiser Franz II. legt die Kaiserkrone nieder, nachdem Napoleon den Rheinbund gegründet hat.", 
            event_date=date(1806, 8, 6), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Schlacht bei Jena und Auerstedt", 
            content="Verheerende Niederlage der preußischen Armee gegen Napoleon. Preußen verliert den Großmachtstatus.", 
            event_date=date(1806, 10, 14), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Preußische Reformen", 
            content="Das Oktoberedikt leitet die Stein-Hardenbergschen Reformen ein und verkündet die Bauernbefreiung.", 
            event_date=date(1807, 10, 9), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Völkerschlacht bei Leipzig", 
            content="Die Verbündeten fügen Napoleon eine entscheidende Niederlage zu und befreien Deutschland von der französischen Herrschaft.", 
            event_date=date(1813, 10, 19), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Wiener Kongress", 
            content="Europa wird neu geordnet und der Deutsche Bund als lockerer Staatenbund gegründet.", 
            event_date=date(1815, 6, 8), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Wartburgfest", 
            content="Rund 500 Studenten fordern auf der Wartburg einen deutschen Nationalstaat und eine Verfassung.", 
            event_date=date(1817, 10, 18), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Karlsbader Beschlüsse", 
            content="Zur Unterdrückung der nationalen und liberalen Bewegung werden Pressezensur und das Verbot der Burschenschaften beschlossen.", 
            event_date=date(1819, 9, 20), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Hambacher Fest", 
            content="Erste große demokratische Massenveranstaltung. Zehntausende fordern nationale Einheit und Freiheit.", 
            event_date=date(1832, 5, 27), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Deutscher Zollverein", 
            content="Gründung eines wirtschaftlichen Binnenmarktes in Deutschland unter preußischer Führung.", 
            event_date=date(1834, 1, 1), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Erste Eisenbahnstrecke", 
            content="Der 'Adler' fährt auf der ersten deutschen Eisenbahnstrecke zwischen Nürnberg und Fürth.", 
            event_date=date(1835, 12, 7), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Schlesischer Weberaufstand", 
            content="Rebellion schlesischer Weber gegen ihre Verelendung, die vom preußischen Militär niedergeschlagen wird.", 
            event_date=date(1844, 6, 4), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Märzrevolution", 
            content="Bürger gehen in Berlin und Wien auf die Barrikaden und fordern politische Reformen.", 
            event_date=date(1848, 3, 18), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Frankfurter Nationalversammlung", 
            content="In der Paulskirche tritt das erste frei gewählte gesamtdeutsche Parlament zusammen.", 
            event_date=date(1848, 5, 18), 
            category_id=cat_events.id
        ),
        models.HistoricalEntry(
            title="Scheitern der Revolution", 
            content="Der preußische König Friedrich Wilhelm IV. lehnt die ihm angebotene Kaiserkrone ab. Die Paulskirchenverfassung scheitert.", 
            event_date=date(1849, 4, 3), 
            category_id=cat_events.id
        )
    ]
    db.add_all(events)

    db.commit()
    return {"message": "Database successfully seeded with demo data"}
