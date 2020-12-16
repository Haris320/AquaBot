import discord
import emoji
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import mangadex
import mechanicalsoup
import customFunctions
from customFunctions import genre
import time
from pytmangadex import Mangadex

client = commands.Bot(command_prefix='.')
client.remove_command('help')
browser = mechanicalsoup.Browser()
mangadex = Mangadex()
print("Discord Version: " + discord.__version__)
response = requests.get('https://mangadex.org')
print('API Status Code: ' + str(response.status_code))
client.position = 0


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('.help'))
    print('Bot is ready')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(emoji.emojize(":thinking:" + ' Unknown command. Type .help for a list of commands.'))
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements.')


@client.command()
async def ping(ctx):
    await ctx.send(f'Ping: {round(client.latency * 1000)}ms')


@client.command()
async def dis_ver(ctx):
    await ctx.send("Discord Version: " + discord.__version__)


@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    await ctx.send("TACTICAL NUKE INCOMING")
    time.sleep(1)
    await ctx.channel.purge(limit=10000)
    await ctx.send('https://imgur.com/LIyGeCR')
    await ctx.send(client.user.name + " just nuked the channel")


@client.command()
async def top5(ctx):

    msg = await ctx.send('https://i.gifer.com/ZLnU.gif')
    msg3 = await ctx.send('Fetching Data...')
    try:
        high = mangadex.top_manga()
        embed = discord.Embed(
            title="**Here is a list of the top 5 most followed Manga's currently: **",
            colour=discord.Colour.blue()
        )
        a = []
        for i in range(0, 5):
            a.append(high[str(i)]['title'] + " | Followers:" + high[str(i)]['follow_count'] + " | Rating:" + high[str(i)][
                'star_rating'] + " out of 10" + " | Users:" + high[str(i)]['users'] + ' | https://mangadex.org' +
                     high[str(i)]['thumbnail_link'])
        for i in range(0, 5):
            embed.add_field(name="**Number " + str(i + 1) + ": **", value=a[i], inline=False)
            r = requests.get('https://mangadex.org' + high[str(0)]['thumbnail_link'])
            soup = BeautifulSoup(r.text, 'html.parser')
            results = soup.find_all('div', attrs={'class': 'col-xl-3 col-lg-4 col-md-5'})
            embed.set_thumbnail(url=str(results[0].find('img')['src']))
        await msg.delete()
        await msg3.delete()
        await ctx.send(embed=embed)
    except:
        await msg.delete()
        await msg3.delete()
        await ctx.send("API Status Code 502. Please try again later.")


@client.command()
async def feat(ctx):
    msg = await ctx.send('https://i.gifer.com/ZLnU.gif')
    msg3 = await ctx.send('Fetching Data...')
    try:
        featured = mangadex.featured_titles()
        embed = discord.Embed(
            title="**Here is a list of featured Manga: **",
            colour=discord.Colour.blue()
        )

        a = []
        title = []
        for i in range(0, 5):
            a.append(" Followers: " + featured[str(i)]['follows'] + " | Rating: " +
                     featured[str(i)]['bayesian_rating'] + " out of 10" + ' | Views: ' + featured[str(i)]['views'] +
                     ' | https://mangadex.org' + featured[str(i)]['manga_link'])
        for i in range(0, 5):
            title.append(featured[str(i)]['manga_title'])
            embed.add_field(name=f"{title[i]}:", value=a[i], inline=False)
        r = requests.get('https://mangadex.org' + featured[str(0)]['manga_link'])
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all('div', attrs={'class': 'col-xl-3 col-lg-4 col-md-5'})
        embed.set_thumbnail(url=str(results[0].find('img')['src']))
        await msg.delete()
        await msg3.delete()
        await ctx.send(embed=embed)
    except:
        await msg.delete()
        await msg3.delete()
        await ctx.send('API Status Code 502. Please try again later.')

@client.command()
async def search(ctx, *, term: str):
    msg = await ctx.send('https://i.imgur.com/GdHluBi.gif')
    msg3 = await ctx.send('Searching...')
    try:
        i = 0
        title = []
        link = []
        mangadex.login("Parrota", "QWERTY1234", newLogin=True)
        async for manga in mangadex.search(term, 5):
            title.append(manga.title)
            link.append(f"https://mangadex.org/title/{manga.manga_id}/")
            i += 1
            if i == 10:
                break
        hyperlink = ""
        if i != 0:
            for result in range(0, i):
                hyperlink += f"[{title[result]}]({link[result]})\n"
            embed = discord.Embed(
                title=f"Search results for \"{term}\"",
                description=hyperlink,
                colour=discord.Colour.blue()

            )
            r = requests.get(link[0])
            soup = BeautifulSoup(r.text, 'html.parser')
            results = soup.find_all('div', attrs={'class': 'col-xl-3 col-lg-4 col-md-5'})
            embed.set_thumbnail(url=str(results[0].find('img')['src']))
        if i == 0:
            embed = discord.Embed(
                title=f"No search results for \"{term}\"",
                colour=discord.Colour.blue()
            )
            embed.set_image(url='https://i.kym-cdn.com/photos/images/original/001/223/243/59b.gif')
        await msg.delete()
        await msg3.delete()
        await ctx.send(embed=embed)
    except:
        await msg.delete()
        await msg3.delete()
        await ctx.send('API Status Code 502. Please try again later.')


@client.command()
async def followedmanga(ctx):
    def check(msg):
        return msg.guild is None and msg.author == ctx.message.author

    await ctx.author.send('Enter MangaDex username:')
    username = await client.wait_for('message', timeout=60, check=check)

    await ctx.author.send('Enter MangaDex password:')
    password = await client.wait_for('message', timeout=60, check=check)
    mangadex.login(str(username.content), str(password.content), newLogin=True)
    try:
        hyperlink = ""
        followed = mangadex.user.followed_mangas()
        for i in range(len(followed)):
            hyperlink += f"[{followed[i]['mangaTitle']}](https://mangadex.org/title/{followed[i]['mangaId']})\n"
        embed = discord.Embed(
            title="Here is a list of your followed Manga",
            description=hyperlink,
            colour=discord.Colour.blue()
        )
        r = requests.get(f"https://mangadex.org/title/{followed[0]['mangaId']}/")
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all('div', attrs={'class': 'col-xl-3 col-lg-4 col-md-5'})
        embed.set_thumbnail(url=str(results[0].find('img')['src']))
        await ctx.author.send(embed=embed)
    except:
        await ctx.author.send('Invalid Id')


@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="Help has arrived!",
        colour=discord.Colour.blue()
    )
    embed.add_field(name="--------BOT STATUS--------", value="*.ping* - Display server's latency\n*.dis_ver* - Displays"
                                                             " the current version of Discord\n*.nuke* - Tactical "
                                                             "Nuke (admin required)\n*.clear int* - Clears a certain "
                                                             "number of messages (admin required)"
                    , inline=False)
    embed.add_field(name='--------MANGA COMMANDS--------', value="*.top5* - Displays the top 5 most followed Manga "
                                                                 "series\n*.rec* - Recommends you a manga based off "
                                                                 "a genre of your choice\n*.followedmanga* - Aqua will "
                                                                 "return mangas you follow.\n*.search"
                                                                 " \"str\"* - Type in a key word to search from "
                                                                 "MangaDex\n*.feat* - Displays featured "
                                                                 "manga\n*.wishlist* - Displays your manga wishlist "
                    , inline=False)
    embed.set_image(url='https://i.imgur.com/1rDwKuE.gif')
    await ctx.send(embed=embed)


@client.command()
async def rec(ctx):
    try:
        fal = True
        channel = ctx.channel
        await channel.send('Type in genre you are interested in: Action, adventure, comedy, fantasy, drama,'
                           ' historical, horror, mystery, romance, sci-fi')
        msg = await client.wait_for('message')
        retype = genre(msg.content)
        if retype != 999:
            r = requests.get('https://mangadex.org/genre/' + str(retype))
        else:
            if retype == 999:
                await channel.send('Invalid genre. Please re-enter your preferred genre')

        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all('div', attrs={'class': 'manga-entry col-lg-6 border-bottom pl-0 my-1'})
        a = []
        for i in range(0, 39):
            a.append(results[i])
        await channel.send("React with a ✅ if you like the recommendation or ❌ if you want another one.")
        msg = await channel.send('https://mangadex.org' + str(a[client.position].find('a')['href']))
        reactions = ['✅', '❌']
        for emoji in reactions:
            await msg.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

        while fal:
            reaction, user = await client.wait_for('reaction_add', timeout=80, check=check)
            if reaction.emoji == '✅':
                try:
                    customFunctions.wishlist[str(ctx.author)].append(str(a[client.position].find('a')['href']))
                except:
                    customFunctions.wishlist.update({str(ctx.author): [str(a[client.position].find('a')['href'])]})
                fal = False
                await ctx.send(('Added to your wish list ' + ":wink:" + '.'))
            if reaction.emoji == '❌':
                client.position += 1
                await msg.edit(content='https://mangadex.org' + str(a[client.position].find('a')['href']))
            await msg.remove_reaction(reaction, ctx.author)

        if client.position == 40:
            client.position = 0
    except:
        await ctx.send("API Status code 502. Please try again later.")


@client.command()
async def wishlist(ctx):
    try:
        hyperlink = ''
        for i in range(0, len(customFunctions.wishlist[str(ctx.author)])):
            link = customFunctions.wishlist[str(ctx.author)][i]
            hyperlink += f"[{mangadex.get_manga(link[7:12]).title}](https://mangadex.org/title/{link[7:12]}/)\n"

        embed = discord.Embed(
            title=f"{ctx.author.name}'s wish list:",
            description=hyperlink,
            colour=discord.Colour.blue()

        )
        url = customFunctions.wishlist[str(ctx.author)][0]
        r = requests.get(f"https://mangadex.org/title/{url[7:12]}/")
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all('div', attrs={'class': 'col-xl-3 col-lg-4 col-md-5'})
        embed.set_thumbnail(url=str(results[0].find('img')['src']))
        await ctx.send(embed=embed)
    except:
        await ctx.send("You don't have any thing in your wish list :face_with_raised_eyebrow:. Use `.rec` to add "
                       "Manga to your wish list")


@client.command()
async def test(ctx):
    title = []
    link = []
    mangadex.login("Parrota", "QWERTY1234", newLogin=True)
    async for manga in mangadex.search("darling", 5):
        title.append(manga.title)
        link.append(f"https://mangadex.org/title/{manga.manga_id}/")
    await ctx.send(title[0]+link[0])

client.run('Nzc1NTEyNDU3OTg4MTQ1MTUz.X6naQg.gc0Bz0jaQ8ksNeJzs2LLBzmNY9U')
