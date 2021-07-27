import discord
import json_file_handler as j

def dump(obj):
    if hasattr(obj, '__dict__'): 
        return vars(obj) 
    else:
        return {attr: getattr(obj, attr, None) for attr in obj.__slots__} 

class MyClient(discord.Client):
    async def on_ready(self):
        j.write('user', str(self.user))
        j.write('discord_connected', 'True', namespace='metadata')

    async def on_disconnect(self):
        j.write('discord_connected', 'False', namespace='metadata')

    async def on_voice_state_update(self, member, before, after):
        if member == self.user:
            j.write('muted', str(after.self_mute or after.mute))
            j.write('deafened', str(after.self_deaf or after.deaf))
            j.write('camera_enabled', str(after.self_video))
            j.write('stream_enabled', str(after.self_stream))
            j.write('afk', str(after.afk))
            j.write('connected_to_channel', 'True' if after.channel != None else 'False')
            