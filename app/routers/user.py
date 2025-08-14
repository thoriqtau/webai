from fastapi import Depends, APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .. import models, utils, oauth2
from ..database import get_db

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/signup",
    tags=['Users']
)

@router.api_route("/", methods=["GET", "POST"])
async def signup(request:Request, username: str = Form(None), password: str = Form(None), 
                 confirm_password: str = Form(None), db:Session=Depends(get_db), 
                 current_user = Depends(oauth2.get_current_user)):
    if request.method == "GET":
        if isinstance(current_user, models.User):
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

        return templates.TemplateResponse(
            "signup.html", 
            {"request": request}
        )
    
    if request.method == "POST":
        clean_username = username.strip() 
        if " " in clean_username:
            return templates.TemplateResponse("signup.html", {
                "request": request,
                "error_username": "Username cannot contain spaces",
                "username": clean_username,
                "password": password,
                "confirm_password": confirm_password,
                "success": None
            })
        elif len(clean_username) < 5:
            return templates.TemplateResponse("signup.html", {
                "request": request,
                "error_username": "Username min 3 length.",
                "username": clean_username,
                "password": password,
                "confirm_password": confirm_password,
                "success": None
            })
        elif db.query(models.User).filter(models.User.username == clean_username).first():
            return templates.TemplateResponse("signup.html", {
                "request": request,
                "error_username": "Username already exists",
                "username": clean_username,
                "password": password,
                "confirm_password": confirm_password,
                "success": None
            })
            # Cek panjang password
        elif len(password) < 6:
            return templates.TemplateResponse("signup.html", {
                "request": request,
                "error_password": "Password must be at least 6 characters",
                "username": clean_username,
                "password": password,
                "confirm_password": confirm_password,
                "success": None
            })
        
        elif password != confirm_password:
            return templates.TemplateResponse("signup.html", {
                "request": request,
                "error_password": "Password and Confirm Password do not match",
                "username": clean_username,
                "password": password,
                "confirm_password": confirm_password,
                "success": None
            })
        else:
            hashed_password = utils.hash(password)

            new_user = models.User(username=clean_username,password=hashed_password)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            request.session["flash_success"] = "Signup success"

            return RedirectResponse(
                url="/signin", 
                status_code=status.HTTP_303_SEE_OTHER
            )