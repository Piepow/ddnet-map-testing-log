# Map testing log JSON schema
- Date and time assumed to be UTC
- Don't include `size={{ value }}` query string on avatar URLs
- If a user doesn't have a role, use `"generic"`
- Some properties have a simple value (e.g. string or number) if there is only
  has one member. Otherwise, it may be a sequence or map. Examples of these
  include:
  - `content`
  - `text`

```json
{
    "channel-name": "stellar",
    "channel-topic": "Channel topic goes here",
    "messages": [
        {
            "user": {
                "name": "Ravie",
                "number": 6380,
                "avatar": "https://cdn.discordapp.com/avatars/1/1.png",
                "role": " generic "
            },
            "date": {
                "year": 2018,
                "month": 5,
                "day": 25
            },
            "time": {
                "hour": 17,
                "minute": 20
            },
            "content": "HELLO EVERYONE."
        },
        {
            "user": {
                "name": "Ravie",
                "number": 6380,
                "avatar": "https://cdn.discordapp.com/avatars/1/1.png",
                "role": " generic "
            },
            "date": {
                "year": 2018,
                "month": 5,
                "day": 25
            },
            "time": {
                "hour": 17,
                "minute": 25
            },
            "content": [
                {
                    "text":" I like pancakes. Let's see what "
                },
                {
                    "mention": {
                        "name": "jao",
                        "role": "discord-admin"
                    }
                },
                {
                    "text": " likes to eat!\nI bet jao likes it too!"
                }
            ]
        },
        {
            "user": {
                "name": "Ravie",
                "number": 6380,
                "avatar": "https://cdn.discordapp.com/avatars/1/1.png",
                "role": " generic "
            },
            "date": {
                "year": 2018,
                "month": 5,
                "day": 25
            },
            "time": {
                "hour": 17,
                "minute": 26
            },
            "content": [
                {
                    "text": "Oh, here's my map btw. Notice how I didn't give it a "
                },
                {
                    "code": ".png.map"
                },
                {
                    "text": " extension this time! I am so nice."
                }
            ]
        },
        {
            "user": {
                "name": "Ravie",
                "number": 6380,
                "avatar": "https://cdn.discordapp.com/avatars/1/1.png",
                "role": " generic "
            },
            "date": {
                "year": 2018,
                "month": 5,
                "day": 25
            },
            "time": {
                "hour": 17,
                "minute": 26
            },
            "content": {
                "attachment": {
                    "type": "file",
                    "url": "https://cdn.discordapp.com/attachments/1/1/Stellar.map",
                    "basename": "Stellar",
                    "extension": ".map",
                    "filesize": 227,
                    "filesize-units": "KB"
                }
            }
        },
        {
            "user": {
                "name": "jao",
                "number": 3750,
                "avatar": "https://cdn.discordapp.com/avatars/1/1.png",
                "role": " discord-admin "
            },
            "date": {
                "year": 2018,
                "month": 5,
                "day": 25
            },
            "time": {
                "hour": 17,
                "minute": 51
            },
            "content": [
                [
                    {
                        "mention": {
                            "name": "Ravie",
                            "role": "generic"
                        }
                    },
                    {
                        "text": " Wrong, pisshead. "
                    },
                    {
                        "text": {
                            "text": "This",
                            "bold": true
                        }
                    },
                    {
                        "text": " is my favorite food:"
                    }
                ]
            ]
        },
        {
            "user": {
                "name": "jao",
                "number": 3750,
                "avatar": "https://cdn.discordapp.com/avatars/1/1.png",
                "role": " discord-admin "
            },
            "date": {
                "year": 2018,
                "month": 5,
                "day": 25
            },
            "time": {
                "hour": 17,
                "minute": 51
            },
            "content": {
                "attachment": {
                    "type": "image",
                    "url": "https://cdn.discordapp.com/attachments/1/1/poop.png",
                    "basename": "poop",
                    "extension": ".png"
                }
            }
        }
    ]
}
```
