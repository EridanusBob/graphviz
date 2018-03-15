from hello import FuncStructObj, IfBlockCode, OnelineCode, LinesCode
from graphviz import Digraph
import os

os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz2.38\bin"
y_res, n_res = [], []


def linde_code_process(item, index):
    node_name = index
    dot.node(node_name, item.__str__())


def Ifblock_code_process(item, index):
    global y_res, n_res
    node_name = index
    dot.node(node_name, item.condition, {'shape': "diamond"})
    if item.if_true:
        if type(item.if_true) == IfBlockCode:
            Ifblock_code_process(item.if_true, node_name + 'if_sub')
            dot.edge(node_name, node_name + 'if_sub', label="Y")
        elif type(item.if_true) in (OnelineCode, LinesCode):
            node_name_true = node_name + 'if_true'
            dot.node(node_name_true, item.if_true.__str__())
            dot.edge(node_name, node_name_true, label="Y")
            y_res.append((node_name_true, True))
        else:
            pass
    else:
        y_res.append((node_name, False))

    if item.if_false:
        if type(item.if_false) == IfBlockCode:
            Ifblock_code_process(item.if_false, node_name + 'if_sub')
            dot.edge(node_name, node_name + 'if_sub', label="N")
        elif type(item.if_false) in (OnelineCode, LinesCode):
            node_name_false = node_name + 'if_false'
            dot.node(node_name_false, item.if_false.__str__())
            dot.edge(node_name, node_name_false, label="N")
            n_res.append((node_name_false, True))
        else:
            pass
    else:
        n_res.append((node_name, False))


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

# 处理每个item
for i in items:
    index = str(items.index(i))
    if type(i) == IfBlockCode:
        Ifblock_code_process(i, index)
        i.y_res, i.n_res = y_res.copy(), n_res.copy()
        y_res, n_res = [], []
    elif type(i) in (OnelineCode, LinesCode):
        linde_code_process(i, index)
    else:
        pass

nodes = []
# 获取每个item首尾nodes
for i in items:
    node_name = str(items.index(i))
    if type(i) == IfBlockCode:
        nodes.append((node_name, (i.y_res, i.n_res)))
    elif type(i) in (OnelineCode, LinesCode):
        nodes.append((node_name, node_name))
    else:
        pass

# 将每个item首尾nodes串起来
for i in nodes:
    index = nodes.index(i)
    if index > 0:
        last_item_tail = nodes[index - 1][1]
        this_item_head = nodes[index][0]
        print(type(last_item_tail), last_item_tail, type(this_item_head), this_item_head)

        if type(last_item_tail) == tuple:
            for member in last_item_tail[0]:
                if member[1]:
                    dot.edge(member[0], this_item_head)
                else:
                    dot.edge(member[0], this_item_head, label="Y")

            for member in last_item_tail[1]:
                if member[1]:
                    dot.edge(member[0], this_item_head)
                else:
                    dot.edge(member[0], this_item_head, label="N")
        elif type(last_item_tail) == str:
            dot.edge(last_item_tail, this_item_head)

# Check the generated source code:
print(dot.source)

# Save and render the source code, optionally view the result:
# dot.render(FuncStructObj.name + '.gv', view=True)  # doctest: +SKIP
if os.path.exists(FuncStructObj.name + '.gv'):
    os.remove(FuncStructObj.name + '.gv')
    os.remove(FuncStructObj.name + '.gv' + '.pdf')
dot.view(FuncStructObj.name + '.gv')