from hansken.connect import connect_project
import pandas as pd
from plotly import graph_objects as go

hansken_host = ''
hansken_project = 'd42bd9c3-63db-474c-a36f-b87e1eb9e2d3'

context = connect_project(
    endpoint=f'http://{hansken_host}:9091/gatekeeper/',
    project=hansken_project,
    keystore=f'http://{hansken_host}:9090/keystore/'
)


def walk_tree(context, root, depth, root_label=None):
    if not depth:
        return

    for trace in context.search(f"parent:'{root.uid}'"):
        yield {
            'id': trace.uid,
            'parent': '' if root.uid == root_label else root.uid,
            'label': trace.name,
            'size': trace.get('data.raw.size', 0),
        }

        yield from walk_tree(context, trace, depth=depth - 1)


root_uid = '7b602a8b-f941-4f39-a2e4-0d0cfe8d2476:0-0'
max_depth = 3

root_trace = context.trace(root_uid)
data = list(walk_tree(context, root_trace, max_depth, root_label=root_uid))
data = pd.DataFrame(data)

fig = go.Figure(go.Treemap(
    ids=data['id'],
    parents=data['parent'],
    labels=data['label'],
    values=data['size'],
))
fig.show()
