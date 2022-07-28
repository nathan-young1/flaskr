from typing import *
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def SingletonClass(**kwargs):
    """
    This method is a class factory.

    Summary
    -------
    This method creates a single instance of the class and stores it in ``cls.__instance`` class variable, then it overides the 
    ``cls.__new__`` method to prevent creating further instance of the class.

    Parameters
    ----------
        cls
            The class that should be turned to a singleton.
        
        **kwargs
            Keyworded arguments to initialize the single instance.

    Returns
    -------
        cls
            The class modified to be a singleton.


    Examples
    -------
    >>> # Singleton instance with no argument to __init__
    @SingletonClass()
        class ExampleClass:
            pass

    >>> \n\n        
    >>> # Singleton instance with argument to __init__
    @SingletonClass(name='joe', age=34)
        class ExampleClass
            def __init__(self, name, age):
                pass
    """

    def MakeSingletonClass(cls: Type)-> Type:
        instance = cls(**kwargs)
        # Store class instance in [cls.__instance].
        setattr(cls, "__instance", instance)

        # Create class method to get instance.
        setattr(cls, "get_instance", classmethod(lambda cls: cls.__instance))

        cls.__new__ = SingletonInstantiationError.raise_singleton_exception

        return cls

    return MakeSingletonClass

class SingletonInstantiationError(Exception):
    __MESSAGE : str = "This is a singleton class, get it's instance through [get_instance]."

    def __init__(self):
        super(SingletonInstantiationError, self).__init__(SingletonInstantiationError.__MESSAGE)

    @property
    def message(self):
        return self.__MESSAGE

    @staticmethod
    def raise_singleton_exception(cls, *args, **kwargs):
        try:
            raise SingletonInstantiationError()
        except SingletonInstantiationError as e:
            logger.error(e.message)