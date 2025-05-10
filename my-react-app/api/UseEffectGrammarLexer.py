# Generated from UseEffectGrammar.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\21")
        buf.write("_\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\3\2\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3")
        buf.write("\7\3\b\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3\r\3")
        buf.write("\r\3\r\3\r\3\r\3\r\3\r\3\16\3\16\7\16K\n\16\f\16\16\16")
        buf.write("N\13\16\3\17\3\17\7\17R\n\17\f\17\16\17U\13\17\3\17\3")
        buf.write("\17\3\20\6\20Z\n\20\r\20\16\20[\3\20\3\20\2\2\21\3\3\5")
        buf.write("\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33")
        buf.write("\17\35\20\37\21\3\2\6\5\2C\\aac|\6\2\62;C\\aac|\3\2$$")
        buf.write("\5\2\13\f\17\17\"\"\2a\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2")
        buf.write("\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2")
        buf.write("\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2")
        buf.write("\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\3!")
        buf.write("\3\2\2\2\5+\3\2\2\2\7-\3\2\2\2\t/\3\2\2\2\13\61\3\2\2")
        buf.write("\2\r\63\3\2\2\2\17\66\3\2\2\2\219\3\2\2\2\23;\3\2\2\2")
        buf.write("\25=\3\2\2\2\27?\3\2\2\2\31A\3\2\2\2\33H\3\2\2\2\35O\3")
        buf.write("\2\2\2\37Y\3\2\2\2!\"\7w\2\2\"#\7u\2\2#$\7g\2\2$%\7G\2")
        buf.write("\2%&\7h\2\2&\'\7h\2\2\'(\7g\2\2()\7e\2\2)*\7v\2\2*\4\3")
        buf.write("\2\2\2+,\7*\2\2,\6\3\2\2\2-.\7.\2\2.\b\3\2\2\2/\60\7+")
        buf.write("\2\2\60\n\3\2\2\2\61\62\7=\2\2\62\f\3\2\2\2\63\64\7*\2")
        buf.write("\2\64\65\7+\2\2\65\16\3\2\2\2\66\67\7?\2\2\678\7@\2\2")
        buf.write("8\20\3\2\2\29:\7]\2\2:\22\3\2\2\2;<\7_\2\2<\24\3\2\2\2")
        buf.write("=>\7}\2\2>\26\3\2\2\2?@\7\177\2\2@\30\3\2\2\2AB\7t\2\2")
        buf.write("BC\7g\2\2CD\7v\2\2DE\7w\2\2EF\7t\2\2FG\7p\2\2G\32\3\2")
        buf.write("\2\2HL\t\2\2\2IK\t\3\2\2JI\3\2\2\2KN\3\2\2\2LJ\3\2\2\2")
        buf.write("LM\3\2\2\2M\34\3\2\2\2NL\3\2\2\2OS\7$\2\2PR\n\4\2\2QP")
        buf.write("\3\2\2\2RU\3\2\2\2SQ\3\2\2\2ST\3\2\2\2TV\3\2\2\2US\3\2")
        buf.write("\2\2VW\7$\2\2W\36\3\2\2\2XZ\t\5\2\2YX\3\2\2\2Z[\3\2\2")
        buf.write("\2[Y\3\2\2\2[\\\3\2\2\2\\]\3\2\2\2]^\b\20\2\2^ \3\2\2")
        buf.write("\2\6\2LS[\3\b\2\2")
        return buf.getvalue()


class UseEffectGrammarLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    ID = 13
    STRING = 14
    WS = 15

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'useEffect'", "'('", "','", "')'", "';'", "'()'", "'=>'", "'['", 
            "']'", "'{'", "'}'", "'return'" ]

    symbolicNames = [ "<INVALID>",
            "ID", "STRING", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "ID", "STRING", 
                  "WS" ]

    grammarFileName = "UseEffectGrammar.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


