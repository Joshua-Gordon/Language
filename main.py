import tokenizer
from preproc import preproc

code = tokenizer.readFile("C:\\Users\\Josh\\Desktop\\Code\\Language\\program1.lang")
code = preproc(code)
print(code)
result = tokenizer.tokenize(code,"all")
print(result)
refined = tokenizer.refineTokens(result)
        
for t in refined: print(t)
