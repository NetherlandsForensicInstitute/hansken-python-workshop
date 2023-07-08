from hansken.connect import connect_project
import pandas as pd
from plotly import graph_objects as go

# define our connection parameters
hansken_host = 'hansken'
hansken_project = 'd42bd9c3-63db-474c-a36f-b87e1eb9e2d3'
# connect to the hansken instance at hansken_host
context = connect_project(
    endpoint=f'http://{hansken_host}:9091/gatekeeper/',
    project=hansken_project,
    keystore=f'http://{hansken_host}:9090/keystore/'
)


def walk_tree(context, root, depth, root_label=None):
    """
    Recursively walk *root*, a Hansken trace, creating simple dicts to be used in a tree view.
    """
    if not depth:
        # depth has become falsy (zero), stop recursive steps
        return

    # query hansken for traces whose parent is the provided root
    for trace in context.search(f"parent:'{root.uid}'"):
        # create and provide a simple dictionary representing trace
        yield {
            'id': trace.uid,
            # the treemap will need an indication of what node is to be the root
            # this is done by making the parent an empty string
            'parent': '' if root.uid == root_label else root.uid,
            'label': trace.name,
            # use trace' raw data size to scale the elements in the treemap
            'size': trace.get('data.raw.size', 0),
        }

        # recurse down the tree, up to a certain depth (also see the if at the start of this function)
        yield from walk_tree(context, trace, depth=depth - 1)


root_uid = '7b602a8b-f941-4f39-a2e4-0d0cfe8d2476:0-0'
max_depth = 3
# retrieve the trace object with our root uid
root_trace = context.trace(root_uid)
# populate a list of all the elements produced by walk_tree
data = list(walk_tree(context, root_trace, max_depth, root_label=root_uid))
# turn that list in to a dataframe
data = pd.DataFrame(data)

# now build and show a treemap figure that uses all the references we just created
fig = go.Figure(go.Treemap(
    ids=data['id'],
    parents=data['parent'],
    labels=data['label'],
    values=data['size'],
))
fig.show()
