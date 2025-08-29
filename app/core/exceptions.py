class DoctorDashboardError(Exception):
    """Base exception for the doctor dashboard application."""
    pass


class AuthenticationError(DoctorDashboardError):
    """Exception raised for authentication failures."""
    pass


class AuthorizationError(DoctorDashboardError):
    """Exception raised for authorization failures."""
    pass


class DoctorNotFoundError(DoctorDashboardError):
    """Exception raised when a doctor is not found."""
    pass


class DuplicateError(DoctorDashboardError):
    """Exception raised when attempting to create a duplicate resource."""
    pass


class ValidationError(DoctorDashboardError):
    """Exception raised for validation errors."""
    pass


class DatabaseError(DoctorDashboardError):
    """Exception raised for database-related errors."""
    pass