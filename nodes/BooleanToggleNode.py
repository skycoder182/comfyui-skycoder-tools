class BooleanToggle:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "toggle": ("BOOLEAN", {"default": False, "label": "Boolean Toggle"}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("toggle_value",)
    FUNCTION = "toggle_func"
    CATEGORY = "Custom"

    def toggle_func(self, toggle):
        return (toggle,)

NODE_CLASS_MAPPINGS = {
    "BooleanToggle": BooleanToggle,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "BooleanToggle": "Boolean Toggle",
}