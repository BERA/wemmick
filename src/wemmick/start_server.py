#!/usr/bin/env python
"""
Start webserver after loading environment variables.
"""

import os
import uvicorn

port = int(os.getenv("PORT", 8080))
host = os.getenv("HOST", "127.0.0.1")
print("running server")
uvicorn.run("server:app", host=host, port=port, log_level="info")
