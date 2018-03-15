from hello import FuncStructObj, IfBlockCode
from graphviz import Digraph
import os

os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz2.38\bin"
y_res, n_res = [], []


def process_item(item, index):
    global y_res, n_res
    node_name = str(index)
    if type(item) == IfBlockCode:
        dot.node(node_name, item.condition, {'shape': "diamond"})
        if item.if_true:
            if type(item.if_true) == IfBlockCode:
                process_item(item.if_true, index * 10)
                dot.edge(node_name, str(index * 10), label="Y")
            else:
                node_name_true = str(index) + 'if_true'
                dot.node(node_name_true, item.if_true.__str__())
                dot.edge(node_name, node_name_true, label="Y")
                y_res.append((node_name_true, True))
        else:
            y_res.append((str(index), False))
        if item.if_false:
            if type(item.if_false) == IfBlockCode:
                process_item(item.if_false, index * 10)
                dot.edge(node_name, str(index * 10), label="N")
            else:
                node_name_false = str(index) + 'if_false'
                dot.node(node_name_false, item.if_false.__str__())
                dot.edge(node_name, node_name_false, label="N")
                n_res.append((node_name_false, True))
        else:
            n_res.append((str(index), False))
    else:
        dot.node(str(index), item.__str__())


def link_itmes(items, item, index):
    node_name = str(index)
    if items.index(item) > 0:
        last_item_index = items.index(i) - 1
        last_item = items[last_item_index]
        if type(last_item) == IfBlockCode:
            for member in last_item.y_res:
                if member[1]:
                    dot.edge(member[0], node_name)
                else:
                    dot.edge(member[0], node_name, label="Y")

            for member in last_item.n_res:
                if member[1]:
                    dot.edge(member[0], node_name)
                else:
                    dot.edge(member[0], node_name, label="N")
        else:
            last_node_name = str(last_item_index)
            dot.edge(last_node_name, node_name)


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
items = FuncStructObj.items
for i in items:
    index = items.index(i)

    process_item(i, index)
    i.y_res, i.n_res = y_res.copy(), n_res.copy()
    y_res, n_res = [], []

    link_itmes(items, i, index)


# Check the generated source code:
print(dot.source)

# Save and render the source code, optionally view the result:
# dot.render(FuncStructObj.name + '.gv', view=True)  # doctest: +SKIP
if os.path.exists(FuncStructObj.name + '.gv'):
    os.remove(FuncStructObj.name + '.gv')
    os.remove(FuncStructObj.name + '.gv' + '.pdf')
dot.view(FuncStructObj.name + '.gv')
