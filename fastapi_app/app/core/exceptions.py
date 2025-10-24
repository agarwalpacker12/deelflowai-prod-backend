"""
Custom exceptions for the application
"""

from fastapi import HTTPException, status

class DeelFlowAIException(Exception):
    """Base exception for DeelFlowAI application"""
    pass

class NotFoundError(DeelFlowAIException):
    """Resource not found exception"""
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)

class ValidationError(DeelFlowAIException):
    """Validation error exception"""
    def __init__(self, message: str = "Validation error"):
        self.message = message
        super().__init__(self.message)

class AuthorizationError(DeelFlowAIException):
    """Authorization error exception"""
    def __init__(self, message: str = "Authorization error"):
        self.message = message
        super().__init__(self.message)

class AuthenticationError(DeelFlowAIException):
    """Authentication error exception"""
    def __init__(self, message: str = "Authentication error"):
        self.message = message
        super().__init__(self.message)

class BusinessLogicError(DeelFlowAIException):
    """Business logic error exception"""
    def __init__(self, message: str = "Business logic error"):
        self.message = message
        super().__init__(self.message)

class ExternalServiceError(DeelFlowAIException):
    """External service error exception"""
    def __init__(self, message: str = "External service error"):
        self.message = message
        super().__init__(self.message)

# HTTP Exception helpers
def raise_not_found(message: str = "Resource not found"):
    """Raise 404 HTTP exception"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=message
    )

def raise_validation_error(message: str = "Validation error"):
    """Raise 422 HTTP exception"""
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=message
    )

def raise_authorization_error(message: str = "Authorization error"):
    """Raise 403 HTTP exception"""
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=message
    )

def raise_authentication_error(message: str = "Authentication error"):
    """Raise 401 HTTP exception"""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message
    )

def raise_business_logic_error(message: str = "Business logic error"):
    """Raise 400 HTTP exception"""
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )

def raise_external_service_error(message: str = "External service error"):
    """Raise 502 HTTP exception"""
    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=message
    )
