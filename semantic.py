#k, sum: int
#(4, 0)
#(2, 2)
#(4, 1)
#(2, 3)
#(1, 2)

lexeme = []
i=0
lexemes = [(4, 0), (2, 2), (4, 1), (2, 3), (1, 2)]
lexemes.reverse()
TD = ['.', ';', ',', ':', ':=', '(', ')', '+', '-', '*', '/', '=', '>', '<']
TW = ['program', 'var', 'int', 'real', 'bool', 'begin', 'end', 'if', 'then', 'else', 'while', 'do', 'read', 'write', 'true', 'false']

class _TID:
    def __init__(self):
        self.sender = []

    def add_elem(self, id, typeid='', descr=0):
        self.sender.append({'id': id, 'typeid': typeid, 'descr': descr})

TID = _TID()
TID.add_elem('k')
TID.add_elem('sum')

def_stack = []
def decid(l, t):
    if TID.sender[l]['descr'] == 1:
        error()
    else:
        TID.sender[l]['descr'] = 1
        TID.sender[l]['typeid'] = t

def dec(t):
    while def_stack != []:
        l = def_stack.pop()
        decid(l, t)

def error():
    print('Error!')

def identifier():
    if lexeme[0] != 4:
        error()
    else:
        def_stack.append(lexeme[1])
    get_next_lexeme()

def get_next_lexeme():
    global lexeme
    if len(lexemes) != 0:
        lexeme = lexemes.pop()

def eq(lex):
    if lexeme[0] == 2 and TD[lexeme[1]] == lex:
        return True
    elif lexeme[0] == 1 and TW[lexeme[1]] == lex:
        return True
    else:
        return False

def definitions():
    get_next_lexeme()
    identifier()
    while eq(','):
        get_next_lexeme()
        identifier()
    if eq(':'):
        get_next_lexeme()
    else:
        error()
    if eq('int'):
        get_next_lexeme()
        dec('int')
    elif eq('bool'):
        get_next_lexeme()
        dec('bool')
    else:
        error()

definitions()
print(TID.sender)