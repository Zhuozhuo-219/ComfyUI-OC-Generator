class ContainsDynamicDict(dict):
    """Allow ComfyUI to expose numbered dynamic inputs like oc_block_0, oc_block_1, ..."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dynamic_prefixes = {
            key.rstrip("0123456789"): value
            for key, value in self.items()
            if isinstance(value, tuple) and len(value) > 1 and value[1].get("_dynamic") == "number"
        }

    def __contains__(self, key):
        return (
            any(key.startswith(prefix) and key[len(prefix):].isdigit() for prefix in self._dynamic_prefixes)
            or super().__contains__(key)
        )

    def __getitem__(self, key):
        for prefix, value in self._dynamic_prefixes.items():
            if key.startswith(prefix) and key[len(prefix):].isdigit():
                return value
        return super().__getitem__(key)
