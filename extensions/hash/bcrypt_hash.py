import logging
from itsdangerous import base64_decode, base64_encode
from extensions.oop.singleton import SingletonClass
from extensions.hash.hash_interface import PasswordHashInterface
import bcrypt

# Intialize logger.
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

@SingletonClass()
class BcryptPasswordHash(PasswordHashInterface):
    """
        A Hash implementation with Bcrypt.
    """

    def hash_password(self, password: str) -> str:
        password_as_bytes : bytes = password.encode('utf-8')

        # generate salt for hashing
        salt : bytes = bcrypt.gensalt()

        hashed_string : bytes = bcrypt.hashpw(password_as_bytes, salt)
        return base64_encode(hashed_string)

    def compare_password_with_hash(self, password: str, hash_str: str) -> bool:
        try: 
            password_as_bytes : bytes = password.encode('utf-8')
            hash_str_as_bytes : bytes = base64_decode(hash_str)

            return bcrypt.checkpw(password_as_bytes, hash_str_as_bytes)

        except ValueError as e:
            logger.error(f"Value Error =========> {str(e)}")
            return False
