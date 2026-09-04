# core/scripts/server.py
import os
import sys
from http.server import HTTPServer
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../.."))

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

os.chdir(root_dir)
load_dotenv()

from api.index import handler

class LocalDevServer(HTTPServer):
    allow_reuse_address = True

def run(port: int = 8000):
    server = LocalDevServer(("127.0.0.1", port), handler)
    print(f"[INFO] Servidor modular dinámico ejecutándose en http://127.0.0.1:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run()