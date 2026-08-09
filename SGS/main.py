from __future__ import annotations
from .database import init_db
from .splash import announce_startup
from .dashboard import NeonDashboard

def main() -> None:
    init_db()
    announce_startup()
    app = NeonDashboard()
    app.mainloop()

if __name__ == "__main__":
    main()
