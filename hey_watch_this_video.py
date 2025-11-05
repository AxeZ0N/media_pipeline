import discord, os, mpv, time, threading
from os.path import isdir as is_locked
from os import mkdir as lock, rmdir as unlock

class AlreadyRunningException(Exception): pass
class NoneTokenException(Exception): pass

class Watcher:
    ''' Responsible for the daemon watching my DMs '''

    CHANNEL_ID = 828429968567435264 # My DMs with Aleah
    TOKEN = os.environ.get('DISCORD_TOKEN', None)
    DOMAINS = ['tiktok', 'instagram',]
    TO_DL = '.to_download'
    LOCKFILE = '.WATCH_LOCK'

    def __init__(self):
        if is_locked(self.LOCKFILE): raise AlreadyRunningException

        self.token = os.environ.get('DISCORD_TOKEN', None)
        if self.token is None: raise NoneTokenException

        lock(self.LOCKFILE)
        self.client = discord.Client()

    def write_to_file(self, msg):
        ''' Append URL to download file '''
        with open(self.TO_DL, 'a') as f:
            f.write(msg + '\n')

    def watch(self):
        ''' Define callback, start client, handle client errors and cleanup '''

        @self.client.event
        async def on_message(message):
            if message.channel.id != self.CHANNEL_ID: return

            content = message.content
            for d in self.DOMAINS:
                if d in content: 
                    print('Writing url')
                    return self.write_to_file(content)

        try: self.client.run(self.token)
        except discord.LoginFailure as e: raise e
        finally: unlock(self.LOCKFILE)

class Player:
    TO_DL = '.to_download'

    def autoplay(self):
        while True:
            with open(self.TO_DL,'r') as f:
                [self.play(url) for url in f]
                with open('.to_download','w'): pass

            time.sleep(1)

    def play(self, url):
        player = mpv.MPV(ytdl=True)
        print('Downloading...')
        player.play(url)
        player.wait_for_playback()
        print('Ended playback')



#watcher = Watcher()
#watcher.watch()

#downloader = Downloader()
#downloader.download()

watcher = Watcher()
watcher_d = threading.Thread(name='Watcher',target=watcher.watch,)
print(f'Started watching!')
watcher_d.start()

player = Player()
print(f'Started autoplay!')
player.autoplay()
watcher_d.join()
