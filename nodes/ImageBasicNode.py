from PIL import Image
import numpy as np
import torch
import math

class ImageBasicNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),  # ComfyUI-internes Bildobjekt
                "resize": ("BOOLEAN", {"default": False}),
                "grayscale": ("BOOLEAN", {"default": False}),
                "keep_aspect_ratio": ("BOOLEAN", {"default": True}),
                "resize_mode": (["by_dimensions", "by_megapixel"], {"default": "by_megapixel"}),
            },
            "optional": {
                "target_megapixel": ("FLOAT", {"default": 1.0, "step":0.1, "min": 0.1}),
                "new_width": ("INT", {"default": 256, "min": 1, "max": 4096}),
                "new_height": ("INT", {"default": 256, "min": 1, "max": 4096}),
                "divisible_by": ([1, 2, 4, 8, 16, 32, 64], {"default": 1}),
            }
        }

    RETURN_TYPES = ("INT", "INT", "FLOAT", "STRING", "STRING", "IMAGE")
    RETURN_NAMES = ("width", "height", "ratio", "aspect_type", "aspect_ratio_common", "output_image")
    FUNCTION = "process_image"
    CATEGORY = "Beispiele/Bild"

    def tensor2pil(self, image):
        if hasattr(image, "__len__") and not isinstance(image, (bytes, str)) and len(image) > 0:
            image = image[0]
        image = image.detach().cpu().numpy()
        image = (image*255).astype(np.uint8)
        return Image.fromarray(image)

    def pil2tensor(self, image):
        image_np = np.array(image)
        image_np = image_np.astype(np.float32) / 255.0
        return torch.from_numpy(image_np).unsqueeze(0)

    def bwimage(self, image):
        px=image.load()
        for y in range(image.height):
            for x in range(image.width):
                value = px[x,y]
                if isinstance(value, tuple):
                    R, G, B = value[:3]
                    avg = int(0.299 * R + 0.587 * G + 0.114 * B)
                    px[x,y] = (avg, avg, avg)
                #print(value)
        return image

    def correctDimensions(self, width, height, ratio, target_megapixel):
        target_pixel = target_megapixel * 1000000
        o_height = int(math.sqrt(target_pixel/ratio))
        o_width = int(ratio * o_height)
        return (o_width, o_height)

    def process_image(self, image, resize, grayscale, keep_aspect_ratio, resize_mode="by_megapixel", target_megapixel=1.0, new_width=None, new_height=None, divisible_by=1):
        # ComfyUI gibt ein numpy-Array zurück, PIL braucht das als Image
        pil_image = self.tensor2pil(image)
        round_to = int(divisible_by)
        width, height = pil_image.size
        ratio = width / height
        output_image = pil_image  # Default

        if resize:
            if resize_mode == "by_megapixel" and target_megapixel:
                new_width, new_height = self.correctDimensions(width, height, ratio, target_megapixel)
            
            elif resize_mode == "by_dimensions" and new_width and new_height:
                if keep_aspect_ratio:
                    if new_width / new_height > ratio:
                        new_width = int(new_height * ratio)
                    else:
                        new_height = int(new_width / ratio)
            
            else:
                new_width, new_height = 256, 256
                if keep_aspect_ratio:
                    if new_width / new_height > ratio:
                        new_width = int(new_height * ratio)
                    else:
                        new_height = int(new_width / ratio)
            
            # Apply user-selected rounding
            new_width = max(round_to, round(new_width / round_to) * round_to)
            new_height = max(round_to, round(new_height / round_to) * round_to)

            output_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            width, height = output_image.size
        
        # grayscale if checkbox is set
        if grayscale:
            output_image = self.bwimage(output_image)

        ratio = width / height
        
        gcd = math.gcd(width, height)
        gcd_w = width // gcd
        gcd_h = height // gcd
        aspect_ratio_common = f"{gcd_w}:{gcd_h}"
        aspect_type = "landscape" if ratio > 1 else "portrait" if ratio < 1 else "square"
        
        
        # Für ComfyUI zurück in Tensor wandeln
        img_tensor = self.pil2tensor(output_image)

        return (width, height, ratio, aspect_type, aspect_ratio_common, img_tensor)


NODE_CLASS_MAPPINGS = {
    "ImageBasicNode": ImageBasicNode,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageBasicNode": "Image Advanced Resize",
}