import tokenizer
from preproc import preproc

code = tokenizer.readFile("C:\\Users\\Josh\\Desktop\\Code\\Language\\program1.lang")
code = preproc(code)
result = tokenizer.tokenize(code,"all")
        
print(tokenizer.printTokens(result))
