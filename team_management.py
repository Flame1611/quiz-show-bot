class Teams():
    def __init__(self) -> None:
        self.teams:dict = {}
        self.host_server:int = None
        self.admins:list[int] = [1,2,3]
    
    def add_team(self,name: str = None, members: list = [], id: int = 0) -> str:
        existing = self.teams.get(name,False)
        if not existing and members and id != self.host_server:
            if not name:
                name = f"Team {len(self.teams) + 1}"
            self.teams[id] = team(name= name, members= members)
            return f'Team \"{self.teams[id].name}\" created successfully!'
        elif id == self.host_server:
            return 'This is the host server, unable to make team server'
        elif existing:
            return 'This is aready a team server!'
        

    def remove_team(self, index: int = None) -> str:
        name = self.teams.get(index,False)
        if name:
            name = name.name
            self.teams.pop(index)
            return (f'Successfully removed the team "{name}"')

    # def remove_admin(self, id: int = None) -> str:
    #     name = self.teams.index
    #     self.teams.pop(index)
        
    def set_host(self,id:int = 0) -> str:
        self.host_server = id

    def set_captain(self, id:int = 0) -> str:
        for team in self.teams:
            if id in self.teams[team].members:
                captains_team = id
                old_id = team
                break
        else:
            return f'<@{id}> is not in a team'
        self.teams[captains_team] = self.teams[old_id]
        self.teams[captains_team].captain = captains_team
        self.teams.pop(old_id)
        return f'Successfully set <@{id}> as team captain'
    
    def add_points(self,score:int , captain_id:int = 0) -> int:
        for team_id in self.teams:
            if team_id == captain_id:
                self.teams[captain_id].score += score
                return('Points added')
        return('Player not captain')

class team():
    def __init__(self, name: str = "Unnamed team", members: list[int] = []) -> None:
        self.name: str = name  # The name of the team, Each team will be in a server of the same name
        self.score: int = 0 # The score of the team
        self.members:list[int] = members # The members of the team easiest way of setting it up is to take from the server
        self.captain: int = None # The captain of the team, elected between the members earlier in the day. Used as index as they answer the questions

if __name__ == "__main__":
    
    #  # Runs bot for testing
    import os
    from dotenv import load_dotenv
    import discord
    from discord.ext import commands
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    intents = discord.Intents.all()
    bot = commands.Bot(intents=intents, command_prefix="!")
    
    @bot.event
    async def on_ready():
        assert bot.user is not None
        print(bot.user.name, "has connected to discord")
    players = Teams()
    
    @bot.hybrid_command(name="create-host-server")
    async def host_server(ctx):
        players.set_host(ctx.message.guild.id)

    @bot.hybrid_command(name="become_captain")
    async def set_captain(ctx):    
        await ctx.send(players.set_captain(ctx.message.author.id))

    @bot.hybrid_command(name="add_points")
    async def win_points(ctx):    
        result = players.add_points(captain_id= ctx.message.author.id, score= 100)
        await ctx.send(result)

    @bot.hybrid_command(name="view_team_info")
    async def team_info(ctx):
        await ctx.send(f'<@{players.host_server}>')
        for i in players.teams:
            await ctx.send(f'''Team id: {i}
Team name: {players.teams[i].name}
Team captain: <@{players.teams[i].captain}>
Team score: {players.teams[i].score}
Team members:''')
            for j in players.teams[i].members:
                await ctx.send(f'-  <@{j}>')

    @bot.hybrid_command(name="create-team-server")
    async def team_server(ctx):
        await ctx.send(
        players.add_team(name= ctx.message.guild.name, 
                        members= [user.id for user in ctx.message.guild.members if not user.bot and user.id not in players.admins], 
                        id= ctx.message.guild.id)
        )
    bot.run(TOKEN)
