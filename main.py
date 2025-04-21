#updated code (02) on 4/21/25 6:55pm:
import discord
from discord.ext import commands
import os
import requests
from bs4 import BeautifulSoup
from keep_alive import keep_alive

# --- Discord Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot is ready. Logged in as {bot.user}')

@bot.command()
async def test(ctx):
    await ctx.send("Hare Krishna! Bot is alive and responding!")

# --- Merged Verses Dictionary ---
merged_verses = {
    'bg': {
        1: [(16, 18), (21, 22)],
        2: [(5, 6)],
        10: [(21, 22)],
        11: [(15, 30)],
        13: [(13, 14), (15, 18)],
        18: [(13, 14), (16, 17), (27, 28), (53, 54)],
    },
    'sb': {},
    'cc': {}
}

# --- URL Resolution Function ---
def resolve_url(scripture, chapter, verse):
    if scripture in merged_verses and chapter in merged_verses[scripture]:
        for verse_range in merged_verses[scripture][chapter]:
            if verse in range(verse_range[0], verse_range[1] + 1):
                return f'https://vedabase.io/en/library/{scripture}/{chapter}/{verse_range[0]}-{verse_range[1]}/'
    return f'https://vedabase.io/en/library/{scripture}/{chapter}/{verse}/'

# --- Scraper Function ---
def scrape_vedabase_verse(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        devanagari = soup.find('h2', string='Devanagari').find_next('div').text.strip()
        verse_text = soup.find('h2', string='Verse text').find_next('div').text.strip()
        translation = soup.find('h2', string='Translation').find_next('div').text.strip()
        purport = soup.find('h2', string='Purport').find_next('div').text.strip()
        synonyms = soup.find('h2', string='Synonyms').find_next('div').text.strip()

        return {
            'devanagari': devanagari,
            'verse_text': verse_text,
            'translation': translation,
            'purport': purport,
            'synonyms': synonyms
        }
    except requests.RequestException as e:
        return f"Error fetching the webpage: {e}"
    except AttributeError as e:
        return f"Error parsing the content: {e}"

# --- Embed Sending Function ---
async def send_verse_embed(ctx, scripture_name, verse_number, content, color):
    if isinstance(content, dict):
        embed = discord.Embed(title=f"{scripture_name} {verse_number}", color=color)
        for label, text in content.items():
            if text:
                for i in range(0, len(text), 1024):
                    embed.add_field(
                        name=label.capitalize() if i == 0 else f"{label.capitalize()} (cont'd)",
                        value=text[i:i + 1024],
                        inline=False
                    )
        await ctx.send(embed=embed)
    else:
        await ctx.send(content)

# --- Verse Commands ---
@bot.command(name='bg')
async def fetch_bg_verse(ctx, verse_number: str):
    try:
        chapter, verse = map(int, verse_number.split("."))
        url = resolve_url('bg', chapter, verse)
        verse_content = scrape_vedabase_verse(url)
        await send_verse_embed(ctx, "Bhagavad Gita", verse_number, verse_content, discord.Color.purple())
    except ValueError:
        await ctx.send("Please enter a valid verse format like 2.13")

@bot.command(name='sb')
async def fetch_sb_verse(ctx, verse_number: str):
    try:
        chapter, verse = map(int, verse_number.split("."))
        url = resolve_url('sb', chapter, verse)
        verse_content = scrape_vedabase_verse(url)
        await send_verse_embed(ctx, "Śrīmad Bhāgavatam", verse_number, verse_content, discord.Color.blue())
    except ValueError:
        await ctx.send("Please enter a valid verse format like 2.13")

@bot.command(name='cc')
async def fetch_cc_verse(ctx, verse_number: str):
    try:
        chapter, verse = map(int, verse_number.split("."))
        url = resolve_url('cc', chapter, verse)
        verse_content = scrape_vedabase_verse(url)
        await send_verse_embed(ctx, "Chaitanya Charitāmṛta", verse_number, verse_content, discord.Color.green())
    except ValueError:
        await ctx.send("Please enter a valid verse format like 2.13")

# --- Run Everything ---
keep_alive()
bot.run(os.environ['DISCORD_TOKEN'])


# updated code on 4/21/25 6:38pm :

# import discord
# from discord.ext import commands
# import os
# import requests
# from bs4 import BeautifulSoup
# from keep_alive import keep_alive


# # --- Discord Bot Setup ---
# intents = discord.Intents.default()
# intents.message_content = True
# bot = commands.Bot(command_prefix='!', intents=intents)


# @bot.event
# async def on_ready():
#     print(f'✅ Bot is ready. Logged in as {bot.user}')


# @bot.command()
# async def test(ctx):
#     await ctx.send("Hare Krishna! Bot is alive and responding!")


# # --- Merged Verses Logic ---
# merged_verses = {
#     'bg': {
#         1: [(16, 18), (21, 22)],
#         2: [(5, 6)],
#         # Add more merged verses as needed
#     },
#     'sb': {},
#     'cc': {}
# }

# # --- URL Resolution Function ---
# def resolve_url(scripture, chapter, verse):
#     """
#     Resolves the correct URL for a verse, including merged verses.
#     """
#     # Check if merged verses exist for the scripture and chapter
#     if scripture in merged_verses and chapter in merged_verses[scripture]:
#         for verse_range in merged_verses[scripture][chapter]:
#             if verse in range(verse_range[0], verse_range[1] + 1):
#                 # For merged verses, return a URL that includes both verses
#                 return f'https://vedabase.io/en/library/{scripture}/{chapter}/{verse_range[0]}-{verse_range[1]}/'
    
#     # Return URL for a single verse if not a merged range
#     return f'https://vedabase.io/en/library/{scripture}/{chapter}/{verse}/'


# # --- Scraper Function ---
# def scrape_vedabase_verse(url):
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Scrape the required data from the page
#         devanagari = soup.find('h2', string='Devanagari').find_next('div').text.strip()
#         verse_text = soup.find('h2', string='Verse text').find_next('div').text.strip()
#         translation = soup.find('h2', string='Translation').find_next('div').text.strip()
#         purport = soup.find('h2', string='Purport').find_next('div').text.strip()
#         synonyms = soup.find('h2', string='Synonyms').find_next('div').text.strip()

#         return {
#             'devanagari': devanagari,
#             'verse_text': verse_text,
#             'translation': translation,
#             'purport': purport,
#             'synonyms': synonyms
#         }
#     except requests.RequestException as e:
#         return f"Error fetching the webpage: {e}"
#     except AttributeError as e:
#         return f"Error parsing the content: {e}"


# # --- Embed Sending Function ---
# async def send_verse_embed(ctx, scripture_name, verse_number, content, color):
#     if isinstance(content, dict):
#         embed = discord.Embed(title=f"{scripture_name} {verse_number}", color=color)
#         for label, text in content.items():
#             if text:
#                 for i in range(0, len(text), 1024):
#                     embed.add_field(name=label.capitalize() if i == 0 else f"{label.capitalize()} (cont'd)", value=text[i:i + 1024], inline=False)
#         await ctx.send(embed=embed)
#     else:
#         await ctx.send(content)


# # --- Verse Commands ---
# @bot.command(name='bg')
# async def fetch_bg_verse(ctx, verse_number: str):
#     try:
#         chapter, verse = map(int, verse_number.split("."))
#         url = resolve_url('bg', chapter, verse)
#         verse_content = scrape_vedabase_verse(url)
#         await send_verse_embed(ctx, "Bhagavad Gita", verse_number, verse_content, discord.Color.purple())
#     except ValueError:
#         await ctx.send("Please enter a valid verse format like 2.13")


# @bot.command(name='sb')
# async def fetch_sb_verse(ctx, verse_number: str):
#     try:
#         chapter, verse = map(int, verse_number.split("."))
#         url = resolve_url('sb', chapter, verse)
#         verse_content = scrape_vedabase_verse(url)
#         await send_verse_embed(ctx, "Śrīmad Bhāgavatam", verse_number, verse_content, discord.Color.blue())
#     except ValueError:
#         await ctx.send("Please enter a valid verse format like 2.13")


# @bot.command(name='cc')
# async def fetch_cc_verse(ctx, verse_number: str):
#     try:
#         chapter, verse = map(int, verse_number.split("."))
#         url = resolve_url('cc', chapter, verse)
#         verse_content = scrape_vedabase_verse(url)
#         await send_verse_embed(ctx, "Chaitanya Charitāmṛta", verse_number, verse_content, discord.Color.green())
#     except ValueError:
#         await ctx.send("Please enter a valid verse format like 2.13")


# # --- Run Everything ---
# keep_alive()
# bot.run(os.environ['DISCORD_TOKEN'])  # Discord token will be accessed from Replit Secrets



# updated code:

# import discord
# from discord.ext import commands
# import os
# import requests
# from bs4 import BeautifulSoup
# from keep_alive import keep_alive


# # --- Discord Bot Setup ---
# intents = discord.Intents.default()
# intents.message_content = True
# bot = commands.Bot(command_prefix='!', intents=intents)


# @bot.event
# async def on_ready():
#     print(f'✅ Bot is ready. Logged in as {bot.user}')


# @bot.command()
# async def test(ctx):
#     await ctx.send("Hare Krishna! Bot is alive and responding!")


# # --- Merged Verses Logic ---
# merged_verses = {
#     'bg': {
#         1: [(16, 18), (21, 22)],
#         2: [(5, 6)],
#         # Add more merged verses as needed
#     },
#     'sb': {},
#     'cc': {}
# }

# # --- URL Resolution Function ---
# def resolve_url(scripture, chapter, verse):
#     """
#     Resolves the correct URL for a verse, including merged verses.
#     """
#     if scripture in merged_verses and chapter in merged_verses[scripture]:
#         for verse_range in merged_verses[scripture][chapter]:
#             if verse in range(verse_range[0], verse_range[1] + 1):
#                 # For merged verses, return a URL that includes both verses
#                 return f'https://vedabase.io/en/library/{scripture}/{chapter}/{verse_range[0]}-{verse_range[1]}/'
#     return f'https://vedabase.io/en/library/{scripture}/{chapter}/{verse}/'


# # --- Scraper Function ---
# def scrape_vedabase_verse(url):
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')

#         devanagari = soup.find('h2', string='Devanagari').find_next('div').text.strip()
#         verse_text = soup.find('h2', string='Verse text').find_next('div').text.strip()
#         translation = soup.find('h2', string='Translation').find_next('div').text.strip()
#         purport = soup.find('h2', string='Purport').find_next('div').text.strip()
#         synonyms = soup.find('h2', string='Synonyms').find_next('div').text.strip()

#         return {
#             'devanagari': devanagari,
#             'verse_text': verse_text,
#             'translation': translation,
#             'purport': purport,
#             'synonyms': synonyms
#         }
#     except requests.RequestException as e:
#         return f"Error fetching the webpage: {e}"
#     except AttributeError as e:
#         return f"Error parsing the content: {e}"


# # --- Embed Sending Function ---
# async def send_verse_embed(ctx, scripture_name, verse_number, content, color):
#     if isinstance(content, dict):
#         embed = discord.Embed(title=f"{scripture_name} {verse_number}", color=color)
#         for label, text in content.items():
#             if text:
#                 for i in range(0, len(text), 1024):
#                     embed.add_field(name=label.capitalize() if i == 0 else f"{label.capitalize()} (cont'd)", value=text[i:i + 1024], inline=False)
#         await ctx.send(embed=embed)
#     else:
#         await ctx.send(content)


# # --- Verse Commands ---
# @bot.command(name='bg')
# async def fetch_bg_verse(ctx, verse_number: str):
#     try:
#         chapter, verse = map(int, verse_number.split("."))
#         url = resolve_url('bg', chapter, verse)
#         verse_content = scrape_vedabase_verse(url)
#         await send_verse_embed(ctx, "Bhagavad Gita", verse_number, verse_content, discord.Color.purple())
#     except ValueError:
#         await ctx.send("Please enter a valid verse format like 2.13")


# @bot.command(name='sb')
# async def fetch_sb_verse(ctx, verse_number: str):
#     try:
#         chapter, verse = map(int, verse_number.split("."))
#         url = resolve_url('sb', chapter, verse)
#         verse_content = scrape_vedabase_verse(url)
#         await send_verse_embed(ctx, "Śrīmad Bhāgavatam", verse_number, verse_content, discord.Color.blue())
#     except ValueError:
#         await ctx.send("Please enter a valid verse format like 2.13")


# @bot.command(name='cc')
# async def fetch_cc_verse(ctx, verse_number: str):
#     try:
#         chapter, verse = map(int, verse_number.split("."))
#         url = resolve_url('cc', chapter, verse)
#         verse_content = scrape_vedabase_verse(url)
#         await send_verse_embed(ctx, "Chaitanya Charitāmṛta", verse_number, verse_content, discord.Color.green())
#     except ValueError:
#         await ctx.send("Please enter a valid verse format like 2.13")


# # --- Run Everything ---
# keep_alive()
# bot.run(os.environ['DISCORD_TOKEN'])  # Discord token will be accessed from Replit Secrets



#original code down here :


# import discord
# from discord.ext import commands
# import os
# import requests
# from bs4 import BeautifulSoup
# from keep_alive import keep_alive


# # --- Discord Bot Setup ---
# intents = discord.Intents.default()
# intents.message_content = True
# bot = commands.Bot(command_prefix='!', intents=intents)


# @bot.event
# async def on_ready():
#     print(f'✅ Bot is ready. Logged in as {bot.user}')


# @bot.command()
# async def test(ctx):
#     await ctx.send("Hare Krishna! Bot is alive and responding!")


# # --- Scraper Function ---
# def scrape_vedabase_verse(url):
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')

#         devanagari = soup.find(
#             'h2', string='Devanagari').find_next('div').text.strip()
#         verse_text = soup.find(
#             'h2', string='Verse text').find_next('div').text.strip()
#         translation = soup.find(
#             'h2', string='Translation').find_next('div').text.strip()
#         purport = soup.find('h2',
#                             string='Purport').find_next('div').text.strip()
#         synonyms = soup.find('h2',
#                              string='Synonyms').find_next('div').text.strip()

#         return {
#             'devanagari': devanagari,
#             'verse_text': verse_text,
#             'translation': translation,
#             'purport': purport,
#             'synonyms': synonyms
#         }
#     except requests.RequestException as e:
#         return f"Error fetching the webpage: {e}"
#     except AttributeError as e:
#         return f"Error parsing the content: {e}"


# # --- Embed Sending Function ---
# async def send_verse_embed(ctx, scripture_name, verse_number, content, color):
#     if isinstance(content, dict):
#         embed = discord.Embed(title=f"{scripture_name} {verse_number}",
#                               color=color)
#         for label, text in content.items():
#             if text:
#                 for i in range(0, len(text), 1024):
#                     embed.add_field(name=label.capitalize() if i == 0 else
#                                     f"{label.capitalize()} (cont'd)",
#                                     value=text[i:i + 1024],
#                                     inline=False)
#         await ctx.send(embed=embed)
#     else:
#         await ctx.send(content)


# # --- Verse Commands ---
# @bot.command(name='bg')
# async def fetch_bg_verse(ctx, verse_number: str):
#     url = f'https://vedabase.io/en/library/bg/{verse_number.replace(".", "/")}/'
#     verse_content = scrape_vedabase_verse(url)
#     await send_verse_embed(ctx, "Bhagavad Gita", verse_number, verse_content,
#                            discord.Color.purple())


# @bot.command(name='sb')
# async def fetch_sb_verse(ctx, verse_number: str):
#     url = f'https://vedabase.io/en/library/sb/{verse_number.replace(".", "/")}/'
#     verse_content = scrape_vedabase_verse(url)
#     await send_verse_embed(ctx, "Śrīmad Bhāgavatam", verse_number,
#                            verse_content, discord.Color.blue())


# @bot.command(name='cc')
# async def fetch_cc_verse(ctx, verse_number: str):
#     url = f'https://vedabase.io/en/library/cc/{verse_number.replace(".", "/")}/'
#     verse_content = scrape_vedabase_verse(url)
#     await send_verse_embed(ctx, "Chaitanya Charitāmṛta", verse_number,
#                            verse_content, discord.Color.green())


# # --- Run Everything ---
# keep_alive()
# bot.run(os.environ['DISCORD_TOKEN']
#         )  # Discord token will be accessed from Replit Secrets

# # This is a test change to track updates

