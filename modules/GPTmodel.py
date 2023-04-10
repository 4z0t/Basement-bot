from nomic.gpt4all import GPT4All
import asyncio
import signal
import platform
from .Utils import to_thread

# if platform.system() == "Windows":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# MODEL_CONFIG = {
#     "num_beams": 2,
#     "min_new_tokens": 10,
#     "max_length": 100,
#     "repetition_penalty": 2.0,
# }

# MODEL_PATH = os.getenv("GPT_MODEL_PATH")

# if MODEL_PATH is None:
#     raise Exception("GPT_MODEL_PATH isnt set!")


class AsyncGPT4All(GPT4All):
    async def open(self):
        if self.bot is not None:
            await self.close()
        # This is so dumb, but today is not the day I learn C++.
        creation_args = [
            str(self.executable_path.absolute()),
            "--model",
            str(self.model_path.absolute()),
        ]
        for k, v in self.decoder_config.items():
            creation_args.append(f"--{k}")
            creation_args.append(str(v))
        print(creation_args)
        self.bot = await asyncio.create_subprocess_exec(
            *creation_args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
        )

        # queue up the prompt.
        await self._parse_to_prompt()

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _parse_to_prompt(self):
        bot_says = [""]
        point = b""
        bot = self.bot
        while True:
            point += await bot.stdout.read(1)
            try:
                character = point.decode("utf-8")
                if (
                    character == "\f" or character == ">"
                ):  # We've replaced the delimiter character with this.
                    return "\n".join(bot_says)
                if character == "\n":
                    bot_says.append("")
                else:
                    bot_says[-1] += character
                point = b""

            except UnicodeDecodeError:
                if len(point) > 4:
                    point = b""

    async def prompt(self, prompt: str):
        """
        Write a prompt to the bot and return the response.
        """
        continuous_session = self.bot is not None
        if not continuous_session:
            await self.open()
        bot = self.bot
        bot.stdin.write(prompt.encode("utf-8"))
        bot.stdin.write(b"\n")
        return_value = await self._parse_to_prompt()
        if not continuous_session:
            await self.close()
        return return_value

    async def close(self):
        self.bot.terminate()
        await self.bot.wait()

#@to_thread
async def generate(prompt):
    async with AsyncGPT4All() as model:
        return await model.prompt(prompt)


if __name__ == "__main__":
    result = asyncio.run(generate("Расскажи про Пушкина"))

    print(result)
