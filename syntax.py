
class SyntaxisAnalyzer:

    def __init__(self, lexeme_list, table):
        self.lexeme_list = lexeme_list
        self.index = 0
        self.lexem = None
        self.table = table
        self.error_code = 0

    def extract_next_lexeme(self):
        self.lexem = self.lexeme_list.pop()

    def get_next_lexeme(self):
        return self.lexeme_list[-1]

    def eq(self, str):
        if self.table[self.lexem[0]-1][self.lexem[1]] == str:
            return True
        else:
            return False

    def error(self, index):
        self.error_code = index
        if index == 1:
            raise Exception("Missing ':'")
        elif index == 2:
            raise Exception("Missing type of variable")
        elif index == 3:
            raise Exception("Missing ';'")
        elif index == 4:
            raise Exception("Missing begin keyword")
        elif index == 5:
            raise Exception("Missing end keyword")
        elif index == 6:
            raise Exception("Missing ')'")
        elif index == 7:
            raise Exception("Missing ']'")

    def id(self):
        return self.lexem[0] == 4

    def num(self):
        return self.lexem[0] == 3

    def identifier(self):
        return self.lexem[0] == 4

    def number(self):
        pass

    def description(self):
        while self.identifier():
            self.extract_next_lexeme()
            if self.eq(','):
                self.extract_next_lexeme()
        if not self.eq(':'):
            self.error(1)
        else:
            self.extract_next_lexeme()
            if not (self.eq('integer') or self.eq('real')):
                self.error(2)
            else:
                self.extract_next_lexeme()
                if not self.eq(';'):
                    self.error(3)

    def begin(self):
        if not self.eq('begin'):
            self.error(4)
        else:
            self.extract_next_lexeme()

    def operators(self):
        while self.assign():
            pass

    def operator(self):
        pass

    def end(self):
        if not self.eq('end'):
            self.error(5)
        else:
            self.extract_next_lexeme()

    def program(self):
        if self.eq('program'):
            self.extract_next_lexeme()
            self.identifier()
            self.extract_next_lexeme()
            if not self.eq(';'):
                self.error(3)
            else:
                self.extract_next_lexeme()
        if self.eq('var'):
            self.extract_next_lexeme()
            self.description()
            self.extract_next_lexeme()
        self.begin()
        self.operators()
        self.end()

    def assign(self):
        self.variable()
        self.extract_next_lexeme()
        if self.eq(':='):
            self.extract_next_lexeme()
            self.expression()
        else:
            return False
        return True

    def expression(self):
        self.term()
        self.extract_next_lexeme()
        while self.eq('+') or self.eq('-'):
            self.extract_next_lexeme()
            self.term()
        return True

    def term(self):
        self.primary()
        while self.eq('*') or self.eq('/'):
            self.extract_next_lexeme()
            self.primary()
        return True

    def primary(self):
        if self.id():
            self.variable()
        elif self.num():
            self.number()
        elif self.eq('('):
            self.extract_next_lexeme()
            self.expression()
            if self.eq(')'):
                self.extract_next_lexeme()
            else:
                self.error(6)
        else:
            return False
        return True

    def variable(self):
        self.identifier()
        if self.eq('['):
            self.extract_next_lexeme()
            self.subList()
            if self.eq(']'):
                self.extract_next_lexeme()
            else:
                self.error(7)

    def subList(self):
        self.expression()
        while self.eq(','):
            self.extract_next_lexeme()
            self.expression()

    def run_analysis(self):
        try:
            self.index = 0
            self.extract_next_lexeme()
            self.program()
        except Exception as e:
            print("Error: " + str(e))
        finally:
            if self.error_code == 0:
                print('Syntax analysis finished successfully!')
            else:
                print('Syntax analysis finished with errors!')

