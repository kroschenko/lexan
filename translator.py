from lexic import LexicalAnalyzer

la = LexicalAnalyzer('./programs/prog.pas')
lexeme_list = la.run_analysis()

table = [la.TW, la.TD, la.TNUM, la.TID]
print(lexeme_list)