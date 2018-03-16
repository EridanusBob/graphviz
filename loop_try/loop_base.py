class FuncBlock:
    def __init__(self, name=None):
        self.name = name
        self.items = []
        self.head_node_name = None
        self.tail_node_name = None

    def add_item(self, item):
        self.items.append(item)


class OnelineCode:
    def __init__(self, code_string):
        self.code_string = code_string

    def __str__(self):
        return self.code_string


class LinesCode:
    def __init__(self):
        self.items = []

    def add_line(self, item):
        self.items.append(item)

    def __str__(self):
        # ToDo 有更好的写法,待完善
        result = []
        for i in self.items:
            result.append(i.code_string)
        return '\n'.join(result)


class IfBlockCode:
    def __init__(self, condition):
        self.condition = condition
        self.if_true = None
        self.if_false = None


class LoopCode:
    def __init__(self):
        self.node_name = None
        self.init_block = None
        self.ifblock = None
        self.other_block = None
        self.other_block_head = None
        self.other_block_tail = None
        self.break_node_name = None
        self.continue_node_name = None


FuncStructObj = FuncBlock("Insieme_SpromVerifyMain")

item1 = OnelineCode(r'ENTER "Insieme_SpromProgMain\\n"')
item2 = OnelineCode('CLR_REM')

init_block = LinesCode()
init_block.add_line(OnelineCode('setnumber pres_subslot_num 0'))
init_block.add_line(OnelineCode('calc pres_slot_num += 1'))

condition = "pres_subslot_num > max_subslots"
ifblock = IfBlockCode(condition)
ifblock.if_true = OnelineCode('break')

init_block1 = LinesCode()
init_block1.add_line(OnelineCode('setnumber aaa 0'))
init_block1.add_line(OnelineCode('calc aaa += 1'))
condition = "aaa > 10"
ifblock1 = IfBlockCode(condition)
ifblock1.if_true = OnelineCode('break')
temp = LoopCode()
temp.init_block = init_block1
temp.ifblock = ifblock1
other_block = FuncBlock("haha")
a = OnelineCode('hahaha')
other_block.items = [temp, a]


item3 = LoopCode()
item3.init_block = init_block
item3.ifblock = ifblock
item3.other_block = other_block
# item3.other_block = temp
# item3.other_block = OnelineCode('111')
item4 = OnelineCode('EXIT')
FuncStructObj.items = [item1, item2, item3, item4]

if __name__ == "__main__":
    print(FuncStructObj.name, '\n')
    for i in FuncStructObj.items:
        if type(i) == IfBlockCode:
            print(i.condition, '\n', i.if_true, '\n', i.if_false, '\n')
        else:
            print(i, '\n')

