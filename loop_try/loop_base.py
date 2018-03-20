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
        self.other_block = None  # FuncBlock类型数据
        self.other_block_head = None
        self.other_block_tail = None
        self.break_node_name = None
        self.continue_node_name = None


FuncStructObj = FuncBlock("Insieme_SpromVerifyMain")
item1 = LinesCode()
item1.add_line(OnelineCode(r'ENTER "Insieme_SpromVerifyMain\\n"'))
item1.add_line(OnelineCode(r'setstring test "SPROM VERIFY"'))
item1.add_line(OnelineCode(r'UPDATE_CELL_DISPLAY'))
item2 = OnelineCode(r'setnumber pres_slot_num 0')

init_block = LinesCode()
init_block.add_line(OnelineCode('setnumber pres_subslot_num 0'))
init_block.add_line(OnelineCode('calc pres_slot_num += 1'))

condition = "pres_subslot_num > max_subslots"
ifblock = IfBlockCode(condition)
ifblock.if_true = OnelineCode('break')

condition = "pres_subslot_num > max_subslots"
ifblock1 = IfBlockCode(condition)
ifblock1.if_true = OnelineCode('break')

ddd = FuncBlock(FuncStructObj.name + "_loop1" + "_sub1")
ddd1 = OnelineCode(r' DBG2 "Slot (%d/%d),  Run Status: [0x%x]\\n" pres_slot_num pres_subslot_num status')
ddd2 = IfBlockCode("!(status & status_running) || (status & status_gold)")
ddd22 = LinesCode()
ddd22.add_line(OnelineCode('calc pres_subslot_num += 1'))
ddd22.add_line(OnelineCode('continue'))
ddd2.if_true = ddd22

ddd3 = LoopCode()
ddd3.ifblock = IfBlockCode("!(dbg & dbg_DoSpromChecking)")
ddd3.ifblock.if_true = LinesCode()
ddd3.ifblock.if_true.add_line(OnelineCode(r'type "Skipping SPROM Capture\\n"'))
ddd3.ifblock.if_true.add_line(OnelineCode(r'break'))

eee = FuncBlock(FuncStructObj.name + "_loop1" + "_sub1" + "_sub1")
eee1 = OnelineCode(r' call Insieme_SpromCaptureSingleLine')
eee2 = IfBlockCode("(status & status_running)")
eee2.if_true = OnelineCode("call Insieme_SpromCheckToScanned")
eee3 = IfBlockCode("(status & status_running)")
eee3.if_true = OnelineCode("call Insieme_SpromCheckToCMPD")
eee.items = [ddd1, ddd2, ddd3]
ddd3.other_block = eee
# ddd3 = IfBlockCode("!(dbg & dbg_DoSpromChecking)")
# ddd3.if_true = OnelineCode(r'type "Skipping SPROM Capture\\n"')
# ddd3_else = FuncBlock(FuncStructObj.name + "_loop1" + "_sub1" + "_elseCode")
# ddd3_else_1 = OnelineCode(r'call Insieme_SpromCaptureSingleLine')
# ddd3_else_2 = IfBlockCode("(status & status_running)")
# ddd3_else_2.if_true = OnelineCode(r'call Insieme_SpromCheckToScanned')
# ddd3_else_3 = IfBlockCode("(status & status_running)")
# ddd3_else_3.if_true = OnelineCode(r'call Insieme_SpromCheckToCMPD')
# ddd3_else.items = [ddd3_else_1, ddd3_else_2, ddd3_else_3]
# ddd3.if_false = ddd3_else
ddd4 = OnelineCode(r'calc pres_subslot_num += 1')
ddd.items = [ddd1, ddd2, ddd3, ddd4, OnelineCode(r'continue')]

temp = LoopCode()
temp.ifblock = ifblock1
temp.other_block = ddd


other_block = FuncBlock(FuncStructObj.name + "_loop1")  # 注意，一定要给名字(独一无二的名)
other_block.items = [temp, OnelineCode(r'continue')]


item3 = LoopCode()
item3.init_block = init_block
item3.ifblock = ifblock
item3.other_block = other_block
# item3.other_block = temp
# item3.other_block = OnelineCode('111')
item4 = OnelineCode(r'EXIT "Insieme_SpromVerifyMain\\n"')
FuncStructObj.items = [item1, item2, item3, item4]

if __name__ == "__main__":
    print(FuncStructObj.name, '\n')
    for i in FuncStructObj.items:
        if type(i) == IfBlockCode:
            print(i.condition, '\n', i.if_true, '\n', i.if_false, '\n')
        else:
            print(i, '\n')

