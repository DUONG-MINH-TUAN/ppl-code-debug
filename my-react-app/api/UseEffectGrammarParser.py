# Generated from UseEffectGrammar.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\21")
        buf.write("X\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\5\4(\n\4\3")
        buf.write("\5\3\5\3\5\7\5-\n\5\f\5\16\5\60\13\5\3\6\3\6\3\6\3\6\7")
        buf.write("\6\66\n\6\f\6\16\69\13\6\5\6;\n\6\3\6\3\6\3\7\3\7\7\7")
        buf.write("A\n\7\f\7\16\7D\13\7\3\7\3\7\3\b\3\b\5\bJ\n\b\3\b\3\b")
        buf.write("\3\t\3\t\3\t\5\tQ\n\t\3\t\3\t\3\n\3\n\3\n\3\n\2\2\13\2")
        buf.write("\4\6\b\n\f\16\20\22\2\2\2U\2\24\3\2\2\2\4\26\3\2\2\2\6")
        buf.write("\'\3\2\2\2\b)\3\2\2\2\n\61\3\2\2\2\f>\3\2\2\2\16I\3\2")
        buf.write("\2\2\20M\3\2\2\2\22T\3\2\2\2\24\25\5\4\3\2\25\3\3\2\2")
        buf.write("\2\26\27\7\3\2\2\27\30\7\4\2\2\30\31\5\6\4\2\31\32\7\5")
        buf.write("\2\2\32\33\5\n\6\2\33\34\7\6\2\2\34\35\7\7\2\2\35\5\3")
        buf.write("\2\2\2\36\37\7\b\2\2\37 \7\t\2\2 (\5\f\7\2!\"\7\4\2\2")
        buf.write("\"#\5\b\5\2#$\7\6\2\2$%\7\t\2\2%&\5\f\7\2&(\3\2\2\2\'")
        buf.write("\36\3\2\2\2\'!\3\2\2\2(\7\3\2\2\2).\7\17\2\2*+\7\5\2\2")
        buf.write("+-\7\17\2\2,*\3\2\2\2-\60\3\2\2\2.,\3\2\2\2./\3\2\2\2")
        buf.write("/\t\3\2\2\2\60.\3\2\2\2\61:\7\n\2\2\62\67\7\17\2\2\63")
        buf.write("\64\7\5\2\2\64\66\7\17\2\2\65\63\3\2\2\2\669\3\2\2\2\67")
        buf.write("\65\3\2\2\2\678\3\2\2\28;\3\2\2\29\67\3\2\2\2:\62\3\2")
        buf.write("\2\2:;\3\2\2\2;<\3\2\2\2<=\7\13\2\2=\13\3\2\2\2>B\7\f")
        buf.write("\2\2?A\5\16\b\2@?\3\2\2\2AD\3\2\2\2B@\3\2\2\2BC\3\2\2")
        buf.write("\2CE\3\2\2\2DB\3\2\2\2EF\7\r\2\2F\r\3\2\2\2GJ\5\20\t\2")
        buf.write("HJ\5\22\n\2IG\3\2\2\2IH\3\2\2\2JK\3\2\2\2KL\7\7\2\2L\17")
        buf.write("\3\2\2\2MN\7\17\2\2NP\7\4\2\2OQ\7\20\2\2PO\3\2\2\2PQ\3")
        buf.write("\2\2\2QR\3\2\2\2RS\7\6\2\2S\21\3\2\2\2TU\7\16\2\2UV\5")
        buf.write("\20\t\2V\23\3\2\2\2\t\'.\67:BIP")
        return buf.getvalue()


class UseEffectGrammarParser ( Parser ):

    grammarFileName = "UseEffectGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'useEffect'", "'('", "','", "')'", "';'", 
                     "'()'", "'=>'", "'['", "']'", "'{'", "'}'", "'return'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "ID", "STRING", "WS" ]

    RULE_prog = 0
    RULE_useEffectCall = 1
    RULE_callback = 2
    RULE_params = 3
    RULE_dependencyArray = 4
    RULE_block = 5
    RULE_statement = 6
    RULE_exprStmt = 7
    RULE_returnStmt = 8

    ruleNames =  [ "prog", "useEffectCall", "callback", "params", "dependencyArray", 
                   "block", "statement", "exprStmt", "returnStmt" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    ID=13
    STRING=14
    WS=15

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def useEffectCall(self):
            return self.getTypedRuleContext(UseEffectGrammarParser.UseEffectCallContext,0)


        def getRuleIndex(self):
            return UseEffectGrammarParser.RULE_prog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProg" ):
                listener.enterProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProg" ):
                listener.exitProg(self)




    def prog(self):

        localctx = UseEffectGrammarParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 18
            self.useEffectCall()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UseEffectCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def callback(self):
            return self.getTypedRuleContext(UseEffectGrammarParser.CallbackContext,0)


        def dependencyArray(self):
            return self.getTypedRuleContext(UseEffectGrammarParser.DependencyArrayContext,0)


        def getRuleIndex(self):
            return UseEffectGrammarParser.RULE_useEffectCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUseEffectCall" ):
                listener.enterUseEffectCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUseEffectCall" ):
                listener.exitUseEffectCall(self)




    def useEffectCall(self):

        localctx = UseEffectGrammarParser.UseEffectCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_useEffectCall)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self.match(UseEffectGrammarParser.T__0)
            self.state = 21
            self.match(UseEffectGrammarParser.T__1)
            self.state = 22
            self.callback()
            self.state = 23
            self.match(UseEffectGrammarParser.T__2)
            self.state = 24
            self.dependencyArray()
            self.state = 25
            self.match(UseEffectGrammarParser.T__3)
            self.state = 26
            self.match(UseEffectGrammarParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CallbackContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def block(self):
            return self.getTypedRuleContext(UseEffectGrammarParser.BlockContext,0)


        def params(self):
            return self.getTypedRuleContext(UseEffectGrammarParser.ParamsContext,0)


        def getRuleIndex(self):
            return UseEffectGrammarParser.RULE_callback

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCallback" ):
                listener.enterCallback(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCallback" ):
                listener.exitCallback(self)




    def callback(self):

        localctx = UseEffectGrammarParser.CallbackContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_callback)
        try:
            self.state = 37
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [UseEffectGrammarParser.T__5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 28
                self.match(UseEffectGrammarParser.T__5)
                self.state = 29
                self.match(UseEffectGrammarParser.T__6)
                self.state = 30
                self.block()
                pass
            elif token in [UseEffectGrammarParser.T__1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 31
                self.match(UseEffectGrammarParser.T__1)
                self.state = 32
                self.params()
                self.state = 33
                self.match(UseEffectGrammarParser.T__3)
                self.state = 34
                self.match(UseEffectGrammarParser.T__6)
                self.state = 35
                self.block()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(UseEffectGrammarParser.ID)
            else:
                return self.getToken(UseEffectGrammarParser.ID, i)

        def getRuleIndex(self):
            return UseEffectGrammarParser.RULE_params

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParams" ):
                listener.enterParams(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParams" ):
                listener.exitParams(self)




    def params(self):

        localctx = UseEffectGrammarParser.ParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_params)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self.match(UseEffectGrammarParser.ID)
            self.state = 44
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==UseEffectGrammarParser.T__2:
                self.state = 40
                self.match(UseEffectGrammarParser.T__2)
                self.state = 41
                self.match(UseEffectGrammarParser.ID)
                self.state = 46
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DependencyArrayContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(UseEffectGrammarParser.ID)
            else:
                return self.getToken(UseEffectGrammarParser.ID, i)

        def getRuleIndex(self):
            return UseEffectGrammarParser.RULE_dependencyArray

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDependencyArray" ):
                listener.enterDependencyArray(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDependencyArray" ):
                listener.exitDependencyArray(self)




    def dependencyArray(self):

        localctx = UseEffectGrammarParser.DependencyArrayContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_dependencyArray)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self.match(UseEffectGrammarParser.T__7)
            self.state = 56
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UseEffectGrammarParser.ID:
                self.state = 48
                self.match(UseEffectGrammarParser.ID)
                self.state = 53
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==UseEffectGrammarParser.T__2:
                    self.state = 49
                    self.match(UseEffectGrammarParser.T__2)
                    self.state = 50
                    self.match(UseEffectGrammarParser.ID)
                    self.state = 55
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 58
            self.match(UseEffectGrammarParser.T__8)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UseEffectGrammarParser.StatementContext)
            else:
                return self.getTypedRuleContext(UseEffectGrammarParser.StatementContext,i)


        def getRuleIndex(self):
            return UseEffectGrammarParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)




    def block(self):

        localctx = UseEffectGrammarParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.match(UseEffectGrammarParser.T__9)
            self.state = 64
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==UseEffectGrammarParser.T__11 or _la==UseEffectGrammarParser.ID:
                self.state = 61
                self.statement()
                self.state = 66
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 67
            self.match(UseEffectGrammarParser.T__10)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def exprStmt(self):
            return self.getTypedRuleContext(UseEffectGrammarParser.ExprStmtContext,0)


        def returnStmt(self):
            return self.getTypedRuleContext(UseEffectGrammarParser.ReturnStmtContext,0)


        def getRuleIndex(self):
            return UseEffectGrammarParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)




    def statement(self):

        localctx = UseEffectGrammarParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [UseEffectGrammarParser.ID]:
                self.state = 69
                self.exprStmt()
                pass
            elif token in [UseEffectGrammarParser.T__11]:
                self.state = 70
                self.returnStmt()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 73
            self.match(UseEffectGrammarParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(UseEffectGrammarParser.ID, 0)

        def STRING(self):
            return self.getToken(UseEffectGrammarParser.STRING, 0)

        def getRuleIndex(self):
            return UseEffectGrammarParser.RULE_exprStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprStmt" ):
                listener.enterExprStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprStmt" ):
                listener.exitExprStmt(self)




    def exprStmt(self):

        localctx = UseEffectGrammarParser.ExprStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_exprStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self.match(UseEffectGrammarParser.ID)
            self.state = 76
            self.match(UseEffectGrammarParser.T__1)
            self.state = 78
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UseEffectGrammarParser.STRING:
                self.state = 77
                self.match(UseEffectGrammarParser.STRING)


            self.state = 80
            self.match(UseEffectGrammarParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def exprStmt(self):
            return self.getTypedRuleContext(UseEffectGrammarParser.ExprStmtContext,0)


        def getRuleIndex(self):
            return UseEffectGrammarParser.RULE_returnStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStmt" ):
                listener.enterReturnStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStmt" ):
                listener.exitReturnStmt(self)




    def returnStmt(self):

        localctx = UseEffectGrammarParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_returnStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.match(UseEffectGrammarParser.T__11)
            self.state = 83
            self.exprStmt()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





