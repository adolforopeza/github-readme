# api/index.py
import os
import sys
from http.server import BaseHTTPRequestHandler

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from core.router import router
import core.routes.registry

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            clean_path = self.path.split("?")[0]

            # Manejo de archivos estáticos (CSS) en entorno de desarrollo local
            if clean_path.startswith("/static/"):
                file_path = os.path.join(root_dir, "core", clean_path.lstrip("/"))
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    with open(file_path, "rb") as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header("Content-type", "text/css" if clean_path.endswith(".css") else "text/plain")
                    self.send_header("Cache-Control", "public, max-age=3600")
                    self.end_headers()
                    self.wfile.write(content)
                    return

            # Resolución dinámica O(1) de rutas del sistema
            content, c_type, status_code = router.resolve(self.path)

            self.send_response(status_code)
            if status_code == 200:
                self.send_header("Content-type", c_type)
                self.send_header("Cache-Control", "public, max-age=3600, s-maxage=3600, stale-while-revalidate=86400")
            self.end_headers()

            if status_code == 200:
                self.wfile.write(content.encode("utf-8") if isinstance(content, str) else content)
            else:
                self.wfile.write(b"Not Found")

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))