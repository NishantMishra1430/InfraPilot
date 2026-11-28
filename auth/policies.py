
ROLE_POLICY = {
    # {role}: {resource: [], actions: []}
    "admin": {
        "resources": ["*"],
        "actions": ["read", "write", "delete", "manage_users"],
    },
    "developer": {
        "resources": ["ec2", "s3", "lambda"],
        "actions": ["read", "write"],
    },
    "analyst": {
        "resources": ["ec2", "s3", "lambda"],
        "actions": ["read", "write"],
    }
}

# now for accessing these roles policies we have to define a function

def get_roles_policies(role: str) -> dict:
    """Returns the policy dict for a given role, defaulting to empty access."""
    return ROLE_POLICY.get(role.lower(), {"resources": [], "actions": []})
