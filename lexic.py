class LexicalAnalyzer:
    def __init__(self, program_filename):
        self.ch = ''
        self.buf = ''
        self.state = ['H', 'ID', 'NUM', 'COM', 'ASGN', 'DLM', 'FINE', 'ER']
        self.TW = ['program', 'var', 'int', 'real', 'bool', 'begin', 'end', 'if', 'then', 'else', 'while', 'do', 'read', 'write', 'true', 'false']
        self.TD = ['.', ';', ',', ':', ':=', '(', ')', '+', '-', '*', '/', '=', '>', '<']
        self.TNUM = []
        self.TID = []
        self.dt = 0
        self.current_state = 'H'
        self.program_filename = program_filename
        self.file = None
        self.lexeme_list = []

    def get_next(self):
        self.ch = self.file.read(1)

    def clear(self):
        self.buf = ''

    def add(self):
        self.buf += self.ch

    def look(self, cls):
        if self.buf in cls:
            return cls.index(self.buf)
        else:
            return -1

    def put(self, cls):
        if self.buf not in cls:
            cls.append(self.buf)
        return cls.index(self.buf)

    def putnum(self, cls):
        if self.dt not in cls:
            cls.append(self.dt)
        return cls.index(self.dt)

    # @staticmethod
    def make_lex(self, cls, num):
        # print('('+str(cls)+', '+str(num)+')')
        self.lexeme_list.append([cls, num])

    def run_analysis(self):
        self.file = open(self.program_filename, 'r')
        self.get_next()
        while True:
            if self.current_state == 'H':
                if self.ch == ' ' or self.ch == '\n' or self.ch == '\t':
                    self.get_next()
                elif self.ch.isalpha():
                    self.clear()
                    self.add()
                    self.get_next()
                    self.current_state = 'ID'
                elif self.ch.isdigit():
                    self.dt = int(self.ch)
                    self.get_next()
                    self.current_state = 'NUM'
                elif self.ch == '{':
                    self.get_next()
                    self.current_state = 'COM'
                elif self.ch == ':':
                    self.get_next()
                    self.current_state = 'ASGN'
                elif self.ch == '.':
                    self.make_lex(2, 0)
                    self.current_state = 'FIN'
                else:
                    self.current_state = 'DLM'
            elif self.current_state == 'ID':
                if self.ch.isalpha() or self.ch.isdigit():
                    self.add()
                    self.get_next()
                else:
                    j = self.look(self.TW)
                    if j != -1:
                        self.make_lex(1, j)
                    else:
                        j = self.put(self.TID)
                        self.make_lex(4, j)
                    self.current_state = 'H'
            elif self.current_state == 'NUM':
                if self.ch.isdigit():
                    self.dt = self.dt * 10 + int(self.ch)
                    self.get_next()
                else:
                    j = self.putnum(self.TNUM)
                    self.make_lex(3, j)
                    self.current_state = 'H'
            elif self.current_state == 'DLM':
                self.clear()
                self.add()
                j = self.look(self.TD)
                if j != -1:
                    self.get_next()
                    self.make_lex(2, j)
                    self.current_state = 'H'
                else:
                    self.current_state = 'ER'
            elif self.current_state == 'ASGN':
                if self.ch == '=':
                    self.make_lex(2, 4)
                else:
                    self.make_lex(2, 3)
                self.get_next()
                self.current_state = 'H'
            if self.current_state == 'FIN' or self.current_state == 'ER':
                break
        if self.current_state == 'ER':
            print('Error. Please check program for errors!')
        if self.current_state == 'FIN':
            print('Lexical analysis completed successfully!')
        self.file.close()
        return self.lexeme_list

