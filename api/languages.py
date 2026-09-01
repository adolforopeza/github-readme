import os
import requests
from http.server import BaseHTTPRequestHandler
import math

COLORS = {
    "PHP": "4F5D95", "JavaScript": "F1E05A", "HTML": "E34C26", "CSS": "563D7C",
    "Less": "1D365D", "Shell": "89E051", "GDScript": "355570", "Vue": "41B883",
    "SCSS": "C6538C", "PLpgSQL": "336791", "VCL": "1B887A", "Hack": "878787",
    "Python": "3776AB", "Rust": "DEA584", "C++": "F34B7D", "C": "555555",
    "TypeScript": "3178C6", "Go": "00ADD8", "Java": "B07219", "Ruby": "701516",
    "C#": "178600", "Swift": "F05138", "Kotlin": "A97BFF", "Dart": "00B4AB",
    "Lua": "000080", "Perl": "0298C3", "R": "198CE7", "Scala": "C22D40",
    "PowerShell": "012456", "Dockerfile": "384d54", "SQL": "E38C00",
    "Assembly": "6E4C13", "Batch": "C1F12E", "Clojure": "DB5855",
    "Elixir": "6E4A7E", "Elm": "60B5CC", "Erlang": "B83998", "F#": "B845FC",
    "Groovy": "4298B8", "Haskell": "5E5086", "Julia": "A270BA", "Lisp": "3FB68B",
    "Makefile": "427819", "Matlab": "E16737", "Nim": "FFC200", "Objective-C": "438EFF",
    "OCaml": "3BE133", "Pascal": "E3F171", "PostScript": "DA291C", "Prolog": "74283C",
    "Solidity": "AA6746", "Svelte": "FF3E00", "TeX": "3D6117", "WebAssembly": "04133B",
    "XML": "0060AC", "YAML": "CB171E", "Zig": "EC915C"
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        token = os.getenv("GH_TOKEN")
        if not token:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Missing GH_TOKEN configuration.")
            return

        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "Vercel-Stats-Optimizer"
        })

        repos = []
        page = 1
        per_page = 100

        while True:
            url = (
                f"https://api.github.com/user/repos"
                f"?visibility=all"
                f"&affiliations=owner,collaborator,organization_member"
                f"&per_page={per_page}"
                f"&page={page}"
            )

            response = session.get(url, timeout=10)
            if response.status_code != 200:
                break

            data = response.json()
            if not data or not isinstance(data, list):
                break

            repos.extend(data)
            if len(data) < per_page:
                break
            page += 1

        global_languages = {}
        total_bytes = 0

        for repo in repos:
            lang_url = repo.get("languages_url")
            if not lang_url:
                continue

            lang_res = session.get(lang_url, timeout=5)
            if lang_res.status_code == 200:
                for lang, bytes_count in lang_res.json().items():
                    global_languages[lang] = global_languages.get(lang, 0) + bytes_count
                    total_bytes += bytes_count

        # Ordenar rigurosamente de mayor a menor según cantidad de bytes acumulados
        sorted_langs = sorted(global_languages.items(), key=lambda x: x[1], reverse=True)

        num_langs = len(sorted_langs)
        rows = math.ceil(num_langs / 3) if num_langs > 0 else 1
        svg_height = max(120, 50 + (rows * 25) + 15)

        svg_content = f'''<svg width="490" height="{svg_height}" viewBox="0 0 490 {svg_height}" xmlns="http://www.w3.org/2000/svg">
            <style>
                .title {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 600; fill: #c9d1d9; }}
                .lang-text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 12px; fill: #8b949e; }}
            </style>
            <rect width="490" height="{svg_height}" rx="6" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
            <text x="20" y="30" class="title">Estadísticas de Lenguajes (Privados y Públicos)</text>
        '''

        for i, (lang, bytes_count) in enumerate(sorted_langs):
            percentage = (bytes_count / total_bytes) * 100 if total_bytes > 0 else 0.0
            color = COLORS.get(lang, "777BB4")

            col = i % 3
            row = i // 3

            cx = 20 + (col * 155)
            cy = 60 + (row * 25)

            svg_content += f'''
                <circle cx="{cx + 5}" cy="{cy}" r="5" fill="#{color}"/>
                <text x="{cx + 18}" y="{cy + 4}" class="lang-text">{lang}: {percentage:.1f}%</text>
            '''

        svg_content += '</svg>'

        self.send_response(200)
        self.send_header("Content-type", "image/svg+xml; charset=utf-8")
        self.end_headers()
        self.wfile.write(svg_content.encode("utf-8"))