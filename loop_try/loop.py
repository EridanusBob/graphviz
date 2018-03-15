from loop_try.loop_base import FuncStructObj, IfBlockCode, OnelineCode, LinesCode, LoopCode
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


def loop_code_process(item, index):
    global y_res, n_res
    node_name = index
    # init_block----------------------------------
    init_block = item.init_block
    ifblock = item.ifblock
    other_block = item.other_block
    if init_block is None:
        ifblock.node_name = node_name
        dot.node(node_name, item.ifblock.condition, {'shape': "diamond"})
    elif type(init_block) == LinesCode:
        ifblock.node_name = 'loop_if_block' + node_name
        dot.node(node_name, init_block.items[0].__str__())
        for i in init_block.items:
            local_index = init_block.items.index(i)
            if local_index > 0:
                if local_index == 1:
                    last_node_name = node_name
                else:
                    last_node_name = "loop_init_line" + str(local_index - 1)
                this_node_name = "loop_init_line" + str(local_index)
                dot.node(this_node_name, i.__str__())
                dot.edge(last_node_name, this_node_name)
        dot.node(ifblock.node_name, item.ifblock.condition, {'shape': "diamond"})
        dot.edge("loop_init_line" + str(len(init_block.items) - 1), ifblock.node_name)
    elif type(init_block) == OnelineCode:
        ifblock.node_name = 'loop_if_block' + node_name
        dot.node(ifblock.node_name, item.ifblock.condition, {'shape': "diamond"})
        dot.node(node_name, init_block.__str__())
        dot.edge(node_name, ifblock.node_name)
    # ifblock----------------------------------
    Ifblock_code_process(ifblock, ifblock.node_name)
    ifblock.y_res, ifblock.n_res = y_res.copy(), n_res.copy()
    y_res, n_res = [], []
    item.break_node_name = ifblock.y_res[0][0]
    # other_block----------------------------------
    if type(other_block) == OnelineCode:
        other_block.node_name = 'loop_other_block' + node_name + 'OnelineCode'
        item.continue_node_name = other_block.node_name
        dot.node(other_block.node_name, other_block.__str__())
        other_block.node_tail = other_block.node_name
    else:
        pass

    for member in ifblock.n_res:
        if member[1]:
            dot.edge(member[0], other_block.node_name)
        else:
            dot.edge(member[0], other_block.node_name, label="N")

    dot.edge(other_block.node_tail, 'continue')
    dot.edge('continue', node_name)


# 初始化
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

# 处理每个item,并获取每个item首尾nodes
for i in items:
    index = str(items.index(i))
    if type(i) == IfBlockCode:
        Ifblock_code_process(i, index)
        i.y_res, i.n_res = y_res.copy(), n_res.copy()
        y_res, n_res = [], []
    elif type(i) in (OnelineCode, LinesCode):
        linde_code_process(i, index)
    elif type(i) == LoopCode:
        loop_code_process(i, index)
    else:
        pass

# 将每个item首尾nodes串起来
for i in items:
    index = items.index(i)
    if index > 0:
        last_item = items[index - 1]
        this_item_head = str(index)
        if type(last_item) == IfBlockCode:
            for member in last_item.y_res:
                if member[1]:
                    dot.edge(member[0], this_item_head)
                else:
                    dot.edge(member[0], this_item_head, label="Y")

            for member in last_item.n_res:
                if member[1]:
                    dot.edge(member[0], this_item_head)
                else:
                    dot.edge(member[0], this_item_head, label="N")
        elif type(last_item) in (OnelineCode, LinesCode):
            dot.edge(str(index - 1), this_item_head)
        elif type(i) == LoopCode:
            dot.edge(i.break_node_name, this_item_head)
        else:
            pass

# Check the generated source code:
print(dot.source)

# Save and render the source code, optionally view the result:
if os.path.exists(FuncStructObj.name + '.gv'):
    os.remove(FuncStructObj.name + '.gv')
    os.remove(FuncStructObj.name + '.gv' + '.pdf')
dot.view(FuncStructObj.name + '.gv')