# %% [markdown]
## Plot the distribution of senders of chat messages
### Setup Hansken connection

# %% [python]
import squarify
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
### Retrieve all senders
# The `unique_values` function returns all values and the number of occurrences for a given property within a project.
# In this case, we retrieve all values for `chatMessage.from`.

# %% [python]
sizes = []
labels = []
for sender in context.unique_values("chatMessage.from"):
    sizes.append(sender['count'])
    labels.append(sender['value'])

# %% [markdown]
### Use a treemap visualization to plot the distribution of senders.

# %% [python]
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111)
squarify.plot(sizes=sizes, label=labels, alpha=.6, ax=ax)
plt.axis('off')
plt.show()

# %%
