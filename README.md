# GitHub README & Dynamic Dashboard Generator

Backend modular optimizado en Python para la generación dinámica de perfiles, dashboards y assets visuales, diseñado bajo una arquitectura desacoplada compatible con entornos Serverless (Vercel) y ejecución local.

## Estructura del Proyecto

```text
.
├── api/                 # Punto de entrada Serverless (Vercel handler)
├── core/                # Núcleo lógico de la aplicación
│   ├── constants/       # Datos estructurados y perfiles centralizados
│   ├── modules/         # Motores lógicos (TemplateEngine, Router, cliente GitHub)
│   ├── routes/          # Controladores de endpoints y registro dinámico
│   ├── scripts/         # Utilidades y servidor de desarrollo local
│   ├── static/          # Recursos estáticos (hojas de estilo CSS)
│   ├── templates/       # Layouts base y componentes HTML modulares
│   └── views/           # Ensambladores de vistas
├── pyproject.toml       # Configuración del paquete e indentación de dependencias
└── vercel.json          # Configuración de despliegue Serverless