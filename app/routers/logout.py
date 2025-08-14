from fastapi import status, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/logout",
    tags=['Users']
)

@router.get("/")
def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(
        key="access_token",
        httponly=True,   
        samesite="lax", 
    )
    return response