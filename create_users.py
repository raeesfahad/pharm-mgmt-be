# Import necessary modules
from database.connecter import engine
from user.tables import User
from sqlmodel import Session


# Function to create a new user
def create_user(username: str, password: str) -> str:
    """
    Creates a new user in the database.

    Args:
    - username (str): The username of the new user.
    - password (str): The password of the new user.

    Returns:
    - str: A success message indicating the user has been created.
    """
    with Session(engine) as session:
        # Create a new User object
        user = User(username=username, password=password)
        
        # Add the user to the session
        session.add(user)
        
        # Commit the changes to the database
        session.commit()
        
        # Return a success message
        return f"{user.username} has been created"


# Get user input
username: str = input("Enter Username: ")
password: str = input("Enter Password: ")


# Create a new user and print the result
uu = create_user(username, password)
print(uu)
