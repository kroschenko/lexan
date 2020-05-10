
class SyntaxisAnalyzer:

    def __init__(self, lexeme_list, table):
        self.lexeme_list = lexeme_list
        self.index = 0
        self.lexem = None
        self.table = table
        self.error_code = 0

    def get_next_lexeme(self):
        self.lexem = self.lexeme_list[self.index]
        self.index += 1

    def eq(self, str):
        if self.table[self.lexem[0]-1][self.lexem[1]] == str:
            return True
        else:
            return False

    def error(self):
        self.error_code = 1

    def id(self):
        return self.lexem[0] == 4

    def num(self):
        return self.lexem[0] == 3

    def identifier(self):
        if self.lexem[0] != 4:
            self.error()

    def number(self):
        pass

    def description(self):
        pass

    def begin(self):
        if not self.eq('begin'):
            self.error()
        else:
            self.get_next_lexeme()

    def operators(self):
        while self.expression() or self.assign():
            self.get_next_lexeme()

    def operator(self):
        pass

    def end(self):
        if not self.eq('end'):
            self.error()
        else:
            self.get_next_lexeme()

    def program(self):
        if self.eq('program'):
            self.get_next_lexeme()
            self.identifier()
            self.get_next_lexeme()
        if self.eq('var'):
            self.description()
            self.get_next_lexeme()
        self.begin()
        self.operators()
        self.end()

    def assign(self):
        self.variable()
        if self.eq(':='):
            self.get_next_lexeme()
            self.expression()
        else:
            return False
            # self.error()
        return True

    def expression(self):
        self.term()
        while self.eq('+') or self.eq('-'):
            self.get_next_lexeme()
            self.term()
        return True

    def term(self):
        self.primary()
        while self.eq('*') or self.eq('/'):
            self.get_next_lexeme()
            self.primary()
        return True

    def primary(self):
        if self.id():
            self.variable()
        elif self.num():
            self.number()
        elif self.eq('('):
            self.get_next_lexeme()
            self.expression()
            if self.eq(')'):
                self.get_next_lexeme()
            else:
                self.error()
        else:
            return False
        return True

    def variable(self):
        self.identifier()
        if self.eq('['):
            self.get_next_lexeme()
            self.subList()
            if self.eq(']'):
                self.get_next_lexeme()
            else:
                self.error()

    def subList(self):
        self.expression()
        while self.eq(','):
            self.get_next_lexeme()
            self.expression()

    def run_analysis(self):
        self.index = 0
        self.get_next_lexeme()
        self.program()
        if self.error_code == 0:
            print('Analysis is finished successfully!')
        else:
            print('Analysis is failed!')

