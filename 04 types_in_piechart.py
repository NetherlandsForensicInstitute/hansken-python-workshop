# %% [markdown]
## Show the distribution of different trace types within a Hansken project
### Setup Hansken connection

# %% [python]
import sys
import plotly.express as px
from types import SimpleNamespace

from hansken.connect import connect_project
from hansken.query import TermFacet

in_browser = 'js' in sys.modules
hansken_host = ''
project = 'd42bd9c3-63db-474c-a36f-b87e1eb9e2d3'
context = connect_project(endpoint=f'http://{hansken_host}:9091/gatekeeper/',
                          project=project,
                          keystore=f'http://{hansken_host}:9091/keystore/',
                          # Authentication is faked if we run in the browser,
                          # because an authenticated session should already be present
                          auth=SimpleNamespace() if in_browser else None,
                          interactive=True)

# %% [markdown]
### Retrieve different trace types from Hansken.
# A `Facet` query is used to count the different types of traces. This `Facet` returns the 40 most common type of traces for a given query. We query for all traces (`*`), so this will return the most common types within the entire project.

# %% [python]
facet = TermFacet('type', size=40)
# Perform search using the facet, set count=0 to prevent hansken returning traces
with context.search("*", facets=facet, count=0) as searchResult:
    # ignore origin because it is a metatype and compressed to limit the total number of types
    ignoreable_types = {'origin', 'compressed'}
    typeFacet = [bucket for bucket  in searchResult.facets[0].values() 
                 if bucket.value not in ignoreable_types]
    counts = [bucket.count for bucket in typeFacet]
    names = [bucket.value for bucket in typeFacet]

fig = px.pie(values=counts, names=names, title=f'Trace types found in project {project}')
fig.show()
