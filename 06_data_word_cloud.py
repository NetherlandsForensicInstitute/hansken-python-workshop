# %% [python]
import io
from wordcloud import WordCloud, STOPWORDS

import matplotlib.pyplot as plt

from hansken.connect import connect_project

hansken_host = ''
hansken_project = '9f415f8c-c6d0-4341-bcdf-f86db5353471'

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
# The cell below searches for all `document` traces in the current project. Most documents contain a 'text' data stream which contains text extracted from the document.
# If this data is available, the words are added to the wordcloud.

# %% [python]
words = ""
with context.search("type:document") as search_result:
    for trace in search_result:
        # verify text data stream is available
        if "text" in trace.data_types:
            with io.TextIOWrapper(trace.open(stream='text'), encoding="utf-8", errors="ignore") as content:
                words += content.read()
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
