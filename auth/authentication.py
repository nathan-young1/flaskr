import logging
from sqlalchemy import select
from extensions.oop.singleton import SingletonClass
from db.db_connector import MYSQL_DB
from auth.user_model import User
from extensions.hash.bcrypt_hash import BcryptPasswordHash
from typing import Union

# Intialize logger.
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

@SingletonClass()
class AuthenticationHandler:

    def validate_login_credientials(self, username : str, password : str) -> bool:
        """
            Check if the login credientials are valid.

            Parameters
            ----------
                username
                    The username of the user
                
                password
                    The password of the user

            Returns
            -------
                bool
                    A boolean result based on the validity of the user's credientials
        """

        user_details_from_db : Union[None, User] = self.__return_user_if_exists(username)

        if user_details_from_db is None: return False

        # compare the inputed password with password in the DB
        return (
            BcryptPasswordHash
                .get_instance()
                .compare_password_with_hash(password, user_details_from_db.password)
                )

    def register(self, username : str, password : str):
        """
            Registers a new user to database.

            Parameters
            ----------
                username
                    The desired username of the user
                
                password
                    The desired password of the user

            Returns
            -------
                bool
                    Returns False if the user already exists otherwise 
                    returns True when the user is registered successfully.
        """
        user : Union[None, User] = self.__return_user_if_exists(username)
        
        # User already exists
        if user is not None: return False

        # Otherwise create a new user in db
        with MYSQL_DB.start_transaction() as db:
            db.add(
                User(
                    username=username, 
                    password=BcryptPasswordHash.get_instance().hash_password(password)
                    )
                )
            return True

    def forgot_password(self, username : str, newPassword : str):
        """
            changes the password of the user in the database.

            Parameters
            ----------
                username
                    The username of the user
                
                newPassword
                    The user's new password.

            Returns
            -------
                bool
                    Returns False if the user does not exists in the database otherwise 
                    returns True when the user's password is changed successfully.
        """
        user : Union[None, User] = self.__return_user_if_exists(username)
        
        # User does not exist in the database
        if user is None: return False

        # Otherwise change the user's password
        with MYSQL_DB.start_transaction():
            user.password = BcryptPasswordHash.get_instance().hash_password(newPassword)
            return True


    def __return_user_if_exists(self, username) -> Union[None, User]:
        """
            Return the user of the database if it exists otherwise returns None.
        """

        with MYSQL_DB.start_transaction() as db:
            user_details_from_db : list = db.query(User).where(User.username == username).first()

        return user_details_from_db
