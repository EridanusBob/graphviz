class FuncBlock:
    def __init__(self, name=None):
        self.name = name
        self.items = []

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

    def add_item(self, item):
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


FuncStructObj = FuncBlock("Insieme_SpromProgMain")
item1 = OnelineCode(r'ENTER "Insieme_SpromProgMain\\n"')
item2 = OnelineCode('CLR_REM')
item3 = OnelineCode('setstring test "SPROM PROG MAIN"')

condition = "(testtype & testtype_SC)||(testtype & testtype_FM)||(testtype & testtype_LC)||(testtype & testtype_Sup)"
item4 = IfBlockCode(condition)
item4.if_true = OnelineCode('Insieme_CortinaSpromProgMain also setnumber CallingDone 1')
# item4.if_false = OnelineCode('11111111111')

condition = "(testtype & testtype_TOR) || (testtype & testtype_MPA)"
item5 = IfBlockCode(condition)
item5.if_true = OnelineCode('Insieme_TORSpromProgMain also setnumber CallingDone 1')
# item5.if_false = OnelineCode('11111111111')

condition = "!(CallingDone)"
item6 = IfBlockCode(condition)
itme6_tureBlock = LinesCode()
itme6_tureBlock.add_item(
    OnelineCode('TYPE "Invalid testtypeStat, Looking for testtype_SC, testtype_TOR, testtype_FM, testtype_Sup"'))
itme6_tureBlock.add_item(OnelineCode('setstring remark1 "Unexpected value of testtype"'))
itme6_tureBlock.add_item(OnelineCode('call Insieme_Fail'))
item6.if_true = itme6_tureBlock
item6.if_false = OnelineCode('11111111111')

item7 = OnelineCode('setstring cell_display4 ""')
item8 = OnelineCode(r'EXIT "Insieme_SpromProgMain\\n"')

FuncStructObj.items = [item1, item2, item3, item4, item5, item6, item7, item8]

if __name__ == "__main__":
    print(FuncStructObj.name, '\n')
    for i in FuncStructObj.items:
        if type(i) == IfBlockCode:
            print(i.condition, '\n', i.if_true, '\n', i.if_false, '\n')
        else:
            print(i, '\n')

