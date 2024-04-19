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

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    
    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '+', '-', '*' or '/'"))
        return res
    
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
                        "Expected ')', 'cualca', 'si', 'para', 'mientras', 'laburo', int, float, identifier"
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

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advance()
            self.advance()
            return res.success(NumberNode(tok))
        
        if tok.type == TT_STRING:
            res.register_advance()
            self.advance()
            return res.success(StringNode(tok))
        
        if tok.type == TT_IDENTIFIER:
            res.register_advance()
            self.advance()
            return res.success(VarAccessNode(tok))
        
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
            "Expected int, float, identifier, '+', '-', '(', 'si', 'para', 'mientras', 'laburo'"
        ))
    
    def power(self):
        return self.bin_op(self.call, (TT_POW,), self.factor)
    
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
    
    # comparison expresion
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
                "Expected int, float, identifier, '+', '-' or '(', 'truchar'"
            ))
        
        return res.success(node)
    
    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))
    
    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, 'si'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected 'si'"
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

        expr = res.register(self.expr())
        if res.error:
            return res
        
        cases.append((condition, expr))

        while self.current_tok.matches(TT_KEYWORD, 'osi'):
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

            expr = res.register(self.expr())
        
        if self.current_tok.matches(TT_KEYWORD, 'otro'):
            res.register_advance()
            self.advance()

            else_case = res.register(self.expr())
            if res.error:
                return res

        return res.success(IfNode(cases, else_case))
    
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

        body = res.register(self.expr())
        if res.error:
            return res
        
        return res.success(ForNode(var_name, start_value, end_value, step_value, body))

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

        body = res.register(self.expr())
        if res.error:
            return res
        
        return res.success(WhileNode(condition, body))
    
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

        if self.current_tok.type != TT_COLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ':'"
            ))
        
        res.register_advance()
        self.advance()

        node_to_return = res.register(self.expr())
        if res.error:
            return res
        
        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            node_to_return
        ))

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

            return res.success(VarAssignNode(var_name, expr))
        
        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, 'y'), (TT_KEYWORD, 'o'))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected 'cualca', 'si', 'para', 'mientras', 'laburo', int, float, identifier, '+', '-', '(' or 'truchar'"
            ))
        
        return res.success(node)

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
    
class ParseResult:

    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advance(self):
        self.advance_count += 1
    
    def register(self, res):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self