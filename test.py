import core.logger #as core
from core.config import ROOT_DIR
def sent() -> str:
    category : str = input("\nCategory os Log: ")
    username: str = input("\n Enter Username: ")
    role: str = input("\n Enter role: ")
    actions: str = input("\n Action Performed: ")
    Status: str = input("\nStatus: ")
    core.logger.write_log(category, username, role, actions, Status)
    path = ROOT_DIR / ".infrapilot" / "logs" / category
    return f"\n✅ Log File successfully created in {path}"
    

if __name__ == "__main__":
    status = sent()
    print(status)