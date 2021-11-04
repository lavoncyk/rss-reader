
class FeedProcessError(Exception):
    """Base exception for all feed processing errors."""


class InvalidEntry(FeedProcessError):
    """Fetched entry has unexpected format."""
