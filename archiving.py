import re
import os
import json
from urllib.parse import urlsplit

import discord
from discord.ext import commands
from utils import default

config = default.get('config.json')

def format_size(size):
    for unit in ['', 'K', 'M']:
        if abs(size) < 1024.0:
            return '%3.1f' % size, unit + 'B'

        size /= 1024.0#

def url_remove_query_string(url):
    url_split = urlsplit(url)
    return url_split.scheme + "://" + url_split.netloc + url_split.path

class Archiving:
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        global guild
        guild = self.bot.get_guild(int(config.guild))

    @commands.command(pass_context=True)
    async def archive(self, ctx):
        def process_reaction(reaction):
            return {
                'emoji': reaction.emoji,
                'count': reaction.count
            }

        def process_custom_reaction(name, id, count):
            return {
                'name': name,
                'url': f'https://cdn.discordapp.com/emojis/{id}.png',
                'count': count
            }

        def process_file(attachment):
            basename, extension = os.path.splitext(attachment.filename)
            filesize, units = format_size(attachment.size)
            return {
                'attachment': {
                    'url': attachment.url,
                    'basename': basename,
                    'extension': extension,
                    'filesize': filesize,
                    'filesize-units': units
                }
            }

        def process_image(image):
            basename, extension = os.path.splitext(image.filename)
            return {
                'image': {
                    'url': image.url,
                    'basename': basename,
                    'extension': extension 
                }
            }

        def process_custom_emoji(groups):
            name = groups[0]
            id = groups[1]
            return {
                'custom-emoji': {
                    'name': name,
                    'url': f'https://cdn.discordapp.com/emojis/{id}.png'
                }
            }

        def process_user_mention(groups):
            user = guild.get_member(int(groups[0]))
            roles = []
            for r in user.roles:
                roles.append(r.name)

            if len(roles) > 1:
                del roles[0]

            else:
                roles = ['generic']

            return {
                'user-mention': {
                    'name': user.name,
                    'discriminator': user.discriminator,
                    'avatar': url_remove_query_string(user.avatar_url_as(format='png')),
                    'roles': roles[::-1]
                }
            }

        def process_channel_mention(groups):
            channel = guild.get_channel(int(groups[0]))
            category = discord.utils.get(guild.categories, id=channel.category_id)
            return {
                'channel-mention': {
                    'name': channel.name,
                    'category': category.name,
                }
            }

        def process_role_mention(groups):
            role = discord.utils.get(guild.roles, id=int(groups[0]))
            return {
                'role-mention': {
                    'name': role.name
                }
            }

        def process_url(groups):
            url_string = groups[0]
            return {
                'url': url_string
            }

        regexes = [
            {
                'processor': process_custom_emoji,
                'regex': r'<(:.*?:)(\d*)>'
            },
            {
                'processor': process_user_mention,
                'regex': r'<@!?(\d+)>'
            },
            {
                'processor': process_channel_mention,
                'regex': r'<#(\d+)>'
            },
            {
                'processor': process_role_mention,
                'regex': r'<@&(\d+)>'
            },
            {
                'processor': process_url,
                'regex': r'(\b(?:(?:https?|ftp|file)://|www\.|ftp\.)(?:\([-a-zA-Z0-9+&@#/%?=~_|!:,\.\[\];]*\)|[-a-zA-Z0-9+&@#/%?=~_|!:,\.\[\];])*(?:\([-a-zA-Z0-9+&@#/%?=~_|!:,\.\[\];]*\)|[-a-zA-Z0-9+&@#/%=~_|$]))'
            }
        ]

        await ctx.message.delete()

        channel = ctx.channel
        topic = str(channel.topic).replace('**', '')
        options = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']

        for x in enumerate(options):
            if x[1] in topic:
                topic = topic.replace(x[1], str(x[0]))

        output = {
            'channel-name': channel.name,
            'channel-topic': topic
        }

        messages = []

        async for message in channel.history(reverse=True):
            user = message.author
            time = message.created_at
            roles = []
            for r in user.roles:
                roles.append(r.name)

            if len(roles) > 1:
                del roles[0]

            else:
                roles = ['generic']

            current_message = {
                'user': {
                    'name': user.name,
                    'discriminator': user.discriminator,
                    'avatar': url_remove_query_string(user.avatar_url_as(format='png')),
                    'roles': roles[::-1]
                },
                'date': {
                    'year': time.year,
                    'month': time.month,
                    'day': time.day
                },
                'time': {
                    'hour': time.hour,
                    'minute': time.minute
                },
                'content': []
            }

            if message.content:
                message_content = [{'text': message.content}]

                for regex in regexes:
                    for key, message_chunk in enumerate(message_content):
                        if "text" in message_chunk:
                            match = re.search(regex["regex"], message_content[key]["text"])
                            if match:
                                text = message_content[key]["text"]

                                text_before_match = text[:match.start()]
                                if text_before_match:
                                    message_content[key] = {"text": text_before_match}
                                    key += 1
                                else:
                                    del message_content[key]

                                # If there are capturing groups, send those. If not, send the
                                # whole matched string
                                processed_match = regex["processor"](
                                    match.groups() if match.groups() else match.group(0)
                                )
                                message_content.insert(
                                    key,
                                    processed_match
                                )
                                key += 1

                                text_after_match = text[match.end():]
                                if text_after_match:
                                    message_content.insert(
                                        key,
                                        {"text": text_after_match}
                                    )

                current_message['content'].append(message_content)

            if message.attachments:
                if message.attachments[0].height:
                    current_message['content'].append(process_image(message.attachments[0]))
                else:
                    current_message['content'].append(process_file(message.attachments[0]))

            messages.append(current_message)

            if message.reactions:
                reactions = {'reactions': []}

                for reaction in message.reactions:
                    emoji = str(reaction.emoji)
                    match = re.search(r'<(:.*?:)(\d*)>', emoji)

                    if match:
                        reactions['reactions'].append(process_custom_reaction(match.group(1), match.group(2), reaction.count))

                    else:
                        reactions['reactions'].append(process_reaction(reaction))

                current_message['content'].append(reactions)

        output['messages'] = messages
                    
        with open(f'logs/{channel.name}.json', 'w', encoding='utf-8') as jsonfile:
            output = json.dumps(output, indent=4)
            jsonfile.write(output)

def setup(bot):
    bot.add_cog(Archiving(bot))
