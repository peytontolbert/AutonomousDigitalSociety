
import discord
import os
from chatgpt_interface_new import ChatGPTInterface

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

class PersonaBot(discord.Client):
    def __init__(self, persona_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persona_name = persona_name
        self.chatgpt_interface = ChatGPTInterface(persona_name)
        self.context = {}

    async def on_ready(self):
        print(f'{self.user} has connected to Discord as {self.persona_name}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!'):
            await self.handle_command(message)
        else:
            await self.handle_conversation(message)

    async def handle_command(self, message):
        command = message.content[1:].split()[0]
        if command == 'set_tone':
            tone = message.content.split()[1]
            self.context['tone'] = tone
            await message.channel.send(f'Tone set to {tone}')
        elif command == 'clear_context':
            self.context = {}
            await message.channel.send('Context cleared')
        else:
            await message.channel.send('Unknown command')

    async def handle_conversation(self, message):
        system_prompt = "You are a helpful assistant."
        tone = self.context.get('tone', 'neutral')
        response = self.chatgpt_interface.chat_with_llm(system_prompt, message.content, tone=tone)
        await message.channel.send(response)

if __name__ == "__main__":
    persona_name = os.getenv("PERSONA_NAME")
    token = os.getenv("DISCORD_TOKEN")
    client = PersonaBot(persona_name, intents=intents)
    client.run(token)
