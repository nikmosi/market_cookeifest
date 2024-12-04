from typing import Any


class ApplicationError(Exception):
    """Base exception type for the application custom exception types."""

    detail: str

    def __init__(self, *args: Any, detail: str = "") -> None:
        """Initialize ``AdvancedAlchemyException``.

        Args:
            *args: args are converted to :class:`str` before passing to :class:`Exception`
            detail: detail of the exception.
        """
        str_args = [str(arg) for arg in args if arg]
        if not detail:
            if str_args:
                detail, *str_args = str_args
            elif hasattr(self, "detail"):
                detail = self.detail
        self.detail = detail
        super().__init__(*str_args)

    def __repr__(self) -> str:
        if self.detail:
            return f"{self.__class__.__name__} - {self.detail}"
        return self.__class__.__name__

    def __str__(self) -> str:
        return " ".join((*self.args, self.detail)).strip()


class RetryError(ApplicationError):
    def __init__(self, url: str, retries: int, *args: Any) -> None:
        detail = f"Failed to fetch {url} after {retries} attempts."
        super().__init__(*args, detail=detail)


class BasketError(ApplicationError):
    def __init__(self, article: str, postfix: str, *args: Any) -> None:
        detail = f"Cant find url for basket. {article=}, {postfix=}."
        super().__init__(*args, detail=detail)
