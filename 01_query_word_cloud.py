# %% [python]
from wordcloud import WordCloud, STOPWORDS

import matplotlib.pyplot as plt

from hansken.connect import connect_project

hansken_host = ''
hansken_project = '5ee273fd-0978-4a0a-b8b0-2af2f8479214'

context = connect_project(endpoint=f'http://{hansken_host}:9091/gatekeeper/',
                          project=hansken_project,
                          keystore=f'http://{hansken_host}:9090/keystore/',
                          interactive=True)

# Hansken SDK running on localhost

# context = connect_project(endpoint='http://localhost:9091/gatekeeper/',
#                           project='d42bd9c3-63db-474c-a36f-b87e1eb9e2d3',
#                           keystore='http://localhost:9090/keystore/')

# %% [markdown]
### Collect words
# The cell below searches for all `chatMessage` traces in the current project. The `chatMessage.message` property contains the actual message. All found messages are concatenated in a single long string.

# %% [python]
words = ""
with context.search("type:chatMessage") as search_result:
    for result in search_result:
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

# %%
