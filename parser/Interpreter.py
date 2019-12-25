HEADLINE, WORD, LBOLD, RBOLD, LITALIC, RITALIC, EOF = 'HEADLINE', 'WORD', 'LBOLD', 'RBOLD', 'LITALIC', 'RITALIC', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def move(self):
        # move the pointer one step forward
        self.pos += 1
        if self.pos > len(self.text) - 1:
            # end of the file
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def headline(self):
        level = 0
        while self.current_char is not None and self.current_char == '#' and level <= 3:
            level += 1
            self.move()
        if (self.current_char.isspace()):
            return Token(HEADLINE, level)
        else:
            return Token(WORD, "#" * level)

    def emphasize(self):
        level = 1
        self.move()
        if (self.current_char == '*'):
            self.move()
            if (self.current_char.isspace()):
                return Token(WORD, "*" * level)
            # else:
                # return Token()
        # else:
        #     return Token(WORD, "*" * level)

    def word(self):
        temp = ""
        while self.current_char is not None and self.current_char not in ['#', '*']:
            temp += self.current_char
            self.move()
        return Token(WORD, temp) 

    def get_next_token(self):
        # Lexical analyzer
        while self.current_char is not None:

            if self.current_char == '#':
                return self.headline()

            if self.current_char == '*':
                return self.emphasize()
            
            return self.word()

        return Token(EOF, None)

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """Interpreter

        expr -> HEADLINE WORD
        """
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()
        left = self.current_token
        self.eat(HEADLINE)
        mid = self.current_token
        self.eat(WORD)


        level = str(left.value)
        result = "<h" + level + ">" + mid.value + " </h" + level + ">"

        return result


def main():
    while True:
        try:
            text = input('pyDown> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()