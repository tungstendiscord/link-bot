import discord
from discord.ext import commands
import requests, json

class Dictionary(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.guild_only()
    async def dictionary(self, ctx, *, args):
        if " " not in args:
            await ctx.send("Must send more than one argument!")
        args = args.split(" ")
        func = args[0]
        args = args[1:]
        if func == "search":
            r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{''.join(args)}")
            
            try:
                word = json.loads(r.content)[0]
                e = discord.Embed(
                    title=word["word"],
                    color=0x008080
                )
                
                s = ""
                for pronunciation in word["phonetics"]:
                    s += pronunciation["text"] + ", "
                s = s[:-2]
                e.add_field(
                    name="Pronunciation",
                    value=s
                )
                s = ""
                for _ in word["meanings"]:
                    if _["partOfSpeech"][0] in "aeiou":
                        s += "As an " + _["partOfSpeech"] + ": "
                    else:
                        s += "As a " + _["partOfSpeech"] + ": "
                    for defs in _["definitions"]:
                        try:
                            example = defs["example"]
                            temp = example[0].upper() + example[1:]
                            example = temp
                            if example[-1] not in "?!.":
                                example += "."
                            s += defs["definition"] + "\nFor example: " + example + "\n"
                        except:
                            pass
                        try:
                            for synonym in defs["synonyms"]:
                                s += synonym + ", "
                            s = s[:-2]
                            s += "\n\n"
                        except:
                            s += "\n\n"
                    s += "\n"
                e.add_field(
                    name="Definition",
                    value=s
                )
                await ctx.send(embed=e)
            except:
                await ctx.send(f"Sorry, could not find {' '.join(args)} :sob:")
        elif func == "synonyms":
            r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{''.join(args)}")
            word = json.loads(r.content)[0]
            s = ""
            for _ in word["meanings"]:
                for defs in _["definitions"]:
                    try:
                        for synonym in defs["synonyms"]:
                            s += synonym + ", "
                        s = s[:-2]
                    except:
                        s = "Sorry, no synonyms found :sob:"
            e = discord.Embed(
                title=f"Synonyms of {word['word'][0].upper() + word['word'][1:]}",
                description=s,
                color=0x008080
            )
            await ctx.send(embed=e)



def setup(client):
    client.add_cog(Dictionary(client))
