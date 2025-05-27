import os
import torch
from PIL import Image
import numpy as np

class DirectoryImageLoader:
    """
    ComfyUI Node zum Laden von Bildern aus einem Verzeichnis basierend auf Index
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Pfad zum Bildverzeichnis"
                }),
                "index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 999999,
                    "step": 1
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "filename")
    FUNCTION = "load_image_by_index"
    CATEGORY = "image/io"
    
    # Unterstützte Bildformate
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.gif'}
    
    def load_image_by_index(self, directory_path, index):
        """
        Lädt ein Bild basierend auf dem Index aus dem angegebenen Verzeichnis
        """
        try:
            # Prüfen ob Verzeichnis existiert
            if not os.path.exists(directory_path):
                raise ValueError(f"Verzeichnis nicht gefunden: {directory_path}")
            
            if not os.path.isdir(directory_path):
                raise ValueError(f"Pfad ist kein Verzeichnis: {directory_path}")
            
            # Alle Bilddateien im Verzeichnis finden und sortieren
            image_files = []
            for filename in os.listdir(directory_path):
                if any(filename.lower().endswith(ext) for ext in self.SUPPORTED_FORMATS):
                    image_files.append(filename)
            
            # Sortieren für konsistente Reihenfolge
            image_files.sort()
            
            if not image_files:
                raise ValueError(f"Keine Bilddateien im Verzeichnis gefunden: {directory_path}")
            
            # Index prüfen
            if index >= len(image_files):
                raise ValueError(f"Index {index} außerhalb des Bereichs. Verfügbare Bilder: 0-{len(image_files)-1}")
            
            # Dateiname und vollständigen Pfad ermitteln
            filename = image_files[index]
            full_path = os.path.join(directory_path, filename)
            
            # Bild laden
            image = Image.open(full_path)
            
            # Zu RGB konvertieren falls nötig
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Zu numpy array konvertieren
            image_array = np.array(image).astype(np.float32) / 255.0
            
            # Zu torch tensor konvertieren und Dimensionen anpassen für ComfyUI (batch, height, width, channels)
            image_tensor = torch.from_numpy(image_array)[None,]
            
            return (image_tensor, filename)
            
        except Exception as e:
            # Fallback: schwarzes Bild erstellen bei Fehlern
            print(f"Fehler beim Laden des Bildes: {str(e)}")
            
            # Schwarzes 512x512 Bild erstellen
            black_image = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
            error_filename = f"ERROR: {str(e)}"
            
            return (black_image, error_filename)


class DirectoryImageInfo:
    """
    Hilfsfunktion um Informationen über Bilder in einem Verzeichnis zu erhalten
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Pfad zum Bildverzeichnis"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("info", "count")
    FUNCTION = "get_directory_info"
    CATEGORY = "image/io"
    OUTPUT_NODE = True
    
    def get_directory_info(self, directory_path):
        """
        Gibt Informationen über das Bildverzeichnis zurück
        """
        try:
            if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
                return ("Verzeichnis nicht gefunden oder ungültig", 0)
            
            # Bilddateien zählen
            supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.gif'}
            image_files = []
            
            for filename in os.listdir(directory_path):
                if any(filename.lower().endswith(ext) for ext in supported_formats):
                    image_files.append(filename)
            
            image_files.sort()
            count = len(image_files)
            
            if count == 0:
                info = "Keine Bilddateien gefunden"
            else:
                info = f"Gefunden: {count} Bilder\n"
                info += f"Erste 5 Dateien:\n"
                for i, filename in enumerate(image_files[:5]):
                    info += f"  [{i}] {filename}\n"
                if count > 5:
                    info += f"  ... und {count-5} weitere"
            
            return (info, count)
            
        except Exception as e:
            return (f"Fehler: {str(e)}", 0)


# Node Registrierung für ComfyUI
NODE_CLASS_MAPPINGS = {
    "DirectoryImageLoader": DirectoryImageLoader,
    "DirectoryImageInfo": DirectoryImageInfo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DirectoryImageLoader": "📁 Directory Image Loader",
    "DirectoryImageInfo": "ℹ️ Directory Image Info"
}