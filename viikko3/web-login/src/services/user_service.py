from entities.user import User
from repositories.user_repository import (
    user_repository as default_user_repository
)


class UserInputError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self._user_repository = user_repository

    def check_credentials(self, username, password):
        if not username or not password:
            raise UserInputError("Username and password are required")

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise AuthenticationError("Invalid username or password")

        return user

    def create_user(self, username, password, password_confirmation):
        self.validate(username, password, password_confirmation)

        user = self._user_repository.create(
            User(username, password)
        )

        return user

    def validate(self, username, password, password_confirmation):
        if not username or not password:
            raise UserInputError("Username and password are required")

        if len(username)<3:
            raise Exception(
                f"Username {username} is too short"
            )
        
        if len(password)<8:
            raise Exception(
                f"Password is too short"
            )
        
        if not any(char.isdigit() for char in password):
            raise Exception(
                "Password must contain at least one number"
            )
        
        if password != password_confirmation:
            raise Exception(
                "Password didn't match with the confirmation"
            )


user_service = UserService()
