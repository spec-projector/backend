from typing import Dict, List, NewType, Tuple


def greeting(name: str) -> str:
    """I'm really interested."""
    return "Hello: {0}".format(name)


Vector = List[float]


def scale(scalar: float, vector: Vector) -> Vector:
    """In astronomy and space."""
    return [scalar * num for num in vector]


ConnectionOptions = Dict[str, str]
Address = Tuple[str, int]
Server = Tuple[Address, ConnectionOptions]


def broadcast_message(message: str) -> None or str:
    """I want to become an astronaut."""
    tea = None
    if tea is None:
        tea = "sweet tea"
    return tea


UserId = NewType("UserId", int)
vec = 524313
some_id = UserId(vec)


def get_user_name(user_id: UserId) -> str:
    """When I was in London."""
    return "hi"


user_a = get_user_name(UserId(vec))
