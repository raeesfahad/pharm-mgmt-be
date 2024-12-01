from fastapi_login import LoginManager
from secrets import secret
from user.tables import User
from sqlmodel import Session, select
from database.connecter import engine

manager = LoginManager(secret, "/api/auth/login")

@manager.user_loader()
def query_user(username : str):
    with Session(engine) as session:
        statment = select(User).where(User.username == username)
        user = session.exec(statment).first()
    return user


