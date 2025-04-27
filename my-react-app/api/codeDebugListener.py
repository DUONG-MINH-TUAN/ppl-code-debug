# Generated from codeDebug.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .codeDebugParser import codeDebugParser
else:
    from codeDebugParser import codeDebugParser

# This class defines a complete listener for a parse tree produced by codeDebugParser.
class codeDebugListener(ParseTreeListener):

    # Enter a parse tree produced by codeDebugParser#program.
    def enterProgram(self, ctx:codeDebugParser.ProgramContext):
        pass

    # Exit a parse tree produced by codeDebugParser#program.
    def exitProgram(self, ctx:codeDebugParser.ProgramContext):
        pass


    # Enter a parse tree produced by codeDebugParser#main_structure.
    def enterMain_structure(self, ctx:codeDebugParser.Main_structureContext):
        pass

    # Exit a parse tree produced by codeDebugParser#main_structure.
    def exitMain_structure(self, ctx:codeDebugParser.Main_structureContext):
        pass


    # Enter a parse tree produced by codeDebugParser#parameter_list.
    def enterParameter_list(self, ctx:codeDebugParser.Parameter_listContext):
        pass

    # Exit a parse tree produced by codeDebugParser#parameter_list.
    def exitParameter_list(self, ctx:codeDebugParser.Parameter_listContext):
        pass


    # Enter a parse tree produced by codeDebugParser#function_declaration.
    def enterFunction_declaration(self, ctx:codeDebugParser.Function_declarationContext):
        pass

    # Exit a parse tree produced by codeDebugParser#function_declaration.
    def exitFunction_declaration(self, ctx:codeDebugParser.Function_declarationContext):
        pass


    # Enter a parse tree produced by codeDebugParser#body_function.
    def enterBody_function(self, ctx:codeDebugParser.Body_functionContext):
        pass

    # Exit a parse tree produced by codeDebugParser#body_function.
    def exitBody_function(self, ctx:codeDebugParser.Body_functionContext):
        pass


    # Enter a parse tree produced by codeDebugParser#content.
    def enterContent(self, ctx:codeDebugParser.ContentContext):
        pass

    # Exit a parse tree produced by codeDebugParser#content.
    def exitContent(self, ctx:codeDebugParser.ContentContext):
        pass


    # Enter a parse tree produced by codeDebugParser#return_statement.
    def enterReturn_statement(self, ctx:codeDebugParser.Return_statementContext):
        pass

    # Exit a parse tree produced by codeDebugParser#return_statement.
    def exitReturn_statement(self, ctx:codeDebugParser.Return_statementContext):
        pass


    # Enter a parse tree produced by codeDebugParser#variableTypes.
    def enterVariableTypes(self, ctx:codeDebugParser.VariableTypesContext):
        pass

    # Exit a parse tree produced by codeDebugParser#variableTypes.
    def exitVariableTypes(self, ctx:codeDebugParser.VariableTypesContext):
        pass


    # Enter a parse tree produced by codeDebugParser#stateSetter.
    def enterStateSetter(self, ctx:codeDebugParser.StateSetterContext):
        pass

    # Exit a parse tree produced by codeDebugParser#stateSetter.
    def exitStateSetter(self, ctx:codeDebugParser.StateSetterContext):
        pass


    # Enter a parse tree produced by codeDebugParser#statePair.
    def enterStatePair(self, ctx:codeDebugParser.StatePairContext):
        pass

    # Exit a parse tree produced by codeDebugParser#statePair.
    def exitStatePair(self, ctx:codeDebugParser.StatePairContext):
        pass


    # Enter a parse tree produced by codeDebugParser#initialValue.
    def enterInitialValue(self, ctx:codeDebugParser.InitialValueContext):
        pass

    # Exit a parse tree produced by codeDebugParser#initialValue.
    def exitInitialValue(self, ctx:codeDebugParser.InitialValueContext):
        pass


    # Enter a parse tree produced by codeDebugParser#valueForInitialization.
    def enterValueForInitialization(self, ctx:codeDebugParser.ValueForInitializationContext):
        pass

    # Exit a parse tree produced by codeDebugParser#valueForInitialization.
    def exitValueForInitialization(self, ctx:codeDebugParser.ValueForInitializationContext):
        pass


    # Enter a parse tree produced by codeDebugParser#array.
    def enterArray(self, ctx:codeDebugParser.ArrayContext):
        pass

    # Exit a parse tree produced by codeDebugParser#array.
    def exitArray(self, ctx:codeDebugParser.ArrayContext):
        pass


    # Enter a parse tree produced by codeDebugParser#numberArray.
    def enterNumberArray(self, ctx:codeDebugParser.NumberArrayContext):
        pass

    # Exit a parse tree produced by codeDebugParser#numberArray.
    def exitNumberArray(self, ctx:codeDebugParser.NumberArrayContext):
        pass


    # Enter a parse tree produced by codeDebugParser#stringArray.
    def enterStringArray(self, ctx:codeDebugParser.StringArrayContext):
        pass

    # Exit a parse tree produced by codeDebugParser#stringArray.
    def exitStringArray(self, ctx:codeDebugParser.StringArrayContext):
        pass


    # Enter a parse tree produced by codeDebugParser#arrayValue.
    def enterArrayValue(self, ctx:codeDebugParser.ArrayValueContext):
        pass

    # Exit a parse tree produced by codeDebugParser#arrayValue.
    def exitArrayValue(self, ctx:codeDebugParser.ArrayValueContext):
        pass


    # Enter a parse tree produced by codeDebugParser#stringValue.
    def enterStringValue(self, ctx:codeDebugParser.StringValueContext):
        pass

    # Exit a parse tree produced by codeDebugParser#stringValue.
    def exitStringValue(self, ctx:codeDebugParser.StringValueContext):
        pass


    # Enter a parse tree produced by codeDebugParser#identifierValue.
    def enterIdentifierValue(self, ctx:codeDebugParser.IdentifierValueContext):
        pass

    # Exit a parse tree produced by codeDebugParser#identifierValue.
    def exitIdentifierValue(self, ctx:codeDebugParser.IdentifierValueContext):
        pass


    # Enter a parse tree produced by codeDebugParser#element.
    def enterElement(self, ctx:codeDebugParser.ElementContext):
        pass

    # Exit a parse tree produced by codeDebugParser#element.
    def exitElement(self, ctx:codeDebugParser.ElementContext):
        pass


    # Enter a parse tree produced by codeDebugParser#emptyFragment.
    def enterEmptyFragment(self, ctx:codeDebugParser.EmptyFragmentContext):
        pass

    # Exit a parse tree produced by codeDebugParser#emptyFragment.
    def exitEmptyFragment(self, ctx:codeDebugParser.EmptyFragmentContext):
        pass


    # Enter a parse tree produced by codeDebugParser#openTag.
    def enterOpenTag(self, ctx:codeDebugParser.OpenTagContext):
        pass

    # Exit a parse tree produced by codeDebugParser#openTag.
    def exitOpenTag(self, ctx:codeDebugParser.OpenTagContext):
        pass


    # Enter a parse tree produced by codeDebugParser#closeTag.
    def enterCloseTag(self, ctx:codeDebugParser.CloseTagContext):
        pass

    # Exit a parse tree produced by codeDebugParser#closeTag.
    def exitCloseTag(self, ctx:codeDebugParser.CloseTagContext):
        pass


    # Enter a parse tree produced by codeDebugParser#elementContent.
    def enterElementContent(self, ctx:codeDebugParser.ElementContentContext):
        pass

    # Exit a parse tree produced by codeDebugParser#elementContent.
    def exitElementContent(self, ctx:codeDebugParser.ElementContentContext):
        pass


    # Enter a parse tree produced by codeDebugParser#valueIndicator.
    def enterValueIndicator(self, ctx:codeDebugParser.ValueIndicatorContext):
        pass

    # Exit a parse tree produced by codeDebugParser#valueIndicator.
    def exitValueIndicator(self, ctx:codeDebugParser.ValueIndicatorContext):
        pass



del codeDebugParser