from . import feed, get, db, output, verbose, dbmysql

class Favorites:
    def __init__(self, config):
        self.init = -1
        self.feed = [-1]
        self.count = 0
        self.config = config
        if config.hostname:
            self.conn = dbmysql.Conn(config.hostname, config.Database, config.DB_user, config.DB_pwd)
        else:
            self.conn = db.Conn(config.Database)
        self.config.Favorites = True
        
        verbose.Elastic(config)

    async def Feed(self):
        response = await get.RequestUrl(self.config, self.init)
        self.feed = []
        try:
            self.feed, self.init = feed.Mobile(response)
        except:
            pass

    async def main(self):
        if self.config.User_id is not None:
            self.config.Username = await get.Username(self.config.User_id)
        
        while True:
            if len(self.feed) > 0:
                await self.Feed()
                self.count += await get.Multi(self.feed, self.config, self.conn)
            else:
                break
            
            if get.Limit(self.config.Limit, self.count):
                break
        
        verbose.Count(self.config, self.count)
