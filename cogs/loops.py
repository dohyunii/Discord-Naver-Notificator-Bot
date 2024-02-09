from discord.ext import commands, tasks
import datetime


KST = datetime.timezone(datetime.timedelta(hours=9))
times = [datetime.time(hour=22, minute=50, tzinfo=KST), datetime.time(hour=22, minute=55, tzinfo=KST), datetime.time(hour=23, minute=0, tzinfo=KST)]


class Loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check.start()

    @tasks.loop(time=times)
    async def check(self):
        import json
        from logic import find_last
        from datetime import datetime, timedelta
        tomorrow = (datetime.now() + timedelta(1)).strftime('%A')
        weekdays_link = dict()
        with open("weekdays_link.txt", "r") as data:
            weekdays_link = json.load(data)
        link_title_episode = dict()
        with open("link_title_episode.txt", "r") as data:
            link_title_episode = json.load(data)
        link_channel = dict()
        with open("link_channel.txt", "r") as data:
            link_channel = json.load(data)
        for i in weekdays_link[tomorrow]:
            last_episode = find_last(i)
            if last_episode == "":
                continue
            if link_title_episode[i][1] != last_episode:
                title = link_title_episode[i][0]
                link_title_episode[i][1] = last_episode
                for j in link_channel[i]:
                    channel = self.bot.get_channel(j)
                    await channel.send(f"New episode from {title} is out!\n{last_episode}")
        with open("link_title_episode.txt", "w") as data:
            json.dump(link_title_episode, data)


async def setup(bot):
    await bot.add_cog(Loop(bot))