import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import folder_paths
import numpy as np

class BLIP2Captioning:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {"tooltip": "Input image to generate caption for."})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("caption",)
    FUNCTION = "generate_caption"
    CATEGORY = "BLIP2"

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_id = "Salesforce/blip-image-captioning-base"

        # Laden von Processor & Modell
        self.processor = BlipProcessor.from_pretrained(self.model_id)
        self.model = BlipForConditionalGeneration.from_pretrained(self.model_id).to(self.device)

    def generate_caption(self, image):
        # Sicheres Konvertieren: ComfyUI-Tensor → PIL
        pil_image = tensor2pil(image).convert("RGB")

        # BLIP Processing + Inferenz
        inputs = self.processor(images=pil_image, return_tensors="pt").to(self.device)
        out = self.model.generate(**inputs)
        caption = self.processor.decode(out[0], skip_special_tokens=True)

        return (caption,)

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

NODE_CLASS_MAPPINGS = {
    "BLIP2Captioning": BLIP2Captioning
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BLIP2Captioning": "BLIP2 Image Caption"
}

