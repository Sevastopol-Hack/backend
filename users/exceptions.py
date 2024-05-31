from fastapi import HTTPException, status


class UserNotAdmin(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user is not admin",
        )
