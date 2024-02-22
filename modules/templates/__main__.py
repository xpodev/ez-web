import ez

from .manager import TEMPLATE_MANAGER


def load_template_packs():
    TEMPLATE_MANAGER.load_template_packs()

    packages = TEMPLATE_MANAGER.get_packages()
    if not packages:
        ez.log.warning("No template packages loaded.")
        return
    
    ez.log.info(f"Loaded {len(packages)} template packages:")
    for package in packages:
        ez.log.info(f"\tLoaded template package: {package.info.package_name}")


load_template_packs()
