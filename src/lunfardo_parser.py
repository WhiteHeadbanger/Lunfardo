from constants.tokens import *
from nodes import *
from errors import InvalidSyntaxError
    
# Run Time Result
class RTResult:

    def __init__(self):
        self.reset()
    
    def reset(self):
        self.value = None
        self.error = None
        self.func_return_value = None
        self.loop_should_continue = False
        self.loop_should_break = False

    def register(self, res):
        self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        
        return res.value
    
    def success(self, value):
        self.reset()
        self.value = value
        return self
    
    def success_return(self, value):
        self.reset()
        self.func_return_value = value
        return self
    
    def success_continue(self):
        self.reset()
        self.loop_should_continue = True
        return self
    
    def success_break(self):
        self.reset()
        self.loop_should_break = True
        return self
    
    def failure(self, error):
        self.reset()
        self.error = error
        return self
    
    def should_return(self):
        return (
            self.error or
            self.func_return_value or
            self.loop_should_continue or
            self.loop_should_break
        )

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
                "Se esperaba '+', '-', '*', '/', '^', '==', '!=', '<', '>', '<=', '>=', 'y' ó 'o'"))
        return res
    # MARK: Parser.statements
    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == TT_NEWLINE:
            res.register_advance()
            self.advance()

        statement = res.register(self.statement())
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

            statement = res.try_register(self.statement())
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
    
    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.matches(TT_KEYWORD, 'devolver'):
            res.register_advance()
            self.advance()
            
            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)

            return res.success(DevolverNode(expr, pos_start, self.current_tok.pos_end.copy()))
        
        if self.current_tok.matches(TT_KEYWORD, 'continuar'):
            res.register_advance()
            self.advance()

            return res.success(ContinuarNode(pos_start, self.current_tok.pos_end.copy()))

        if self.current_tok.matches(TT_KEYWORD, 'rajar'):
            res.register_advance()
            self.advance()

            return res.success(RajarNode(pos_start, self.current_tok.pos_end.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Se esperaba 'devolver', 'continuar', 'rajar', 'poneleque', 'si', 'para', 'mientras', 'laburo', int, float, identifier, '+', '-', '(', '[' ó 'truchar'"
            ))
        
        return res.success(expr)

    # MARK: Parser.call
    def call(self):
        res = ParseResult()
        
        atom = res.register(self.atom())
        if res.error:
            return res
        
        #TODO Accessing a coso by index is currently done like this: coso / index. However I want replace it with the traditional coso[index]. Maybe using coso / index when
        # wanting to split a list in two. From 0 -> index and index + 1 -> end.
        # Here we can address the first issue.
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
                        "Se esperaba ')', 'poneleque', 'si', 'para', 'mientras', 'laburo', int, float, identifier, '+', '-', '(', '[' ó 'truchar'"
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
                        "Se esperaba ',' ó ')'"
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
            
            return res.success(PoneleQueAccessNode(tok))
        
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
                self.current_tok.pos_start, 
                self.current_tok.pos_end,
                "Se esperaba ')'"
            ))
        
        if tok.type == TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            
            if res.error:
                return res
            
            return res.success(list_expr)
        
        if tok.type == TT_LCURLY:
            dict_expr = res.register(self.dict_expr())

            if res.error:
                return res
            
            return res.success(dict_expr)
        
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
            "Se esperaba int, float, identifier, '+', '-', '(', '[', 'si', 'para', 'mientras' ó 'laburo'"
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
                "Se esperaba int, float, identifier, '+', '-', '(', '[' ó truchar'"
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
                "Se esperaba '['"
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
                    "Se esperaba ']', 'poneleque', 'si', 'para', 'mientras', 'laburo', int, float, identifier, '+', '-', '(', '[' ó 'truchar'"
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
                    "Se esperaba ',' ó ']'"
                ))
            
            res.register_advance()
            self.advance()
            

        return res.success(CosoNode(
            element_nodes,
            pos_start,
            self.current_tok.pos_end.copy()
        ))
    
    def dict_expr(self):
        res = ParseResult()

        keys, values = [], []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LCURLY:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Se esperaba '{'"
            ))
        
        res.register_advance()
        self.advance()

        # Empty mataburros (dict)
        if self.current_tok.type == TT_RCURLY:
            res.register_advance()
            self.advance()

        else:
            expr = self.expr()
            if isinstance(expr.node, (CosoNode, MataburrosNode)):
                #TODO create a 'type error' like error
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Un coso ó mataburros no puede utilizarse como clave"
                ))

            keys.append(res.register(expr))
            
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Se esperaba una clave"
                ))
            
            if not self.current_tok.type == TT_COLON:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Se esperaba ':'"
                ))
            
            res.register_advance()
            self.advance()

            values.append(res.register(self.expr()))

            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Se esperaba un valor"
                ))
            
            while self.current_tok.type == TT_COMMA:
                res.register_advance()
                self.advance()

                expr = self.expr()
                if isinstance(expr.node, (CosoNode, MataburrosNode)):
                    #TODO create a 'type error' like error
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Un coso ó mataburros no puede utilizarse como clave"
                    ))
                
                key_value = expr.node.tok.value
                if not key_value in [k.tok.value for k in keys]:
                    keys.append(res.register(expr))
                    
                    if res.error:
                        return res
                    
                    if not self.current_tok.type == TT_COLON:
                        return res.failure(InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Se esperaba ':'"
                        ))
                    
                    res.register_advance()
                    self.advance()

                    values.append(res.register(self.expr()))

                    if res.error:
                        return res
                
                else:
                    # Update value if key token already exists
                    idx = [k.tok.value for k in keys].index(key_value)

                    res.register_advance()
                    self.advance()

                    values[idx] = res.register(self.expr())

                    if res.error:
                        return res
            
            if self.current_tok.type != TT_RCURLY:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Se esperaba ',' ó '}'"
                ))
            
            res.register_advance()
            self.advance()

        return res.success(MataburrosNode(
            keys,
            values,
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

        if self.current_tok.matches(TT_KEYWORD, 'sino'):
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
                        "Se esperaba 'chau'"
                    ))
                
            else:
                expr = res.register(self.statement())
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
                f"Se esperaba '{case_keyword}'"
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
                "Se esperaba 'entonces'"
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
            expr = res.register(self.statement())
            
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
                "Se esperaba 'para'"
            ))
        
        res.register_advance()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Se esperaba identificador"
            ))
        
        var_name = self.current_tok
        
        res.register_advance()
        self.advance()

        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, 
                self.current_tok.pos_end,
                "Se esperaba '='"
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
                "Se esperaba 'hasta'"
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
                "Se esperaba 'entonces'"
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
                    "Se esperaba 'chau'"
                ))
            
            res.register_advance()
            self.advance()
            
            return res.success(ParaNode(var_name, start_value, end_value, step_value, body, True))

        body = res.register(self.statement())
        
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
                "Se esperaba 'mientras'"
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
                "Se esperaba 'entonces'"
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
                    "Se esperaba 'chau'"
                ))
            
            res.register_advance()
            self.advance()
            
            return res.success(MientrasNode(condition, body, True))

        # self.statement() allows for one-liners
        body = res.register(self.statement())
        
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
                "Se esperaba 'laburo'"
            ))
        
        res.register_advance()
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            
            res.register_advance()
            self.advance()

            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, 
                    self.current_tok.pos_end,
                    "Se esperaba '('"
                ))
        
        else:
            var_name_tok = None
            
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, 
                    self.current_tok.pos_end,
                    "Se esperaba identificador ó '('"
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
                        self.current_tok.pos_start, 
                        self.current_tok.pos_end,
                        "Se esperaba identificador"
                    ))
                
                arg_name_toks.append(self.current_tok)
                res.register_advance()
                self.advance()
            
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Se esperaba ',' ó ')'"
                ))
            
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Se esperaba identificador ó ')'"
                ))
            
        res.register_advance()
        self.advance()

        # Here we can change if we want laburos to always have to be defined with a colon. I personally think that it's a good idea to force one-liners
        # and multiline with a return statement. If not provided, just return None.
        if self.current_tok.type == TT_COLON:
            res.register_advance()
            self.advance()

            body = res.register(self.expr())
            
            if res.error:
                return res
            
            return res.success(LaburoDefNode(
                var_name_tok,
                arg_name_toks,
                body,
                True
            ))
        
        if self.current_tok.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Se esperaba ':' ó una nueva linea"
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
                "Se esperaba 'chau'"
            ))
        
        res.register_advance()
        self.advance()

        return res.success(LaburoDefNode(
            var_name_tok,
            arg_name_toks,
            body,
            False
        ))
    
    # MARK: Parse.expr
    def expr(self):
        res = ParseResult()
        
        if self.current_tok.matches(TT_KEYWORD, 'poneleque'):
            res.register_advance()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Se esperaba identificador"
                ))
            
            var_name = self.current_tok
            
            res.register_advance()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Se esperaba '='"
                ))
            
            res.register_advance()
            self.advance()
            
            expr = res.register(self.expr())
            
            if res.error:
                return res

            return res.success(PoneleQueAssignNode(var_name, expr))
        
        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, 'y'), (TT_KEYWORD, 'o'))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Se esperaba 'poneleque', 'si', 'para', 'mientras', 'laburo', numero, identificador, '+', '-', '(', '[' ó 'truchar'"
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
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self