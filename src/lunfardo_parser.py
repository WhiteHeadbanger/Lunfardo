from constants.tokens import *
from nodes import *
from errors import InvalidSyntaxError
    
# Run Time Result
class RTResult:

    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value
    
    def success(self, value):
        self.value = value
        return self
    
    def failure(self, error):
        self.error = error
        return self

# MARK: Parser
class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok
    
    def reverse(self, amount = 1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok
    
    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
    
    def parse(self):
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, 
                self.current_tok.pos_end, 
                "Expected '+', '-', '*', '/', '^', '==', '!=', '<', '>', '<=', '>=', 'y' or 'o'"))
        return res
    # MARK: Parser.statements
    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == TT_NEWLINE:
            res.register_advance()
            self.advance()

        statement = res.register(self.expr())
        if res.error:
            return res
        
        statements.append(statement)

        more_statements = True

        while True:
            nl_count = 0
            
            while self.current_tok.type == TT_NEWLINE:
                res.register_advance()
                self.advance()
                nl_count += 1
            
            if nl_count == 0:
                more_statements = False

            if not more_statements:
                break

            statement = res.try_register(self.expr())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue

            statements.append(statement)
        
        return res.success(CosoNode(
            statements,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    # MARK: Parser.call
    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error:
            return res
        
        if self.current_tok.type == TT_LPAREN:
            res.register_advance()
            self.advance()
            arg_nodes = []

            if self.current_tok.type == TT_RPAREN:
                res.register_advance()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ')', 'cualca', 'si', 'para', 'mientras', 'laburo', int, float, identifier, '+', '-', '(', '[' or 'truchar'"
                    ))
                
                while self.current_tok.type == TT_COMMA:
                    res.register_advance()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res
                
                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ',' or ')'"
                    ))
                
                res.register_advance()
                self.advance()
            
            return res.success(CallNode(atom, arg_nodes))
        
        return res.success(atom)
    # MARK: Parser.atom
    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advance()
            self.advance()
            return res.success(NumeroNode(tok))
        
        if tok.type == TT_STRING:
            res.register_advance()
            self.advance()
            return res.success(ChamuyoNode(tok))
        
        if tok.type == TT_IDENTIFIER:
            res.register_advance()
            self.advance()
            return res.success(CualcaAccessNode(tok))
        
        if tok.type == TT_LPAREN:
            res.register_advance()
            self.advance()
            expr = res.register(self.expr())
            
            if res.error:
                return res
            
            if self.current_tok.type == TT_RPAREN:
                res.register_advance()
                self.advance()
                return res.success(expr)
            
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ')'"
            ))
        
        if tok.type == TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error:
                return res
            
            return res.success(list_expr)
        
        if tok.matches(TT_KEYWORD, 'si'):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            
            return res.success(if_expr)
        
        if tok.matches(TT_KEYWORD, 'para'):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            
            return res.success(for_expr)
        
        if tok.matches(TT_KEYWORD, 'mientras'):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            
            return res.success(while_expr)
        
        if tok.matches(TT_KEYWORD, 'laburo'):
            func_def = res.register(self.func_def())
            if res.error:
                return res
            
            return res.success(func_def)
        
        return res.failure(InvalidSyntaxError(
            tok.pos_start,
            tok.pos_end,
            "Expected int, float, identifier, '+', '-', '(', '[', 'si', 'para', 'mientras', 'laburo'"
        ))
   
    def power(self):
        return self.bin_op(self.call, (TT_POW,), self.factor)
    # MARK: power | factor
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advance()
            self.advance()
            factor = res.register(self.factor())
            
            if res.error:
                return res
            
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))
    
    # MARK: term | comp_expr
    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'truchar'):
            op_tok = self.current_tok
            res.register_advance()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            
            return res.success(UnaryOpNode(op_tok, node))
        
        node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected int, float, identifier, '+', '-', '(', '[' or truchar'"
            ))
        
        return res.success(node)
    
    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))
    # MARK: arith | list_expr
    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected '['"
            ))
        
        res.register_advance()
        self.advance()

        # Empty list
        if self.current_tok.type == TT_RSQUARE:
            res.register_advance()
            self.advance()

        else:
            element_nodes.append(res.register(self.expr()))
            
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected ']', 'cualca', 'si', 'para', 'mientras', 'laburo', int, float, identifier, '+', '-', '(', '[' or 'truchar'"
                ))
            
            while self.current_tok.type == TT_COMMA:
                res.register_advance()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error:
                    return res
            
            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected ',' or ']'"
                ))
            
            res.register_advance()
            self.advance()
            

        return res.success(CosoNode(
            element_nodes,
            pos_start,
            self.current_tok.pos_end.copy()
        ))
    # MARK: Parse.if_expr
    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases('si'))
        if res.error:
            return res
        
        cases, else_case = all_cases
        return res.success(SiNode(cases, else_case))
    
    def if_expr_b(self):
        return self.if_expr_cases('osi')
    
    def if_expr_c(self):
        res = ParseResult()
        else_case = None

        if self.current_tok.matches(TT_KEYWORD, 'otro'):
            res.register_advance()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                res.register_advance()
                self.advance()

                statements = res.register(self.statements())
                if res.error:
                    return res
                
                else_case = (statements, True)
                #MARK:PROBLEMA
                if self.current_tok.matches(TT_KEYWORD, 'chau'):
                    res.register_advance()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected 'chau'"
                    ))
                
            else:
                expr = res.register(self.expr())
                if res.error:
                    return res
                
                else_case = (expr, False)
        
        return res.success(else_case)
    
    def if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_tok.matches(TT_KEYWORD, 'osi'):
            all_cases = res.register(self.if_expr_b())
            if res.error:
                return res
            
            cases, else_case = all_cases
        
        else:
            else_case = res.register(self.if_expr_c())
            if res.error:
                return res
        
        return res.success((cases, else_case))
    
    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                f"Expected '{case_keyword}'"
            ))
        
        res.register_advance()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res
        
        if not self.current_tok.matches(TT_KEYWORD, 'entonces'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected 'entonces'"
            ))
        
        res.register_advance()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advance()
            self.advance()

            statements = res.register(self.statements())
            if res.error:
                return res
            
            cases.append((condition, statements, True))

            if self.current_tok.matches(TT_KEYWORD, 'chau'):
                res.register_advance()
                self.advance()
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                if res.error:
                    return res
                
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        
        else:
            expr = res.register(self.expr())
            if res.error:
                return res
            
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_b_or_c())
            if res.error:
                return res
            
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))

    # MARK: Parse.for_expr
    def for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'para'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected 'para'"
            ))
        
        res.register_advance()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected identifier"
            ))
        
        var_name = self.current_tok
        res.register_advance()
        self.advance()

        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '='"
            ))
        
        res.register_advance()
        self.advance()

        start_value = res.register(self.expr())
        if res.error:
            return res
        
        if not self.current_tok.matches(TT_KEYWORD, 'hasta'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected 'hasta'"
            ))
        
        res.register_advance()
        self.advance()

        end_value = res.register(self.expr())
        if res.error:
            return res
        
        if self.current_tok.matches(TT_KEYWORD, 'entre'):
            res.register_advance()
            self.advance()

            step_value = res.register(self.expr())
            if res.error:
                return res
        else:
            step_value = None

        if not self.current_tok.matches(TT_KEYWORD, 'entonces'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected 'entonces'"
            ))
        
        res.register_advance()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advance()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res
            
            if not self.current_tok.matches(TT_KEYWORD, 'chau'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'chau'"
                ))
            
            res.register_advance()
            self.advance()
            
            return res.success(ParaNode(var_name, start_value, end_value, step_value, body, True))

        body = res.register(self.expr())
        if res.error:
            return res
        
        return res.success(ParaNode(var_name, start_value, end_value, step_value, body, False))
    
    # MARK: Parse.while_expr
    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'mientras'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected 'mientras'"
            ))
        
        res.register_advance()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res
        
        if not self.current_tok.matches(TT_KEYWORD, 'entonces'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected 'entonces'"
            ))
        
        res.register_advance()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advance()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res
            
            if not self.current_tok.matches(TT_KEYWORD, 'chau'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'chau'"
                ))
            
            res.register_advance()
            self.advance()
            
            return res.success(MientrasNode(condition, body, True))

        body = res.register(self.expr())
        if res.error:
            return res
        
        return res.success(MientrasNode(condition, body, False))

    # MARK: Parse.func_expr
    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'laburo'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected 'laburo'"
            ))
        
        res.register_advance()
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advance()
            self.advance()

            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '('"
                ))
        
        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier or '('"
                ))
        
        res.register_advance()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advance()
            self.advance()

            while self.current_tok.type == TT_COMMA:
                res.register_advance()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected identifier"
                    ))
                
                arg_name_toks.append(self.current_tok)
                res.register_advance()
                self.advance()
            
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ',' or ')'"
                ))
            
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier or ')'"
                ))
            
        res.register_advance()
        self.advance()

        if self.current_tok.type == TT_COLON:
            res.register_advance()
            self.advance()

            node_to_return = res.register(self.expr())
            if res.error:
                return res
            
            return res.success(LaburoDefNode(
                var_name_tok,
                arg_name_toks,
                node_to_return,
                False
            ))
        
        if self.current_tok.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ':' or NEWLINE"
            ))
        
        res.register_advance()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res
        
        if not self.current_tok.matches(TT_KEYWORD, 'chau'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected 'chau'"
            ))
        
        res.register_advance()
        self.advance()

        return res.success(LaburoDefNode(
            var_name_tok,
            arg_name_toks,
            body,
            True
        ))
    
    # MARK: Parse.expr
    def expr(self):
        res = ParseResult()
        if self.current_tok.matches(TT_KEYWORD, 'cualca'):
            res.register_advance()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))
            
            var_name = self.current_tok
            res.register_advance()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))
            
            res.register_advance()
            self.advance()
            expr = res.register(self.expr())
            
            if res.error:
                return res

            return res.success(CualcaAssignNode(var_name, expr))
        
        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, 'y'), (TT_KEYWORD, 'o'))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected 'cualca', 'si', 'para', 'mientras', 'laburo', int, float, identifier, '+', '-', '(', '[' or 'truchar'"
            ))
        
        return res.success(node)
    # MARK: Parse.bin_op
    def bin_op(self, func_a, ops, func_b = None):
        if func_b is None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        
        if res.error:
            return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advance()
            self.advance()
            right = res.register(func_b())
            
            if res.error:
                return res
            
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

#MARK: ParseResult
class ParseResult:

    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advance(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1
    
    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        
        return res.node
    
    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self