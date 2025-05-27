class ConcatenateAndTestIfEmpty:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "text1": ("STRING", {"forceInput": True}),
                "text2": ("STRING", {"forceInput": True}),
                "text3": ("STRING", {"forceInput": True}),
                "text4": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("is_empty", "result")
    FUNCTION = "concat_and_test"
    CATEGORY = "Custom"

    def concat_and_test(self, text1=None, text2=None, text3=None, text4=None):
        result = ""
        for t in (text1, text2, text3, text4):
            if t is not None:
                result += t
        is_empty = result == ""
        return (is_empty, result)

NODE_CLASS_MAPPINGS = {
    "ConcatenateAndTestIfEmpty": ConcatenateAndTestIfEmpty,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ConcatenateAndTestIfEmpty": "Concatenate and Test if Empty",
}