from PIL import Image
import numpy as np
import torch

class ImageBasicNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),  # ComfyUI-internes Bildobjekt
                "operation": (["no operation", "resize", "grayscale"],), # Auswahlfunktion
                "keep_aspect_ratio": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "new_width": ("INT", {"default": 256, "min": 1, "max": 4096}),
                "new_height": ("INT", {"default": 256, "min": 1, "max": 4096}),
            }
        }

    RETURN_TYPES = ("INT", "INT", "FLOAT", "STRING", "STRING", "IMAGE")
    RETURN_NAMES = ("width", "height", "ratio", "mode", "format", "output_image")
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
        return

    def correctDimensions(self, width, height, ratio):
        if ratio > width / height:
            o_width = int(width)
            o_height = int(width / ratio)
        elif ratio <= width / height:
            o_width = int(height * ratio)
            o_height = int(height)
        return (o_width, o_height)

    def process_image(self, image, operation, keep_aspect_ratio, new_width=None, new_height=None):
        # ComfyUI gibt ein numpy-Array zurück, PIL braucht das als Image
        pil_image = self.tensor2pil(image)

        width, height = pil_image.size
        ratio = width / height
        output_image = pil_image  # Default

        if operation == "resize" and new_width and new_height:
            if keep_aspect_ratio:
                new_width, new_height = self.correctDimensions(new_width, new_height, ratio)

            output_image = pil_image.resize((new_width, new_height))
            width, height = output_image.size
        # (Wenn nicht resized wird, bleibt Bild wie es ist)

        elif operation == "grayscale":
            self.bwimage(output_image)

        ratio = width / height
        mode = output_image.mode
        form = output_image.format
        
        # Für ComfyUI zurück in Tensor wandeln
        img_tensor = self.pil2tensor(output_image)

        return (width, height, ratio, mode, form, img_tensor)


NODE_CLASS_MAPPINGS = {
    "ImageBasicNode": ImageBasicNode,
}
