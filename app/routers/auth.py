from fastapi import status, Depends, APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .. import models, utils, oauth2
from ..database import get_db
from ..config import settings

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/signin",
    tags=['Users']
)

@router.api_route("/", methods=["GET", "POST"])
async def signin(request:Request, username: str = Form(None), password: str = Form(None), 
                 db:Session=Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    if request.method == "GET":
        message = request.session.pop("flash_success", None)
        print(message)

        if isinstance(current_user, models.User):
            print(current_user.username)
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

        return templates.TemplateResponse(
            "signin.html", 
            {"request": request, "message": message}
        )
    
    if request.method == "POST":
        clean_username = username.strip() 
        user = db.query(models.User).filter(models.User.username == clean_username).first()
        if not user or not utils.verify(password, user.password):
            return templates.TemplateResponse("signin.html", {"request": request, 
                                                            "error": "Username and Password not match",
                                                            "username": clean_username,
                                                            "password": password})
        
        access_token = oauth2.create_access_token(data={"user_id": user.id})

        # set cookie HttpOnly        
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token",
                            value=access_token,
                            httponly=True,          
                            samesite="lax",
                            max_age=settings.access_token_expire_minutes * 60) 
        return response
        

