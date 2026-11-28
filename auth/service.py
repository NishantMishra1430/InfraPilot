# File: auth/service.py
import bcrypt
from typing import List, Dict, Any

from core.config import cred
from core.database import get_db_session
from core.exceptions import AuthenticationError, RBACDeniedError, InfraPilotError
from core.logger import write_log
from auth.models import User
from auth.policies import get_roles_policies, ROLE_POLICY


def hash_password(plain_password: str) -> str:
    """Hashes a plaintext password using bcrypt with a random salt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def check_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a stored bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def seed_default_admin() -> None:
    """
    Runs on CLI startup. If the users table is empty, creates the
    default admin user from core/config.py (.env).
    """
    for session in get_db_session():
        existing_user = session.query(User).first()
        if existing_user:
            return

        admin_user = User(
            username=cred.DEFAULT_USERNAME.lower(),
            password_hash=hash_password(cred.DEFAULT_PASSWORD),
            role="admin",
            resources=["*"],
        )
        session.add(admin_user)
        session.commit()

        write_log(
            "auth",
            admin_user.username,
            "admin",
            "Seeded default admin user on first boot",
            "SUCCESS",
        )


def verify_user(username: str, password: str) -> Dict[str, any]:
    """
    Authenticates a user against PostgreSQL.
    Returns user context dict (username, role, resources) on succlearcess.
    Raises AuthenticationError on failure.
    """
    
    if not username or not password:
        raise AuthenticationError("Username and password cannot be empty.")

    clean_username = username.strip().lower()

    for session in get_db_session():
        user = session.query(User).filter(User.username == clean_username).first()
        
        if not user or not check_password(password, user.password_hash):
            write_log("auth", clean_username, "unknown", "Failed login attempt", "FAILED")
            raise AuthenticationError("Invalid username or password.")

        write_log("auth", user.username, user.role, "User authenticated", "SUCCESS")
        policy = get_roles_policies(user.role)
        return {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "resources": policy["resources"],
            "actions": policy["actions"],
        }

def create_user(
    actor_username: str,
    actor_role: str,
    new_username: str,
    new_password: str,
    new_role: str = "analyst"
) -> Dict[str, Any]:
    """
    Creates a new user in PostgreSQL. Restricted to 'admin' role only.
    """
    if actor_role.lower() != "admin":
        write_log(
            "auth",
            actor_username,
            actor_role,
            f"Unauthorized attempt to create user '{new_username}'",
            "RBAC_BLOCKED",
        )
        raise RBACDeniedError("Only ADMIN users can create new accounts.")

    clean_username = new_username.strip().lower()
    clean_role = new_role.strip().lower()
    if clean_role not in ROLE_POLICY.keys():
        raise InfraPilotError(f"Invalid role '{clean_role}' ONLY '{ROLE_POLICY.keys}'")

    policy = get_roles_policies(clean_role)
    for session in get_db_session():
        if session.query(User).filter(User.username == clean_username).first():
            raise InfraPilotError(f"User '{clean_username}' already exists.")

        new_user = User(
            username=clean_username,
            password_hash=hash_password(new_password),
            role=clean_role,
            resources=policy["resources"],
            actions=policy["actions"]
        )
        session.add(new_user)
        session.commit()

        write_log(
            "auth",
            actor_username,
            actor_role,
            f"Created user '{clean_username}' with role '{clean_role}'",
            "SUCCESS",
        )
        return {
            "username": new_user.username,
            "role": new_user.role,
            "resources": new_user.resources,
            "actions": new_user.actions
        }
        
def authorize(role: str, resource: str, action: str) -> bool:
    """Enforces Pure RBAC policy for a given role, resource, and action."""
    info = get_roles_policies(role)
    allowed_resources = info.get("resources", [])
    allowed_actions = info.get("actions", [])

    has_resource = "*" in allowed_resources or resource.lower() in allowed_resources
    has_action = action.lower() in allowed_actions

    if has_resource and has_action:
        return True

    raise RBACDeniedError(
        f"RBAC Denied: Role '{role}' cannot perform '{action}' on '{resource}'."
    )