from PIL import Image
import numpy as np
from math import sqrt, floor

class Aspect_Ratio_and_Tile_size_calculator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "tile_megapixel": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 100.0, "step": 0.01, "label": "Tile Megapixel"}),
                "upscale_factor": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 100.0, "step": 0.01, "label": "Upscale Factor"}),
                "tile_padding": ("INT", {"default": 0, "min": 0, "max": 4096, "step": 1, "label": "Tile Padding"}),
            }
        }

    RETURN_TYPES = ("FLOAT", "INT", "INT", "FLOAT", "INT", "INT", "INT")
    RETURN_NAMES = ("aspect_ratio", "width", "height", "upscale_factor", "tile_width", "tile_height", "tile_padding")
    FUNCTION = "get_aspect_ratio"
    CATEGORY = "Custom"

    def get_aspect_ratio(self, image, tile_megapixel, upscale_factor, tile_padding):
        # Tensor to PIL conversion
        def tensor2pil(img):
            if hasattr(img, "__len__") and not isinstance(img, (bytes, str)) and len(img) > 0:
                img = img[0]
            img = img.detach().cpu().numpy()
            img = (img * 255).astype(np.uint8)
            if img.shape[0] == 3:
                img = np.transpose(img, (1, 2, 0))
            return Image.fromarray(img)

        pil_img = tensor2pil(image)
        width, height = pil_img.size
        aspect = width / height if height else 0.0

        # Variablen
        a = upscale_factor
        b = tile_megapixel
        c = width
        d = height
        p = tile_padding

        # Berechnung tile_width und tile_height
        if c > 0 and d > 0 and b > 0 and a > 0:
            divisor = floor((c * a) / sqrt(b * 1000000 * c / d)) + 1
            tile_width = (c * a) / divisor if divisor > 0 else c * a
            tile_height = tile_width * d / c
        else:
            tile_width = 0.0
            tile_height = 0.0

        # Padding addieren
        tile_width += p
        tile_height += p

        return (float(aspect), int(width), int(height), float(upscale_factor), int(tile_width), int(tile_height), int(tile_padding))

NODE_CLASS_MAPPINGS = {
    "Aspect_Ratio_and_Tile_size_calculator": Aspect_Ratio_and_Tile_size_calculator,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Aspect_Ratio_and_Tile_size_calculator": "Aspect Ratio and Tile size calculator",
}
