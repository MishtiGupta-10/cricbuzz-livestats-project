class CricInsightError(Exception):
    """Base exception for all CricInsight errors."""
    pass


class CricbuzzClientError(CricInsightError):
    """Raised when the Cricbuzz API client encounters a network or HTTP error."""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class CricbuzzAPIError(CricInsightError):
    """Raised when the Cricbuzz API returns an error response."""
    pass


class CricbuzzParseError(CricInsightError):
    """Raised when failing to parse the raw JSON from Cricbuzz."""
    pass
