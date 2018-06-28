import datetime
from datetime import timedelta
import re
from html import escape

import discord
from discord.ext import commands

from utils import default

class Archiving:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def archive(self, ctx):
        await ctx.message.delete()

        archived_at = datetime.datetime.utcnow().strftime("%m/%d/%Y %I:%M %p")
        channel = ctx.channel
        topic = channel.topic

        #Topic emojis
        options = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']

        for x in enumerate(options):
            if x[1] in topic:
                topic = topic.replace(x[1], str(x[0]))

        #Topic bold
        topic = topic.replace('**', '')

        html_output = ''
        txt_output = ''
        previous_author = ''
        previous_created_at = None
        message_count = 0

        async for message in channel.history(reverse=True):
            html_content = escape(message.content)
            txt_content = message.content
            author = message.author
            created_at = message.created_at

            if not previous_created_at:
                previous_created_at = created_at

            #Bold
            html_content = re.sub(r'(\*\*)(?=\S)(.+?[*_]*)(?<=\S)\1', '<b>\g<2></b>', html_content)

            #Underline
            html_content = re.sub(r'(__)(?=\S)(.+?)(?<=\S)\1', '<u>\g<2></u>', html_content)

            #Italic
            html_content = re.sub(r'(\*|_)(?=\S)(.+?)(?<=\S)\1', '<i>\g<2></i>', html_content)

            #Strike through
            html_content = re.sub(r'(~~)(?=\S)(.+?)(?<=\S)\1', '<s>\g<2></s>', html_content)

            #Multiline codeblock
            html_content = re.sub(r'```+(?:[^`]*?\n)?([^`]+)\n?```+', '<div class="pre">\g<1></div>', html_content)

            #Inline codeblock
            html_content = re.sub(r'(`|``)([^`]+)\1', '<span class="pre">\g<2></span>', html_content)

            #Links
            html_content = re.sub(r'\[(.*?)\]\((.*?)\)', '<a href="\g<2>">\g<1></a>', html_content)

            #URLs
            html_content = re.sub(r'(\b(?:(?:https?|ftp|file)://|www\.|ftp\.)(?:\([-a-zA-Z0-9+&@#/%?=~_|!:,\.\[\];]*\)|[-a-zA-Z0-9+&@#/%?=~_|!:,\.\[\];])*(?:\([-a-zA-Z0-9+&@#/%?=~_|!:,\.\[\];]*\)|[-a-zA-Z0-9+&@#/%=~_|$]))', '<a href="\g<1>">\g<1></a>', html_content)

            #New lines
            html_content = html_content.replace('\n', '<br />')

            #@everyone
            html_content = html_content.replace('@everyone', '<span class="mention">@everyone</span>')

            #@here
            html_content = html_content.replace('@here', '<span class="mention">@here</span>')

            #User mentions
            for mention in message.mentions:
                html_content = re.sub(r'&lt;@!?(%s)&gt;' % mention.id, f'<span class="mention">@{mention.name}</span>', html_content)

            #Channel mentions
            for mention in message.channel_mentions:
                html_content = re.sub(r'&lt;#(%s)&gt;' % mention.id, f'<span class="mention">#{mention.name}</span>', html_content)

            #Role mentions
            for mention in message.role_mentions:
                html_content = re.sub(r'&lt;@&amp;(%s)&gt;' % mention.id, f'<span class="mention-{mention.name.lower().replace(" ", "-")}">@{mention.name}</span>', html_content)

            #Custom emojis
            html_content = re.sub(r'&lt;(:.*?:)(\d*)&gt;', '<img class="emoji" title="\g<1>" src="https://cdn.discordapp.com/emojis/\g<2>.png" />', html_content)

            #Attachments
            if message.attachments:
                url = message.attachments[0].url
                filename = message.attachments[0].filename
                size = default.sizeof_fmt(message.attachments[0].size)

                #Images
                if message.attachments[0].height:
                    html_content += f'\n<div>\n<a href="{url}"><img class="msg-attachment" src="{url}" /></a>\n</div>'

                else:
                    html_content += ('\n<div class="msg-attachment">'
                                     '\n<img class="msg-attachment-icon" src="../resources/assets/svg/attachment.svg" />'
                                     '\n<div class="msg-attachment-inner">'
                                     '\n<div>'
                                     f'\n<a href="{url}">{filename}</a>'
                                     '\n</div>'
                                     f'\n<div class="msg-attachment-filesize">{size}</div>'
                                     '\n</div>'
                                     f'\n<a href="{url}">'
                                     '\n<svg viewBox="0 0 24 24" class="download-button" name="Download" with="24px" height="24px"><g fill="none" fill-rule="evenodd">'
                                     '\n<path d="M0 0h24v24H0z"></path>'
                                     '\n<path class"fill" fill="currentColor" d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"></path>'
                                     '\n</g></svg>'
                                     '\n</a>'
                                     '\n</div>')

                if txt_content:
                    txt_content += f'\n{url}'

                else:
                    txt_content += url

            #Edited
            if message.edited_at:
                html_content += f'<span class="msg-edited" title="{message.edited_at.strftime("%m/%d/%Y %I:%M %p")}">(edited)</span>'

            #Reactions
            if message.reactions:
                html_content += '<span class="reaction">'

                for reaction in message.reactions:
                    emoji = str(reaction.emoji)

                    #Custom emoji
                    emoji = re.sub(r'<(:.*?:)(\d*)>', '<img class="reaction-emoji" title="\g<1>" src="https://cdn.discordapp.com/emojis/\g<2>.png" />', emoji)

                    html_content += f'<div class=\"reaction">{emoji}<div class="reaction-count">{reaction.count}</div></div>'

                html_content += '</span>'

            #Combine messages
            mins_ago = message.created_at - timedelta(minutes=5)

            if previous_author == author and mins_ago <= previous_created_at:
                html_output += f'\n<div class="msg-content">\n{html_content}\n</div>'

            else:
                previous_author = author

                if author.top_role:
                    role = author.top_role.name.lower().replace(' ', '-')

                    if role == 'testing' or role == 'muted':
                        role = 'everyone'

                else:
                    role = 'everyone'

                html_output += ('\n</div>'
                                '\n</div>'
                                '\n<div class="msg">'
                                '\n<div class="msg-left">'
                                f'\n<img class="msg-avatar" src="{author.avatar_url_as(format="png")}">'
                                '\n</div>'
                                '\n<div class="msg-right">'
                                f'\n<span class="msg-user-{role}" title="{author}">{author.name}</span>'
                                f'\n<span class="msg-date">{created_at.strftime("%m/%d/%Y %I:%M %p")}</span>'
                                '\n<div class="msg-content">'
                                f'\n{html_content}'
                                '\n</div>')

            txt_output += f'[{created_at.strftime("%m/%d/%Y %I:%M %p")}] {message.author}: {txt_content}\n\n'

            previous_created_at = created_at
            message_count += 1

        html_output = (f'\n<!DOCTYPE html>\n<html lang="en"><head>'
                       '\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
                       '\n<link rel="stylesheet" type="text/css" href="../css/style.css">'
                       f'\n<title>Map Testing - #{channel.name}</title>'
                       '\n<meta name="viewport" content="width=device-width">'
                       '\n</head>'
                       '\n<body>'
                       '\n<div class="title-wrapper">'
                       '\n<div class="title-text">'
                       '\n<span class="channel-name">'
                       '\n<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" class="channel-icon">'
                       '\n<path fill="currentColor" d="M2.27333333,12 L2.74666667,9.33333333 L0.08,9.33333333 L0.313333333,8 L2.98,8 L3.68666667,4 L1.02,4 L1.25333333,2.66666667 L3.92,2.66666667 L4.39333333,0 L5.72666667,0 L5.25333333,2.66666667 L9.25333333,2.66666667 L9.72666667,0 L11.06,0 L10.5866667,2.66666667 L13.2533333,2.66666667 L13.02,4 L10.3533333,4 L9.64666667,8 L12.3133333,8 L12.08,9.33333333 L9.41333333,9.33333333 L8.94,12 L7.60666667,12 L8.08,9.33333333 L4.08,9.33333333 L3.60666667,12 L2.27333333,12 L2.27333333,12 Z M5.02,4 L4.31333333,8 L8.31333333,8 L9.02,4 L5.02,4 L5.02,4 Z" transform="translate(1.333 2)">'   
                       '\n</path>'
                       f'\n</svg>{channel.name}'
                       '\n</span>'
                       '\n</div>'
                       '\n<div class="channel-topic">'
                       f'{topic}'
                       '\n</div>'
                       '\n</div>'
                       '\n<div id="log">'
                       f'{html_output}'
                       '\n</div>'
                       '\n</body>'
                       '\n</html>')

        txt_output = ('================================================'
                      f'\nMap Testing - #{channel.name}'
                      f'\n{topic}'
                      f'\n{archived_at} {message_count} Messages'
                      '\n================================================'
                      f'\n\n{txt_output}')

        with open(f'resources/assets/logs/{channel.name}.html', 'w', encoding='utf-8') as htmlfile:
            htmlfile.write(html_output)

        with open(f'resources/assets/logs/{channel.name}.txt', 'w', encoding='utf-8') as txtfile:
            txtfile.write(txt_output)

def setup(bot):
    bot.add_cog(Archiving(bot))
