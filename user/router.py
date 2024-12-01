from fastapi_login.exceptions import InvalidCredentialsException
from auth.local_provider import query_user, manager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends

auth_router = APIRouter(
    tags=["auth"]
)


@auth_router.post("/login")
def Login(data : OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = query_user(email)

    if not user:
        raise InvalidCredentialsException
    elif password != user.password:
         raise InvalidCredentialsException
    
    access_token = manager.create_access_token(data={"sub": email})
    return {"access_token": access_token}