from loop_try.loop_base22 import FuncStructObj, IfBlockCode, OnelineCode, LinesCode, LoopCode, FuncBlock
from graphviz import Digraph
import os

os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz2.38\bin"
y_res, n_res = [], []


def ifblock_tail_process(y_res, n_res, node_name):
    for member in y_res:
        if member[1]:
            dot.edge(member[0], node_name)
        else:
            dot.edge(member[0], node_name, label="Y")

    for member in n_res:
        if member[1]:
            dot.edge(member[0], node_name)
        else:
            dot.edge(member[0], node_name, label="N")


def code_block_process(obj, **options):
    global y_res, n_res
    items = obj.items
    # 处理每个item,并获取每个item首尾nodes
    for i in items:
        index = str(items.index(i))
        node_name = index + obj.name
        if type(i) == IfBlockCode:
            Ifblock_code_process(i, node_name, **options)
            i.y_res, i.n_res = y_res.copy(), n_res.copy()
            y_res, n_res = [], []
        elif type(i) in (OnelineCode, LinesCode):
            linde_code_process(i, node_name)
        elif type(i) == LoopCode:
            loop_code_process(i, node_name)
        else:
            pass

    # 将每个item首尾nodes串起来
    for i in items:
        index = items.index(i)
        if index > 0 and i.__str__() not in ("continue", "break"):
            last_item = items[index - 1]
            this_item_head = str(index) + obj.name
            if type(last_item) == IfBlockCode:
                ifblock_tail_process(last_item.y_res, last_item.n_res, this_item_head)
            elif type(last_item) in (OnelineCode, LinesCode):
                dot.edge(str(index - 1) + obj.name, this_item_head)
            elif type(last_item) == LoopCode:
                dot.edge(last_item.break_node_name, this_item_head)
            else:
                pass


def linde_code_process(item, index):
    node_name = index
    if item.__str__() not in ("continue", "break"):
        dot.node(node_name, item.__str__())


def Ifblock_code_process(item, index, **options):
    global y_res, n_res
    node_name = index
    dot.node(node_name, item.condition, {'shape': "diamond"})
    if item.if_true:
        if type(item.if_true) == IfBlockCode:
            Ifblock_code_process(item.if_true, node_name + 'if_sub')
            dot.edge(node_name, node_name + 'if_sub', label="Y")
        elif type(item.if_true) == OnelineCode:
            if item.if_true.__str__() == "break":
                item.if_true = None
                dot.edge(node_name, options["break_node_name"], label="Y")
            elif item.if_true.__str__() == "continue":
                item.if_true = None
                dot.edge(node_name, options["continue_node_name"], label="Y")
            else:
                node_name_true = node_name + 'if_true'
                dot.node(node_name_true, item.if_true.__str__())
                dot.edge(node_name, node_name_true, label="Y")
                y_res.append((node_name_true, True))
        elif type(item.if_true) == LinesCode:
            last_member = item.if_true.items[-1]
            if last_member.__str__() == "break":
                item.if_true.items.pop(-1)
                node_name_true = node_name + 'if_true'
                dot.node(node_name_true, item.if_true.__str__())
                dot.edge(node_name, node_name_true)
                dot.edge(node_name_true, options["break_node_name"], label="Y")
            elif last_member.__str__() == "continue":
                item.if_true.items.pop(-1)
                node_name_true = node_name + 'if_true'
                dot.node(node_name_true, item.if_true.__str__())
                dot.edge(node_name, node_name_true)
                dot.edge(node_name_true, options["continue_node_name"])
            else:
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
        elif type(item.if_false) == FuncBlock:
            node_name_false = str(0) + item.if_false.name
            code_block_process(item.if_false)
            dot.edge(node_name, node_name_false, label="N")
            if type(item.if_false.items[-1]) in (LinesCode, OnelineCode):
                n_res.append(((str(len(item.if_false.items) - 1) + item.if_false.name), True))
            elif type(item.if_false.items[-1]) == IfBlockCode:
                n_res.append(((item.if_false.items[-1].y_res[0][0]), True))
            elif type(item.if_false.items[-1]) == LoopCode:
                n_res.append((item.if_false.items[-1].break_node_name, True))
            else:
                pass

        else:
            pass
    else:
        n_res.append((node_name, False))


def loop_code_process(item, index):
    global y_res, n_res
    item.node_name = index
    init_block = item.init_block
    ifblock = item.ifblock
    other_block = item.other_block
    # continue
    item.continue_node_name = item.node_name + 'continue'
    dot.node(item.continue_node_name, 'continue')
    # break
    item.break_node_name = item.node_name + 'break'
    dot.node(item.break_node_name, 'break')

    # init_block-------------------------------------------
    if init_block is None:
        ifblock.node_name = item.node_name
        dot.node(item.node_name, item.ifblock.condition, {'shape': "diamond"})
    elif type(init_block) in (OnelineCode, LinesCode):
        ifblock.node_name = 'loop_if_block' + item.node_name
        dot.node(ifblock.node_name, item.ifblock.condition, {'shape': "diamond"})
        dot.node(item.node_name, init_block.__str__())
        dot.edge(item.node_name, ifblock.node_name)

    # ifblock------------------------------------------------
    options = {"continue_node_name": item.continue_node_name, "break_node_name": item.break_node_name}
    Ifblock_code_process(ifblock, ifblock.node_name, **options)
    ifblock.y_res, ifblock.n_res = y_res.copy(), n_res.copy()
    y_res, n_res = [], []
    # item.break_node_name = ifblock.y_res[0][0]

    # other_block---------------------------------------------
    if other_block is not None:
        code_block_process(other_block, **options)
        other_block.head_node_name = str(0) + other_block.name
        if type(other_block.items[-2]) in (LinesCode, OnelineCode):
            other_block.tail_node_name = str(len(other_block.items) - 2) + other_block.name
        elif type(other_block.items[-2]) == IfBlockCode:
            other_block.tail_node_name = other_block.items[-2].y_res, other_block.items[-2].n_res
        elif type(other_block.items[-2]) == LoopCode:
            other_block.tail_node_name = other_block.items[-2].break_node_name
        else:
            pass
        item.other_block_head = other_block.head_node_name
        item.other_block_tail = other_block.tail_node_name
    else:
        item.other_block_head = ifblock.node_name
        item.other_block_tail = ifblock.node_name

    # other_block 与 continue_block 的连接-------------------
    if other_block.items[-1].__str__() == "continue":
        if other_block is not None:
            # ifblock的N,指向other_block的头
            member = ifblock.n_res[0]
            if member[1]:
                dot.edge(member[0], item.other_block_head)
            else:
                dot.edge(member[0], item.other_block_head, label="N")
            # other_block的尾,指向continue_block
            if type(item.other_block_tail) == tuple:
                ifblock_tail_process(item.other_block_tail[0], item.other_block_tail[1], item.continue_node_name)
            else:
                dot.edge(item.other_block_tail, item.continue_node_name)
        else:
            # ifblock的N,指向continue_block
            dot.edge(ifblock.n_res[0][0], item.continue_node_name, label="N")
        # continue_block执行LoopCode头
        dot.edge(item.continue_node_name, item.node_name)


# 初始化
dot = Digraph(comment=FuncStructObj.name, engine='dot', format='svg')
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
code_block_process(FuncStructObj)
# Check the generated source code:
print(dot.source)
# Save and render the source code, optionally view the result:
if os.path.exists(FuncStructObj.name + '.gv'):
    os.remove(FuncStructObj.name + '.gv')
    os.remove(FuncStructObj.name + '.gv' + '.svg')
dot.view(FuncStructObj.name + '.gv')
