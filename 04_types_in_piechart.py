# %% [markdown]
## Show the distribution of different trace types within a Hansken project
### Setup Hansken connection

# %% [python]
import plotly.express as px

from hansken.connect import connect_project
from hansken.query import TermFacet

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
### Retrieve different trace types from Hansken.
# A `Facet` query is used to count the different types of traces. This `Facet` returns the 40 most common type of traces for a given query. We query for all traces (`*`), so this will return the most common types within the entire project.

# %% [python]
facet = TermFacet('type', size=40)
# Perform search using the facet, set count=0 to prevent hansken returning traces
with context.search("*", facets=facet, count=0) as search_result:
    # ignore origin because it is a metatype and compressed to limit the total number of types
    ignoreable_types = {'origin', 'compressed'}
    type_facet = [bucket for bucket in search_result.facets[0].values()
                  if bucket.value not in ignoreable_types]
    counts = [bucket.count for bucket in type_facet]
    names = [bucket.value for bucket in type_facet]

fig = px.pie(values=counts, names=names, title=f'Trace types found in project')
fig.show()

# %%
