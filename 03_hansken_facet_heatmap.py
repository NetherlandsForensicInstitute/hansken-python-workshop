# %% [markdown]
# Plot searches over time

import pandas as pd

from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.colors import LogNorm

from hansken.connect import connect_project
from hansken.query import RangeFacet

# %% [python]

# setup Hansken project context

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

# %%

# Perform facet search in Hansken accross dates and present results in a heatmap

start = '2022-7-1T00:00Z'
end = '2022-7-31T23:59Z'
# search_query = "type:chatMessage"
search_query = "type:browserHistory"

# Group the number of searches by the accessedOn property on a scale of a day. A Facet on a date requires a min and max
facet = RangeFacet('dates', scale='hour', min=start, max=end)

# Create a dataframe with entries per hour for the period indicated by start and end
df = pd.DataFrame()
df['Time'] = pd.date_range(start, end, freq='1H')
df['Count'] = 0
df.set_index('Time', inplace=True)

# Perform search using the facet
with context.search(search_query, facets=facet, count=0) as search_result:
    for _, result in search_result.facets[0].items():
        df.loc[pd.to_datetime(result.value), 'Count'] = result.count

# So that we can pivot and prepare a dataframe for our heatmap
df_map = pd.pivot_table(df, fill_value=0.0, columns=df.index.date, index=df.index.hour, aggfunc="sum")['Count']

sns.heatmap(df_map, cmap="Greens", norm=LogNorm())
plt.show()

# %%
