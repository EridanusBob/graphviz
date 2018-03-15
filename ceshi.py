from ceshi_base import FuncStructObj, IfBlockCode
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz2.38\bin"


dot = Digraph(comment=FuncStructObj.name, engine='dot')
dot.edge_attr = {'comment': "Wildcard edge",
                 'fontname': "sans-serif",
                 'fontsize': '10',
                 'colorscheme': "blues3",
                 'color': '2',
                 'fontcolor': '3'}
dot.node_attr = {'fontname': "serif",
                 'colorscheme': "blues4",
                 'color': "2",
                 'style': "filled",
                 'shape': "rectangle",
                 'fontsize': '13',
                 'fillcolor': "1",
                 'fontcolor': "4"}
# Add nodes and edges:
last_node_name = ""
items = FuncStructObj.items
for i in items:
    node_name = str(items.index(i))
    if type(i) == IfBlockCode:
        dot.node(node_name, i.condition, {'shape': "diamond"})
        if i.if_true:
            node_name_true = str(items.index(i)) + 'if_true'
            dot.node(node_name_true, i.if_true.__str__())
            dot.edge(node_name, node_name_true, label="Y")

        if i.if_false:
            node_name_false = str(items.index(i)) + 'if_false'
            dot.node(node_name_false, i.if_false.__str__())
            dot.edge(node_name, node_name_false, label="N")
    else:
        print(str(items.index(i)), type(str(items.index(i))), i.__str__())
        dot.node(str(items.index(i)), i.__str__())

    if items.index(i) > 0:
        last_item_index = items.index(i) - 1
        last_item = items[last_item_index]
        if type(last_item) == IfBlockCode:
            if last_item.if_true:
                last_node_name = str(last_item_index) + 'if_true'
                dot.edge(last_node_name, node_name)
            else:
                last_node_name = str(last_item_index)
                dot.edge(last_node_name, node_name, label="Y")

            if last_item.if_false:
                last_node_name = str(last_item_index) + 'if_false'
                dot.edge(last_node_name, node_name)
            else:
                last_node_name = str(last_item_index)
                dot.edge(last_node_name, node_name, label="N")
        else:
            last_node_name = str(last_item_index)
            dot.edge(last_node_name, node_name)

# Check the generated source code:
print(dot.source)

# Save and render the source code, optionally view the result:
# dot.render(FuncStructObj.name + '.gv', view=True)  # doctest: +SKIP
if os.path.exists(FuncStructObj.name + '.gv'):
    os.remove(FuncStructObj.name + '.gv')
    os.remove(FuncStructObj.name + '.gv' + '.pdf')
dot.view(FuncStructObj.name + '.gv')
