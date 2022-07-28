from typing import *
import logging
from extensions.hash.bcrypt_hash import BcryptPasswordHash

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def bcrypt_hash_test(*, passwords: List[str]) -> bool:
    """
        Tests the BcryptPasswordHash implementation with a list of passwords.

        Parameters
        ----------
            passwords
                A list of passwords to test the BcryptPasswordHash implementation.

        Returns
        -------
            bool
                Returns True only if all the tests passed.
    """

    bcrypt: BcryptPasswordHash = BcryptPasswordHash.get_instance()

    password_test_results : List[bool] = []

    for password in passwords:

        # Hash the passwords
        hashed = bcrypt.hash_password(password)
        logger.info(f"\nHashed str: {hashed}")

        # Comparision to make sure hash is working
        compare_with_wrong_value : bool = bcrypt.compare_password_with_hash(f"{password} wrong", hashed)
        logger.info(f"Comparision result (for wrong password): {compare_with_wrong_value}")

        compare_with_right_value : bool = bcrypt.compare_password_with_hash(password, hashed)
        logger.info(f"Comparision result (for right password): {compare_with_right_value} \n")

        # This particular test passed
        if compare_with_wrong_value is False and compare_with_right_value is True:
            password_test_results.append(True)
        else:
        # This particular test failed
            password_test_results.append(False)

    return all(password_test_results)            


if __name__ == "__main__":
    sample_passwords : List[str] = ["abc123", "jonathan", "30568695"]
    test_result : bool = bcrypt_hash_test(passwords=sample_passwords)

    logger.info("=============================== Results =================================")

    if test_result:
        logger.info("All sample_passwords tests Passed 😀")
    else:
        logger.error("sample_passwords test Failed 🙁")

else:
    # prevent importing this module
    raise ImportError("This module should not be imported.")