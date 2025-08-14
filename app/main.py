from fastapi import FastAPI, Request, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from .routers import user, auth, logout, forgot_password
from .config import settings
from . import models, oauth2
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

secret_key_session = settings.secret_key_session

app.add_middleware(GZipMiddleware)
app.add_middleware(SessionMiddleware, secret_key=secret_key_session)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(logout.router)
app.include_router(forgot_password.router)
app.include_router(user.router)

@app.get("/")
async def index(request:Request, current_user=Depends(oauth2.get_current_user)):
    if current_user == "no_login":
        return templates.TemplateResponse("index.html", {"request": request, "user": None})
    elif current_user == "expired":
        request.session["expired"] = "Token Expired"
        message = request.session.pop("expired", None)
        return templates.TemplateResponse("index.html", {"request": request, "user": None, "message": message})
    else:
        return templates.TemplateResponse("index.html", {"request": request, "user": current_user})