# %% [markdown]
## Plot searches over time

### Initialize Hansken connection
# Replace `hansken_host` with the ip of a Hansken instance.

# %% [python]
import sys
import pandas as pd

from types import SimpleNamespace
from matplotlib import pyplot

from hansken.connect import connect_project
from hansken.query import RangeFacet

# The line below finds out if we run in the browser by checking for the js module
in_browser = 'js' in sys.modules
hansken_host = ''
context = connect_project(endpoint=f'http://{hansken_host}:9091/gatekeeper/',
                          project='5ee273fd-0978-4a0a-b8b0-2af2f8479214',
                          keystore=f'http://{hansken_host}:9090/keystore/',
                          # Authentication is faked if we run in the browser,
                          # because an authenticated session should already be present
                          auth=SimpleNamespace() if in_browser else None,
                          interactive=True)

# context = connect_project(endpoint='http://localhost:9091/gatekeeper/',
#                           project='d42bd9c3-63db-474c-a36f-b87e1eb9e2d3',
#                           keystore='http://localhost:9090/keystore/')
# %% [markdown]
### Aggregate browser history data
# The cell below retrieves the browser activity from Hansken. We use a `Facet` to count the number of traces where the `accessedOn` property is within a specific day.
# %% [python]
# Group the number of searches by the accessedOn property on a scale of a day. A Facet on a date requires a min and max
facet = RangeFacet('browserHistory.accessedOn', scale='day', min="2022-01-01", max="2023-01-01")
# Perform search using the facet, set count=0 to prevent hansken returning traces
with context.search("browserHistory.accessedOn=2022", facets=facet, count=0) as search_result:
    # Convert to dataframe
    dateFacetResult = search_result.facets[0]
    df = pd.DataFrame([[counter.value, counter.count] for _, counter in search_result.facets[0].items()],
                      columns=['Day', 'Count'])
# make sure pandas knows this is a timestamp
df['Day'] = pd.to_datetime(df['Day'])
df

# %% [markdown]
### Plot the results
# The cell below uses `pyplot` to create a bar chart using the previous information, plotting the number of traces/day.

# %% [python]
# Plot results
fig, ax = pyplot.subplots(figsize=(10, 6))
ax.bar(df['Day'], df['Count'])
ax.set_xlabel("day")
ax.set_ylabel("count")
ax.set_title('')
pyplot.show()

# %%
