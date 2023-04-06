# %% [python]
import sys
from wordcloud import WordCloud, STOPWORDS
from types import SimpleNamespace

import matplotlib.pyplot as plt

from hansken.connect import connect_project

# setup hansken connection
in_browser = 'js' in sys.modules
hansken_host = ''
context = connect_project(endpoint=f'http://{hansken_host}:9091/gatekeeper/',
                          project='5ee273fd-0978-4a0a-b8b0-2af2f8479214',
                          keystore=f'http://{hansken_host}:9091/keystore/',
                          # Authentication is faked if we run in the browser,
                          # because an authenticated session should already be present
                          auth=SimpleNamespace() if in_browser else None,
                          interactive=True)
                          
# %% [markdown]
### Collect words
# The cell below searches for all `chatMessage` traces in the current project. The `chatMessage.message` property contains the actual message. All found messages are concatenated in a single long string.
# %% [python]
words = ""
with context.search("type:chatMessage") as searchResult:
  for result in searchResult:
    message = result.get("chatMessage.message")
    if message is not None:
      words += " " + message
words
# %% [markdown]
### Draw Wordcloud
# The cell below draws a wordcloud using the words occurring in the messages. `STOPWORDS` is used to ignore common english words.
# %% [python]
# draw word cloud
wc = WordCloud(stopwords=STOPWORDS, width=600, height=400).generate(words)
plt.figure(figsize=(20, 6))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()
