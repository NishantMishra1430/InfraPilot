from datetime import datetime 
from core.config import cred
from core.config import ROOT_DIR
from pathlib import Path

# Function Which Write Logs
def write_log(category: str, username: str, role: str, actions: str, status: str) -> None:
    """
    Valid Categories:
    - 'auth'            : Login attempts, user creation, RBAC denials
    - 'plan_read'       : Terraform plan, cost estimation, S3/EC2 list
    - 'infra_provision' : Terraform apply, resource creation
    - 'admin_destroy'   : Terraform destroy, bucket/instance deletion
    """
# Directory SetUp  
    category_dir = ROOT_DIR / ".infrapilot" / "logs" / category
    log_file = Path(category_dir / f"{category}.log")
# Directory Creation
    category_dir.mkdir(exist_ok=True, parents=True)
# Time Stamps Schema
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
# Logs Schema
    log_entry = (
        f"[{timestamp}] USER: {username.lower()} | ROLE: {role.lower()} | "
        f"ACTIONS: {actions} | STATUS: {status}\n"
    )
# Log File Creation and Save
    with open(log_file, "a", encoding="utf-8") as lf:
        lf.write(log_entry)
    

