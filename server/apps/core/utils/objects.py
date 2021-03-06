import hashlib


class Empty:
    """Represents not filled value."""

    def __deepcopy__(self, memodict):
        """No copy, but himself."""
        return self


empty = Empty()


def get_instance_hash(instance) -> str:
    """Generate md5 hash for instance based on pk."""
    return hashlib.md5(str(instance.pk).encode()).hexdigest()  # noqa: S303
