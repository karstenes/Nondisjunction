import discord
import isodate
import re
import logging
from googleapiclient.discovery import build


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='/logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


vsearch = []
apikey = 'MzIxMzM4NDQ1ODYxNDg2NTky.DBclTA.NbxGmWj0CcYxI6e1F7n8XEv67rw'
client = discord.Client()
DEVELOPER_KEY = "AIzaSyARhlZ59COWmLaEejRpl2ArsvAompbuJFk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(q, results=5):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=q,
        part="id,snippet",
        order="relevance",
        maxResults=results
    ).execute()

    videos = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            sr = youtube.videos().list(
                part="contentDetails, snippet",
                id=search_result["id"]["videoId"]
            ).execute()
            video = sr["items"][0]
            videos.append([video["snippet"]["title"], str(isodate.parse_duration(video["contentDetails"]["duration"])),
                           search_result["id"]["videoId"]])
    return videos


print(youtube_search("test"))


def urltest(string):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if regex.fullmatch(string):
        return True
    else:
        return False


@client.event
async def on_ready():
    print("Ready")
    print("https://discordapp.com/oauth2/authorize?client_id=" + client.user.id + "&scope=bot&permissions=2146958591")


# noinspection PyGlobalUndefined,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
@client.event
async def on_message(message):
    if message.content.startswith("//"):
        client.delete_message(message)
        command = message.content.split(" ")[0][2:]
        args = message.content.split(" ")[1:]
        print(command)
        if command == "ping":
            await client.send_message(message.channel, message.author.mention + ' pong')
        elif command == "play":
            if urltest(args[0]):
                pass
            else:
                if vsearch:
                    if len("".join(args)) == 1:
                        try:
                            vno = int(args[0])
                            global ytplayer
                            ytplayer = await voiceclient.create_ytdl_player("https://www.youtube.com/watch?v=%s"%vsearch[vno])
                        except TypeError:
                            print("Single character, not selection of video")
                else:
                    embed = discord.Embed(title="Youtube Search", description="Select using `//play n`", color=0xe52d27)
                    embed.set_author(name=message.author.name,
                                     icon_url=message.author.avatar_url)
                    embed.set_thumbnail(url='https://www.youtube.com/yt/brand/media/image/YouTube-icon-full_color.png')
                    if args[0].startswith("r="):
                        results = int(args[0][2:])
                        embed.set_footer(text="Searched for \"" + " ".join(args[1:]) + "\"")
                        search = youtube_search(" ".join(args[1:]), results=results)
                    else:
                        embed.set_footer(text="Searched for \"" + " ".join(args) + "\"")
                        search = youtube_search(" ".join(args))
                    vsearch.append(message.author.id)
                    for video in search:
                        vsearch.append(video)
                        embed.add_field(name=str(search.index(video) + 1), value="%s (%s)" % (video[0], video[1]))
                    print(vsearch)
                    await client.send_message(message.channel, embed=embed)
                if not client.is_voice_connected(message.server):
                    global voiceclient
                    voiceclient = await client.join_voice_channel(message.author.voice.voice_channel)
        elif command == "stop":
            if client.is_voice_connected(message.server):
                voiceclient.disconnect()
    else:
        pass


client.run("MzIxMzM4NDQ1ODYxNDg2NTky.DBcgitsFA.tTub_MC96w4mfM2j8_WiZTCR9R0")