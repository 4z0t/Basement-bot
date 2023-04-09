class CommandProcessor:
    def __init__(self) -> None:
        self._commands: dict[str, function()] = {}

    def register(self, prefix, callback):
        self._commands[prefix] = callback

    async def process(self, text: str, *args, **kwargs):
        for prefix, callback in self._commands.items():
            if text.startswith(prefix):
                rest_text = text.removeprefix(prefix)
                await callback(rest_text, *args, **kwargs)
                break
