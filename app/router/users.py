import traceback
from app.core.auth import oauth
from app.core.config import settings
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from app.helper.user_helper import UserHelper
from app.core.database import get_db
from app.schema import UserResponse
from app.core.dependencies import get_current_auth_user

router = APIRouter(prefix="/users", tags=["users"])
user_helper = UserHelper()

@router.get("/google-login")
async def google_login(request: Request):
    try:
        redirect_uri = request.url_for('google_callback')
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/google-callback")
async def google_callback(request: Request, db_session=Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
        access_token = await user_helper.get_or_create(user_data=user, db_session=db_session)
        
        if access_token == "DEACTIVATED":
            frontend_url = settings.FRONTEND_BASE_URL
            return RedirectResponse(url=f"{frontend_url}/auth/error?detail=account_deactivated")

        # Redirect to frontend with access token
        frontend_url = settings.FRONTEND_BASE_URL
        redirect_url = f"{frontend_url}/auth/google/callback?token={access_token}"
        return RedirectResponse(url=redirect_url, status_code=302)
    except HTTPException:
        raise
    except Exception:
        traceback.print_exc()
        # Redirect to frontend error page on failure
        frontend_url = settings.FRONTEND_BASE_URL
        error_redirect_url = f"{frontend_url}"
        return RedirectResponse(url=error_redirect_url)

# Creating the endpoint to show the current user info
@router.get("/me", response_model=UserResponse)
async def user_data(user=Depends(get_current_auth_user), db_session=Depends(get_db)):
    try:
        return user
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error") 