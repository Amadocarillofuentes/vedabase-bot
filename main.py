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


# --- Scraper Function ---
def scrape_vedabase_verse(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        devanagari = soup.find(
            'h2', string='Devanagari').find_next('div').text.strip()
        verse_text = soup.find(
            'h2', string='Verse text').find_next('div').text.strip()
        translation = soup.find(
            'h2', string='Translation').find_next('div').text.strip()
        purport = soup.find('h2',
                            string='Purport').find_next('div').text.strip()
        synonyms = soup.find('h2',
                             string='Synonyms').find_next('div').text.strip()

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
        embed = discord.Embed(title=f"{scripture_name} {verse_number}",
                              color=color)
        for label, text in content.items():
            if text:
                for i in range(0, len(text), 1024):
                    embed.add_field(name=label.capitalize() if i == 0 else
                                    f"{label.capitalize()} (cont'd)",
                                    value=text[i:i + 1024],
                                    inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(content)


# --- Verse Commands ---
@bot.command(name='bg')
async def fetch_bg_verse(ctx, verse_number: str):
    url = f'https://vedabase.io/en/library/bg/{verse_number.replace(".", "/")}/'
    verse_content = scrape_vedabase_verse(url)
    await send_verse_embed(ctx, "Bhagavad Gita", verse_number, verse_content,
                           discord.Color.purple())


@bot.command(name='sb')
async def fetch_sb_verse(ctx, verse_number: str):
    url = f'https://vedabase.io/en/library/sb/{verse_number.replace(".", "/")}/'
    verse_content = scrape_vedabase_verse(url)
    await send_verse_embed(ctx, "Śrīmad Bhāgavatam", verse_number,
                           verse_content, discord.Color.blue())


@bot.command(name='cc')
async def fetch_cc_verse(ctx, verse_number: str):
    url = f'https://vedabase.io/en/library/cc/{verse_number.replace(".", "/")}/'
    verse_content = scrape_vedabase_verse(url)
    await send_verse_embed(ctx, "Chaitanya Charitāmṛta", verse_number,
                           verse_content, discord.Color.green())


# --- Run Everything ---
keep_alive()
bot.run(os.environ['DISCORD_TOKEN']
        )  # Discord token will be accessed from Replit Secrets
