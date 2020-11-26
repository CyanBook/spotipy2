class BaseAuthFlow:
    def __init__(self) -> None:
        raise TypeError(
            "Base types can only be used for type checking purposes: "
            "you tried to use a base type instance as argument, "
            "but you need to instantiate one of its subclass instead. "
        )
