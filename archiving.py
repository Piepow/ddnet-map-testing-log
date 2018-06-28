import discord
from discord.ext import commands

import datetime
from datetime import timedelta
import re
from html import escape

from utils import default


class Archiving:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def archive(self, ctx):
        await ctx.message.delete()

        with open(f'logs/test.html', 'w', encoding='utf-8') as output:
            topic = ctx.channel.topic

            #Topic emojis
            regex = r'(:)([a-z]+)\1'
            matches = re.finditer(regex, ctx.channel.topic)

            for match in matches:
                string = match.group()

                if ':zero:' in string:
                    value = '<b>0</b>'
                if ':one:' in string:
                    value = '<b>1</b>'
                elif ':two:' in string:
                    value = '<b>2</b>'
                elif ':three:' in string:
                    value = '<b>3</b>'
                elif ':four:' in string:
                    value = '<b>4</b>'
                elif ':five:' in string:
                    value = '<b>5</b>'
                elif ':six:' in string:
                    value = '<b>6</b>'
                elif ':seven:' in string:
                    value = '<b>7</b>'
                elif ':eight:' in string:
                    value = '<b>8</b>'
                elif ':nine:' in string:
                    value = '<b>9</b>'
                elif ':keycap_ten:' in string:
                    value = '<b>10</b>'

                topic = topic.replace(string, value)

            regex = r':[a-z]+:'
            matches = re.finditer(regex, topic)

            for match in matches:
                string = match.group()
                topic = topic.replace(string, '')


            #Topic bold
            regex = r'(\*\*)(?=\S)(.+?[*_]*)(?<=\S)\1'
            matches = re.finditer(regex, topic)

            for match in matches:
                string = match.group()
                old_string = string
                string = re.sub('^\*\*', '<b>', string)
                string = re.sub('\*\*$', '</b>', string)
                topic = topic.replace(old_string, string)

            author = ''
            content_html = ''
            count = 0

            async for log in ctx.message.channel.history(limit=10000000, reverse=True):
                time = log.created_at.strftime("%m/%d/%Y %I:%M %p")
                content = escape(log.content)
                count += 1
                if 'last_created_at' not in locals():
                    last_created_at = log.created_at

                #@everyone
                content = content.replace("@everyone", "<span class=\"mention-generic\">@everyone</span>")

                #@here
                content = content.replace("@here", "<span class=\"mention-generic\">@here</span>")

                #User mentions
                regex = r'&lt;@([0-9]+)&gt;'
                matches = re.finditer(regex, content)

                for match in matches:
                    mention = match.group()
                    member = ctx.guild.get_member(int(mention.replace('&lt;@', '').replace('&gt;', '')))
                    mention_html = f'<span class=\"mention-generic\">@{member.name}</span>'
                    content = content.replace(mention, mention_html)

                #Role mentions
                regex = r'&lt;@&amp;([0-9]+)&gt;'
                matches = re.finditer(regex, content)

                for match in matches:
                    mention = match.group()
                    role = discord.utils.get(ctx.guild.roles, id=int(mention.replace('&lt;@&amp;', '').replace('&gt;', '')))
                    role_class = role.name.lower()

                    if role_class == 'vanilla' or role_class == 'fng' or role_class == 'ictf' or role_class == 'zcatch':
                        role_class = 'non-ddr-moderator'

                    mention_html = f'<span class=\"mention-{role_class}\">@{role.name}</span>'
                    content = content.replace(mention, mention_html)

                #Channel mentions
                regex = r'&lt;#([0-9]+)&gt;'
                matches = re.finditer(regex, content)

                for match in matches:
                    mention = match.group()
                    channel = ctx.guild.get_channel(int(mention.replace('&lt;#', '').replace('&gt;', '')))
                    mention_html = f'<span class=\"mention-generic\">#{channel.name}</span>'
                    content = content.replace(mention, mention_html)

                #Multiline codeblock
                regex = r'```+(?:[^`]*?\n)?([^`]+)\n?```+'
                matches = re.finditer(regex, content)

                for match in matches:
                    codeblock = match.group()
                    codeblock_html = codeblock.replace('```', '')

                    if codeblock_html.startswith('\n'):
                        codeblock_html = re.sub('^\n', '', codeblock_html)

                    if codeblock_html.endswith('\n'):
                        codeblock_html = re.sub('\n$', '', codeblock_html)

                    codeblock_html = f"<pre>{codeblock_html}</pre>"
                    content = content.replace(codeblock, codeblock_html)

                #Inline codeblock
                regex = r'(`|``)([^`]+)\1'
                matches = re.finditer(regex, content)

                for match in matches:
                    codeblock = match.group()
                    codeblock_html = f"<span class=\"pre\">{codeblock.replace('`', '')}</span>"
                    content = content.replace(codeblock, codeblock_html)

                #Bold
                regex = r'(\*\*)(?=\S)(.+?[*_]*)(?<=\S)\1'
                matches = re.finditer(regex, content)

                for match in matches:
                    bold = match.group()
                    bold_html = re.sub('^\*\*', '<b>', bold)
                    bold_html = re.sub('\*\*$', '</b>', bold_html)
                    content = content.replace(bold, bold_html)

                #Underline
                regex = r'(__)(?=\S)(.+?)(?<=\S)\1'
                matches = re.finditer(regex, content)

                for match in matches:
                    underline = match.group()
                    underline_html = re.sub('^__', '<u>', underline)
                    underline_html = re.sub('__$', '</u>', underline_html)
                    content = content.replace(underline, underline_html)

                #Italic
                regex = r'(\*|_)(?=\S)(.+?)(?<=\S)\1'
                matches = re.finditer(regex, content)

                for match in matches:
                    italic = match.group()
                    italic_html = re.sub('^[\*_]', '<i>', italic)
                    italic_html = re.sub('[\*_]$', '</i>', italic_html)
                    content = content.replace(italic, italic_html)

                #Strike through
                regex = r'(~~)(?=\S)(.+?)(?<=\S)\1'
                matches = re.finditer(regex, content)

                for match in matches:
                    strike_through = match.group()
                    strike_through_html = re.sub('^~~', '<s>', strike_through)
                    strike_through_html = re.sub('~~$', '</s>', strike_through_html)
                    content = content.replace(strike_through, strike_through_html)

                #New lines
                content = content.replace('\n', '<br />')

                #URLs
                regex = r'(\b(?:(?:https?|ftp|file)://|www\.|ftp\.)(?:\([-a-zA-Z0-9+&@#/%?=~_|!:,\.\[\];]*\)|[-a-zA-Z0-9+&@#/%?=~_|!:,\.\[\];])*(?:\([-a-zA-Z0-9+&@#/%?=~_|!:,\.\[\];]*\)|[-a-zA-Z0-9+&@#/%=~_|$]))'
                matches = re.finditer(regex, content)

                for match in matches:
                    url = match.group()
                    url_html = f'<a href=\"{url}\">{url}</a>'
                    content = content.replace(url, url_html)

                #Custom emojis
                regex = r'&lt;(:.*?:)(\d*)&gt;'
                matches = re.finditer(regex, content)

                for match in matches:
                    emoji = match.group()
                    emoji_name = re.sub(r'[^a-zA-Z]', '', emoji)
                    emoji_name = emoji_name.replace('lt', '').replace('gt', '')
                    emoji_id = re.sub(r'[^0-9]', '', emoji)
                    emoji_html = f"<img class=\"emoji\" title=\"{emoji_name}\" src=\"https://cdn.discordapp.com/emojis/{emoji_id}.png\" />"
                    content = content.replace(emoji, emoji_html)

                #Attachments
                if log.attachments:
                    #Images
                    if log.attachments[0].height:
                        content += f'\n<div class=\"msg-attachment\">\n<a href=\"{log.attachments[0].url}\"><img class=\"msg-attachment\" src=\"{log.attachments[0].url}\" /></a>\n</div>'

                    else:
                        content += ('\n<div class=\"msg-attachment\">'
                                    '\n<img class=\"msg-attachment-icon\" src=\"./graphics/svg/attachment.svg\" />'
                                    '\n<div class=\"msg-attachment-inner\">'
                                    '\n<div>'
                                    f'\n<a href=\"{log.attachments[0].url}\">{log.attachments[0].filename}</a>'
                                    '\n</div>'
                                    f'\n<div class=\"msg-attachment-filesize\">{default.sizeof_fmt(log.attachments[0].size)}</div>'
                                    '\n</div>'
                                    f'\n<a href="{log.attachments[0].url}">'
                                    '\n<svg viewBox=\"0 0 24 24\" class=\"download-button\" name=\"Download\" with=\"24px\" height=\"24px\"><g fill=\"none\" fill-rule=\"evenodd\">'
                                    '\n<path d=\"M0 0h24v24H0z\"></path>'
                                    '\n<path class=\"fill\" fill=\"currentColor\" d=\"M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z\"></path>'
                                    '\n</g></svg>'
                                    '\n</a>'
                                    '\n</div>')

                #Edit
                if log.edited_at:
                    content += f'<span class=\"msg-edited\" title=\"{log.edited_at.strftime("%m/%d/%Y %I:%M %p")}\">(edited)</span>'

                #Reactions
                if log.reactions:
                    content += '<span class=\"reaction\">'

                    for reaction in log.reactions:
                        reaction_emoji = str(reaction.emoji)
                        
                        #Custom emoji
                        if '<' in str(reaction_emoji):
                            emoji = reaction_emoji
                            emoji_name = re.sub(r'[^a-zA-Z]', '', emoji)
                            emoji_id = re.sub(r'[^0-9]', '', emoji)
                            emoji_html = f"<img class=\"reaction-emoji\" title=\"{emoji_name}\" src=\"https://cdn.discordapp.com/emojis/{emoji_id}.png\" />"
                            reaction_emoji = emoji_html

                        content += f'<div class=\"reaction\">{reaction_emoji}<div class=\"reaction-count\">{reaction.count}</div></div>'

                    content += '</span>'

                #Combine messages
                mins_ago = log.created_at - timedelta(minutes=10)

                if author == log.author and mins_ago <= last_created_at:
                    content_html += f'\n<div class="msg-content">\n{content}</div>'

                else:
                    author = log.author
                    try:
                        role = str(author.top_role).lower().replace(' ', '-')

                        if role == '@everyone' or role == 'testing' or role == 'muted':
                            role = 'everyone'

                    except:
                        role = 'everyone'

                    content_html += ('\n</div>'
                                    '\n</div>'
                                    '\n<div class="msg">'
                                    '\n<div class="msg-left">'
                                    f'\n<img class="msg-avatar" src="{log.author.avatar_url_as(format="png")}">'
                                    '\n</div>'
                                    '\n<div class="msg-right">'
                                    f'\n<span class="msg-user-{role}" title="{log.author}">{log.author.name}</span>'
                                    f'\n<span class="msg-date">{time}</span>'
                                    '\n<div class="msg-content">'
                                    f'\n{content}'
                                    '\n</div>')

                last_created_at = log.created_at

            html = (f'\n<!DOCTYPE html>\n<html lang="en"><head>'
                    '\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
                    '\n<link rel="stylesheet" type="text/css" href="assets/css/style.css">'
                    f'\n<title>DDNet - {ctx.channel.name}</title>'
                    '\n<meta name="viewport" content="width=device-width">'
                    '\n</head>'
                    '\n<body>'
                    '\n<div class="log-info">'
                    '\n<div class="log-content">'
                    '\n<img class=\"map-testing-icon\" src=\"./graphics/png/map_testing.png\" />'
                    f'\n<div class="channel-name">#{ctx.channel.name}</div>'
                    f'\n<div class="channel-topic">{topic}</div>'
                    f'\n<div class="channel-messagecount">{datetime.datetime.utcnow().strftime("%m/%d/%Y %I:%M %p")} {count} messages</div>'
                    '\n</div>'
                    '\n</div>'
                    '\n<div id="log">'
                    f'{content_html}'
                    '\n</div>'
                    '\n</body>'
                    '\n</html>')

            output.write(html)

def setup(bot):
    bot.add_cog(Archiving(bot))
