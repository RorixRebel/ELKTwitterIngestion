from twython import TwythonStreamer
from models import Tweet, es
from datetime import datetime

CONSUMER_KEY = "V1XCyXScnXDZh232FAIvjSd2e"
CONSUMER_SECRET = "JOB36LqZhd8A6WJ4zmd7ZBy3As2CQhK9uLXonlpaliFJYMhcSv"
AUTH_TOKEN = "43233942-pMGIuekO53ZywjjOe3JVZJoekOLWN5KzIfj1NcvKP"
AUTH_SECRET = "ibXRDGgO4g9WA8buMFvzfyJebA6JkhCN26WMUeGeA"


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        try:
            tweets = Tweet(
                username=data["user"]["screen_name"],
                realname=data["user"]["name"],
                location=data["user"]["location"],            
                tweet_text=data["text"],
                hashtags=data["entities"]["hashtags"],
            )
            tweets.push_to_elastic()
        except KeyError:
            pass        
        

    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()
        return False

    def on_timeout(self, data):
        print("Request timed out, try again later")
        self.disconnect()

def start():
    stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, AUTH_TOKEN, AUTH_SECRET)
    stream.statuses.filter(track=["Trump", "trump"])


if __name__ == "__main__":
    start()
