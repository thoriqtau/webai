from fastapi import Depends, APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .. import models, oauth2, utils
from ..database import get_db

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/forgot_password",
    tags=['Users']
)

@router.api_route("/", methods=["GET", "POST"])
async def forgot_password(request:Request, username: str = Form(None), password: str = Form(None), 
                        confirm_password: str = Form(None), db:Session=Depends(get_db),
                        current_user = Depends(oauth2.get_current_user)):
    if request.method == "GET":
        if isinstance(current_user, models.User):
            return RedirectResponse(url="/", status_code=303)

        response = templates.TemplateResponse("forgot_password.html", {"request": request, "success": False})
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        return response
    
    if request.method == "POST":
        clean_username = username.strip()
        user = db.query(models.User).filter(models.User.username == clean_username).first()
        if password is None and confirm_password is None:
            if not user:
                return templates.TemplateResponse("forgot_password.html", {
                    "request": request,
                    "error_username": "Incorrect username",
                    "username": clean_username,
                    "success": False
                })

            return templates.TemplateResponse("forgot_password.html", {
                "request": request,
                "success": True,
                "username": clean_username
            })
        
        elif len(password) < 6:
            return templates.TemplateResponse("forgot_password.html", {
                "request": request,
                "error_password": "Password must be at least 6 characters",
                "username": clean_username,
                "password": password,
                "confirm_password": confirm_password,
                "success": True
            })
        
        elif password != confirm_password:
            return templates.TemplateResponse("forgot_password.html", {
                "request": request,
                "error_password": "Password and Confirm Password do not match",
                "username": clean_username,
                "password": password,
                "confirm_password": confirm_password,
                "success": True
            })
        else:
            user.password = utils.hash(password)
            db.commit()
    
            request.session["flash_success"] = "Reset Password Success"

            return RedirectResponse(
                url="/signin", 
                status_code=status.HTTP_303_SEE_OTHER
            )