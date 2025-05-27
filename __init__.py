"""
ComfyUI Skycoder Tools
A collection of useful custom nodes for ComfyUI workflows
"""

from .nodes.directory_image_loader import NODE_CLASS_MAPPINGS as DIR_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DIR_DISPLAY_MAPPINGS

# Kombiniere alle Node-Mappings (für zukünftige Erweiterungen)
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Directory Image Loader Nodes
NODE_CLASS_MAPPINGS.update(DIR_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(DIR_DISPLAY_MAPPINGS)

# Exportiere alle Node-Mappings für ComfyUI
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Metadaten
__version__ = "1.0.0"
__author__ = "Skycoder"
__description__ = "A collection of useful custom nodes for ComfyUI workflows"
__license__ = "MIT"

# ComfyUI Manager Metadaten
WEB_DIRECTORY = "./web"

print(f"🛠️ Skycoder Tools v{__version__} loaded successfully!")
print(f"📦 Loaded nodes: {len(NODE_CLASS_MAPPINGS)} nodes available")