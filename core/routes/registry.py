# core/routes/registry.py
from core.router import router
from core.routes.home import handle_home
from core.routes.languages import handle_top_languages, handle_all_languages
from core.routes.magento import handle_magento
from core.routes.projects import handle_projects
from core.routes.profile import handle_profile

# Registro dinámico de rutas con soporte independiente para top y total de lenguajes
#router.add("/", handle_home)
# router.add("/profile", handle_profile)
router.add("/top_languages", handle_top_languages)
router.add("/all_languages", handle_all_languages)
# router.add("/magento_modules", handle_magento)
# router.add("/php_proyects", handle_projects)