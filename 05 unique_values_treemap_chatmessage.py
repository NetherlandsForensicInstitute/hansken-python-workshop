# %% [markdown]
## Plot the distribution of senders of chat messages
### Setup Hansken connection
# %% [python]
import sys
import squarify
from types import SimpleNamespace
import matplotlib.pyplot as plt

from hansken.connect import connect_project

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
### Retrieve all senders
# The `unique_values` function returns all values for a given property within a project. In this case, we retrieve all values for `chatMessage.from`.

# %% [python]
sizes = []
labels = []
for sender in context.unique_values("chatMessage.from"):
    sizes.append(sender['count'])
    labels.append(sender['value'])

# %% [markdown]
### Use a treemap visualization to plot the distribution of senders.

# %% [python]
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111)
squarify.plot(sizes=sizes, label=labels, alpha=.6, ax=ax)
plt.axis('off')
plt.show()
