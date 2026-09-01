import os  # Importa el módulo para interactuar con las variables del sistema operativo
import requests  # Importa la librería para realizar peticiones HTTP a la API de GitHub
from http.server import BaseHTTPRequestHandler  # Importa el manejador base para la función serverless HTTP
import math  # Importa funciones matemáticas para calcular filas del diseño SVG

# Diccionario global para almacenar en caché los datos y el hash del commit actual
CACHE = {
    "data": None,  # Almacena la tupla con los lenguajes ordenados y el total de bytes
    "commit_sha": None  # Almacena el identificador único del último commit desplegado en Vercel
}

# Diccionario optimizado de colores oficiales de GitHub Linguist para los lenguajes
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

def fetch_github_stats():
    token = os.getenv("GH_TOKEN")  # Obtiene el token de autenticación de GitHub desde las variables de entorno
    if not token:  # Verifica si el token no está configurado
        raise ValueError("Missing GH_TOKEN configuration.")  # Lanza una excepción si falta el token

    session = requests.Session()  # Inicializa una sesión HTTP persistente para optimizar conexiones TCP
    session.headers.update({
        "Authorization": f"Bearer {token}",  # Configura la cabecera de autorización con el token Bearer
        "Accept": "application/vnd.github+json",  # Especifica el formato de aceptación de la API de GitHub
        "User-Agent": "Vercel-Stats-Optimizer"  # Define un agente de usuario personalizado para la petición
    })

    repos = []  # Inicializa una lista vacía para acumular todos los repositorios del usuario
    page = 1  # Inicializa el contador de paginación en la primera página
    per_page = 100  # Define el límite máximo de elementos por página permitido por la API de GitHub

    while True:  # Inicia un bucle para recorrer todas las páginas de repositorios
        url = (
            f"https://api.github.com/user/repos"
            f"?visibility=all"
            f"&affiliations=owner,collaborator,organization_member"
            f"&per_page={per_page}"
            f"&page={page}"
        )  # Construye la URL del endpoint de repositorios con los filtros necesarios

        response = session.get(url, timeout=10)  # Ejecuta la petición HTTP GET con un tiempo límite de 10 segundos
        if response.status_code != 200:  # Comprueba si la respuesta no fue exitosa
            break  # Rompe el bucle si ocurre un error o se termina el acceso

        data = response.json()  # Convierte la respuesta HTTP en un objeto JSON/diccionario de Python
        if not data or not isinstance(data, list):  # Valida si los datos están vacíos o no son una lista
            break  # Rompe el bucle si no hay más elementos válidos

        repos.extend(data)  # Añade los repositorios obtenidos a la lista principal
        if len(data) < per_page:  # Verifica si la cantidad de elementos es menor al límite por página
            break  # Rompe el bucle porque se alcanzó la última página de resultados
        page += 1  # Incrementa el número de página para la siguiente iteración

    global_languages = {}  # Inicializa un diccionario para acumular los bytes totales por lenguaje
    total_bytes = 0  # Inicializa el contador global de bytes de código analizados

    for repo in repos:  # Itera sobre cada repositorio obtenido de la lista
        lang_url = repo.get("languages_url")  # Extrae la URL del endpoint de lenguajes del repositorio actual
        if not lang_url:  # Salta al siguiente repositorio si la URL de lenguajes no existe
            continue

        lang_res = session.get(lang_url, timeout=5)  # Realiza la petición GET para obtener los lenguajes del repositorio
        if lang_res.status_code == 200:  # Verifica que la consulta de lenguajes haya sido exitosa
            for lang, bytes_count in lang_res.json().items():  # Itera sobre cada par de lenguaje y bytes devueltos
                global_languages[lang] = global_languages.get(lang, 0) + bytes_count  # Acumula los bytes por lenguaje
                total_bytes += bytes_count  # Suma los bytes al total global acumulado

    sorted_langs = sorted(global_languages.items(), key=lambda x: x[1], reverse=True)  # Ordena los lenguajes de mayor a menor según sus bytes
    return sorted_langs, total_bytes  # Retorna la lista ordenada y el total acumulado de bytes

class handler(BaseHTTPRequestHandler):  # Define la clase manejadora de peticiones HTTP para Vercel
    def do_GET(self):  # Define el método que procesa las solicitudes HTTP GET entrantes
        current_commit = os.getenv("VERCEL_GIT_COMMIT_SHA", "local-dev")  # Obtiene el SHA del commit actual inyectado por Vercel

        if CACHE["data"] is None or CACHE["commit_sha"] != current_commit:  # Comprueba si la caché está vacía o si el despliegue cambió
            try:
                sorted_langs, total_bytes = fetch_github_stats()  # Ejecuta la función de recolección de estadísticas desde GitHub
                CACHE["data"] = (sorted_langs, total_bytes)  # Actualiza la caché con los nuevos resultados calculados
                CACHE["commit_sha"] = current_commit  # Actualiza el hash del commit registrado en la caché
            except Exception as e:  # Captura cualquier excepción o error durante el proceso
                self.send_response(500)  # Envía un código de estado HTTP 500 (Error interno del servidor)
                self.end_headers()  # Finaliza las cabeceras HTTP de la respuesta de error
                self.wfile.write(str(e).encode("utf-8"))  # Escribe el mensaje de error codificado en bytes
                return
        else:
            sorted_langs, total_bytes = CACHE["data"]  # Recupera los datos directamente desde la caché si son válidos

        num_langs = len(sorted_langs)  # Obtiene la cantidad total de lenguajes detectados dinámicamente
        rows = math.ceil(num_langs / 3) if num_langs > 0 else 1  # Calcula la cantidad de filas necesarias dividiendo en columnas de 3
        svg_height = max(120, 50 + (rows * 25) + 15)  # Calcula la altura dinámica total del SVG según las filas de lenguajes

        svg_content = f'''<svg width="490" height="{svg_height}" viewBox="0 0 490 {svg_height}" xmlns="http://www.w3.org/2000/svg">
            <style>
                .title {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 600; fill: #c9d1d9; }}
                .lang-text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 12px; fill: #8b949e; }}
            </style>
            <rect width="490" height="{svg_height}" fill="#0d1117" />
            <text x="20" y="30" class="title">Estadísticas de Lenguajes (Privados y Públicos)</text>
        '''  # Define la estructura inicial del SVG con el tema oscuro de GitHub y altura dinámica

        for i, (lang, bytes_count) in enumerate(sorted_langs):  # Itera sobre cada lenguaje ordenado de mayor a menor
            percentage = (bytes_count / total_bytes) * 100 if total_bytes > 0 else 0.0  # Calcula el porcentaje exacto de uso del lenguaje
            color = COLORS.get(lang, "777BB4")  # Obtiene el color oficial del lenguaje o un valor por defecto si no existe

            col = i % 3  # Calcula la columna actual (0, 1 o 2) para distribuir en 3 columnas
            row = i // 3  # Calcula la fila actual basada en el índice iterado

            cx = 20 + (col * 155)  # Define la coordenada horizontal x para el elemento actual
            cy = 60 + (row * 25)  # Define la coordenada vertical y para el elemento actual

            svg_content += f'''
                <circle cx="{cx + 5}" cy="{cy}" r="5" fill="#{color}"/>
                <text x="{cx + 18}" y="{cy + 4}" class="lang-text">{lang}: {percentage:.1f}%</text>
            '''  # Agrega el punto indicador de color y el texto del lenguaje con su porcentaje al SVG

        svg_content += '</svg>'  # Cierra la etiqueta principal del archivo SVG

        self.send_response(200)  # Envía el código de estado HTTP 200 (Éxito)
        self.send_header("Content-type", "image/svg+xml; charset=utf-8")  # Configura la cabecera como imagen SVG válida
        self.send_header("Cache-Control", "public, max-age=3600, s-maxage=3600")  # Instruye el almacenamiento en caché HTTP estándar
        self.end_headers()  # Finaliza las cabeceras de la respuesta HTTP
        self.wfile.write(svg_content.encode("utf-8"))  # Envía el contenido completo del SVG codificado en UTF-8