class Empty:
    """Represents not filled value."""

    def __deepcopy__(self, memodict):
        """No copy, but himself."""
        return self


empty = Empty()
