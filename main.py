import os
import twitter
import time
from content_provider import ContentProvider
# download chromedriver from https://chromedriver.chromium.org/downloads or https://googlechromelabs.github.io/chrome-for-testing/
# and put it in the same directory as this file.
# and set PATH environment variable to the directory.
# e.g. export PATH=$PATH:/path/to/chromedriver

if __name__ == "__main__":
  username = os.environ.get("TWITTER_USER_NAME")
  password = os.environ.get("TWITTER_PASSWORD")
  titter = twitter.Titter(username, password)
  provider = ContentProvider()
  ai_words = provider.get_content("Tell a joke about electric cars.")
  print(ai_words)
  titter.send_tweet(ai_words)
  time.sleep(5)
