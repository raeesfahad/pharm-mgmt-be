from sqlmodel import SQLModel, create_engine, Session


engine = create_engine("sqlite:///database.db")


def create_connection():
    SQLModel.metadata.create_all(engine)

def create_session():
    with Session(engine) as session:
        yield session
