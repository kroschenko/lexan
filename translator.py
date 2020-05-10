from lexic import LexicalAnalyzer
from syntax import SyntaxisAnalyzer

la = LexicalAnalyzer('./programs/example1.pas')
lexeme_list = la.run_analysis()
lexeme_list.reverse()

table = [la.TW, la.TD, la.TNUM, la.TID]
# print(lexeme_list)

sa = SyntaxisAnalyzer(lexeme_list, table)
sa.run_analysis()