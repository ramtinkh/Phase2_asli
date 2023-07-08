from scanner.Scanner import Scanner
from parsr.Grammar import Grammar
from codeGenerator.CodeGenerator import CodeGenerator

scanenr = Scanner()
a = None
c = CodeGenerator(scanenr.file_writer.addresses,scanenr.file_writer.mainAdd)
g = Grammar(scanenr, c)
# while a != 'end':
#      a = scanenr.run()
#      print(a)

scanenr.file_writer.file_writer_errors()
scanenr.file_writer.file_writer_symboltable()
scanenr.file_writer.file_writer_tokens()
print(44,c.pb)
print(11,c.stack)
g.make_error_file()
file1 = open("output.txt","w+")
programBlock=""
for i in range(len(c.pb)):
    programBlock+=f"{i}\t{c.pb[i]}\n"
file1.write(programBlock)
file1.close()
# a1 = g.diagrams[0].first_node
# a2 = a1.next[0]
# a3 = a2[0].next[0]
# print(a3[1].id)

# while True:
#     print(scanenr.get_token())
#     break
