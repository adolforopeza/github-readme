# core/routes/registry.py
from core.router import router
from core.routes.home import handle_home
from core.routes.projects import handle_projects
from core.routes.magento import handle_magento
from core.routes.languages import handle_top_languages, handle_all_languages
from core.routes.profile import handle_profile

# Registro explícito de rutas en el enrutador central
router.add("/", handle_home)
router.add("/projects", handle_projects)
router.add("/magento", handle_magento)
router.add("/languages", handle_top_languages)
router.add("/languages/all", handle_all_languages)
router.add("/profile", handle_profile)