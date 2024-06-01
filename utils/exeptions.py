from fastapi import HTTPException, status


class InvalidObjectId(HTTPException):
    def __init__(self, object_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid ObjectId - {object_id}",
        )


class DocumentNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="No document with this id"
        )
