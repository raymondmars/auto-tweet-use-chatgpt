import os
import twitter

if __name__ == "__main__":
  username = os.environ.get("TWITTER_USER_NAME")
  password = os.environ.get("TWITTER_PASSWORD")
  titter = twitter.Titter(username, password)
  titter.send_tweet('hello,world.')
