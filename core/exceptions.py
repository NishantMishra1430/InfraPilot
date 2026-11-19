class InfraPilotError(Exception):
    """Base error for our entire CLI tool."""
    pass

class InfrastructureOfflineError(InfraPilotError):
    """Raised when Docker containers (Postgres or LocalStack) are down."""
    pass

class AuthenticationError(InfraPilotError):
    """Raised when username or password is wrong."""
    pass

class RBACDeniedError(InfraPilotError):
    """Raised when a non-admin tries to run an admin command."""
    pass