# %% [python]
import io
import sys
from wordcloud import WordCloud, STOPWORDS
from types import SimpleNamespace

import matplotlib.pyplot as plt

from hansken.connect import connect_project

# setup hansken connection
in_browser = 'js' in sys.modules

hansken_host = ''
hansken_project = '5ee273fd-0978-4a0a-b8b0-2af2f8479214'

context = connect_project(endpoint=f'http://{hansken_host}:9091/gatekeeper/',
                          project=hansken_project,
                          keystore=f'http://{hansken_host}:9090/keystore/',
                          # Authentication is faked if we run in the browser,
                          # because an authenticated session should already be present
                          auth=SimpleNamespace() if in_browser else None,
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
        if "text" in trace.data_types:
            with io.TextIOWrapper(trace.open(stream='text')) as content:
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
