"""Entry point for SGS.

Works with both:
    python -m SGS.main
    python SGS/main.py
"""
from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from SGS.database import init_db
from SGS.splash import announce_startup
from SGS.dashboard import NeonDashboard


def main() -> None:
    init_db()
    announce_startup()
    app = NeonDashboard()
    app.mainloop()


if __name__ == "__main__":
    main()
