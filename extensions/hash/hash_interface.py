from abc import ABCMeta, abstractmethod


class PasswordHashInterface(metaclass=ABCMeta):

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """
        Parameters
        ----------
            password : str
                The text to be hashed.

        Returns
        -------
            str
                The hash representation of [text].

        """
        pass

    @abstractmethod
    def compare_password_with_hash(self, password: str, hash_str: str) -> bool:
        """
            This method hashes [password] and compares it with [hash].

            Parameters
            ----------
            password : str
                The password to compare with the hashed string.

            hash_str : str
                A string that was hashed by this class.

            Returns
            --------
                bool
                    result of the comparison.
        """
        pass
