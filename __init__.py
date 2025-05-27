"""
ComfyUI Skycoder Tools
A collection of useful custom nodes for ComfyUI workflows
"""

from .nodes.directory_image_loader import NODE_CLASS_MAPPINGS as DIR_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DIR_DISPLAY_MAPPINGS
from .nodes.Aspect_Ratio_and_Tile_size_calculator import NODE_CLASS_MAPPINGS as ASPECT_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as ASPECT_DISPLAY_MAPPINGS
from .nodes.blipimagecaptioning import NODE_CLASS_MAPPINGS as BLIP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as BLIP_DISPLAY_MAPPINGS
from .nodes.BooleanToggleNode import NODE_CLASS_MAPPINGS as TOGGLE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as TOGGLE_DISPLAY_MAPPINGS
from .nodes.concatenate_and_test_if_empty import NODE_CLASS_MAPPINGS as CONCAT_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as CONCAT_DISPLAY_MAPPINGS

# Combine all Node Mappings
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

NODE_CLASS_MAPPINGS.update(DIR_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(DIR_DISPLAY_MAPPINGS)

NODE_CLASS_MAPPINGS.update(ASPECT_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(ASPECT_DISPLAY_MAPPINGS)

NODE_CLASS_MAPPINGS.update(BLIP_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(BLIP_DISPLAY_MAPPINGS)

NODE_CLASS_MAPPINGS.update(TOGGLE_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(TOGGLE_DISPLAY_MAPPINGS)

NODE_CLASS_MAPPINGS.update(CONCAT_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(CONCAT_DISPLAY_MAPPINGS)

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