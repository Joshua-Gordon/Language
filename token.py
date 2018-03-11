import sys
import os
import TokenGrammar

class ReadFile:
    def __init__(self,filename):
        self.file = os.path.join(os.getcwd(),filename)
    def v1(self):
        tokens = []
        with open(self.file) as f:
            for line in f:
                print line
                tokens.append(line)
        return tokens
    def v2(self):
        with open(self.file) as f:
            return f.read()

class Token:
    def __init__(self,token):
        self.value = token
        self.type = "value"
        for key,values in TokenGrammar.knowntokens.items():
            if token in values:
                self.value = token
                self.type = key
    def __str__(self):
       return '%s : %s' % (self.type, self.value)

    def __repr__(self):
        return 'Token(%s, %s)' % (self.type, self.value)

    def printing():
        print "Type: " + self.type + " Value: " + self.value

class Tokenizer:
    def __init__(self,filename):
        self.curtoken = ""
        self.TokenList = []
        self.filecontent = ReadFile(filename).v2()
    def getNextToken(self):
        self.filecontent.
    def createToken(self,token):
        self.TokenList.append(Token(token))

if __name__ == "__main__":
    print TokenGrammar.knowntokens
    if len(sys.argv) == 1:
        t = Tokenizer("program.lang")
    elif len(sys.argv) == 2:
        t = Tokenizer(sys.argv[1])
    else:
        print """ python token.py """