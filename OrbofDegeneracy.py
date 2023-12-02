import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/',intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Command to add a new row to Google Spreadsheet
@bot.command(name='newbet', brief='\\newbet sport wager odds details [result]')
async def new_bet(ctx, *args):
    # Validate arguments
    if len(args) not in [4,5]:
        await ctx.send('Enter between 4 and 5 arguments. Make sure to enclose bet description in double quotations')
        return
    # 

    # Google Sheets API setup
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/bgram/OneDrive/Documents/Programming Projects/Python/bet-tracker-406017-e3cf07acce59.json', scope)
    client = gspread.authorize(creds)

    # Open the Google Spreadsheet using its title
    spreadsheet = client.open('Bet Tracker')

    # Select the specific worksheet within the spreadsheet
    worksheet = spreadsheet.get_worksheet(0)  # Change the index if needed

    # Get user info
    user = ctx.author.display_name
    args = (user,) + args

    # Get bet submission date and offset id column
    submission_date = ctx.message.created_at.isoformat()
    args = (submission_date,) + args

    # Retrieve the id of the last added row
    id = len(worksheet.get_all_values()) 
    args = (id,) + args

    # Add a new row with the data provided in the command
    worksheet.append_row(args)

    await ctx.send(f'Good luck {user}! Bet id: {id}')

# Command to update win result
@bot.command(name='updatebet', brief='\\updatebet id result')
async def update_bet(ctx, *args):
    # Validate arguments
    if len(args) != 2:
        await ctx.send('Invalid arguments entered. Try again: \\updatebet id result')
        return
    #
    id = int(args[0])
    result = args[1]

    # Google Sheets API setup
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/bgram/OneDrive/Documents/Programming Projects/Python/bet-tracker-406017-e3cf07acce59.json', scope)
    client = gspread.authorize(creds)

    # Open the Google Spreadsheet using its title
    spreadsheet = client.open('Bet Tracker')

    # Select the specific worksheet within the spreadsheet
    worksheet = spreadsheet.get_worksheet(0)  # Change the index if needed

    # Find row with id = id, overwrite result with result
    row_values = worksheet.row_values(id + 1)

    # Update Cell
    worksheet.update_cell(id+1,8,result)

    await ctx.send(f'Bet {row_values[6]} result updated to {result}')

# Command to check last n bets, optionally for a specified username
@bot.command(name='checkbet', brief='\\checkbet n [username]')
async def check_bet(ctx, *args):
    # Validate arguments
    if len(args) not in [1,2] | ~args[0].isdigit():
        await ctx.send('Invalid arguments entered. Try again: \\checkbet n [username]')
        return
    #
    n = int(args[0])

    # Google Sheets API setup
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/bgram/OneDrive/Documents/Programming Projects/Python/bet-tracker-406017-e3cf07acce59.json', scope)
    client = gspread.authorize(creds)

    # Open the Google Spreadsheet using its title
    spreadsheet = client.open('Bet Tracker')

    # Select the specific worksheet within the spreadsheet
    worksheet = spreadsheet.get_worksheet(0)  # Change the index if needed

    # Validate username
    if len(args)==2:
        # Get all unique values of username
        username_values = set(worksheet.col_values(3))
        # Test if username is in the worksheet
        if args[1] not in username_values:
            await ctx.send('Username not found in worksheet. Try again: \\checkbet n [username]')
            return
        # Query spreadsheet
        cell = worksheet.findall(args[1],in_column=3)
        if(len(cell)==0):
            await ctx.send('No records found')
            return
        if(n > len(cell)):
            n = len(cell)
        cell = cell[-n:]
        rows = [o.row for o in cell]
        print(rows)
        for r in rows:
            bet_string = ', '.join(worksheet.row_values(r)[0:8])
            await ctx.send(bet_string)
    else:
        # Query spreadsheet
        lastrow = len(worksheet.get_all_values()) 
        if lastrow == 0:
            await ctx.send('No records found')
            return
        if n > (lastrow-1):
            n = lastrow-1
        rows =  range(lastrow-n+1,lastrow+1)
        for r in rows:
            bet_string = ', '.join(worksheet.row_values(r)[0:8])
            await ctx.send(bet_string)

# Add username 

# Run the bot
bot.run('MTE3NzI5MzQyNDg4MjM1MjE2OA.GTNFJn.do4ytgMBfu2zqw4JS_9FNlnBWucnh7f289ohJE')
