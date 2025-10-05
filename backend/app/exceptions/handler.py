from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundException(CustomException):
    def __init__(self, detail: str = "Item not found"):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=detail)

class EntityTooLargeException(CustomException):
    def __init__(self, detail: str = "Request entity too large"):
        super().__init__(status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=detail)

class BadRequestException(CustomException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedException(CustomException):
    def __init__(self, detail: str = "Unauthorized access"):
        super().__init__(status_code=HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenException(CustomException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=HTTP_403_FORBIDDEN, detail=detail)

class ConflictException(CustomException):
    def __init__(self, detail: str = "Conflict occurred"):
        super().__init__(status_code=HTTP_409_CONFLICT, detail=detail)

class UnprocessableEntityException(CustomException):
    def __init__(self, detail: str = "Unprocessable entity"):
        super().__init__(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class InternalServerErrorException(CustomException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)