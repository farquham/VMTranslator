#VM translator program for nand 2 tetris wk 7
import sys


# vm code file -> assembly symbolic code file
# initializes and uses parser and codewriter objects
def main():
    # initializes the parser object
    p = Parser(sys.argv[1])
    c = CodeWrit()
    c.setFileName(sys.argv[1])

    while p.hasMoreCommands() ==  True:
        if p.commandType() == "C_ARITHMETIC":
            c.writeArithmetic(p.arg1(), p.counter)
            p.advance()
        elif p.commandType() == "C_PUSH" or p.commandType() == "C_POP":
            c.WritePushPop(p.commandType(), p.arg1(), str(p.arg2()))
            p.advance()
        elif p.commandType() == "BLANK":
            p.advance()
        elif p.commandType() == "COMMENT":
            p.advance()
    if p.commandType() == "C_ARITHMETIC":
        c.writeArithmetic(p.arg1(), p.counter)
    elif p.commandType() == "C_PUSH" or p.commandType() == "C_POP":
        c.WritePushPop(p.commandType(), p.arg1(), str(p.arg2()))

    c.Close()


class Parser:
     # opens the input file and intializes the parser
     def __init__(self, filearg):
         file = open(filearg, 'r')
         self.lines = file.readlines()
         file.close()
         self.counter = 0
         self.line = (self.lines)[self.counter]

     # () -> Boolean
     # checks if the current line is not the final line
     def hasMoreCommands(self):
         if (self.counter == (len(self.lines)-1)):
             return False
         else:
             return True

     # __ -> __
     # advances the parser to the next line and clears the whitespace
     def advance(self):
         self.counter += 1
         self.line = (self.lines)[self.counter]
         self.line = (self.line).strip()

     # string -> string
     # determines what type of VM command it is
     def commandType(self):
         try:
            ct = ((self.line).split())[0]
         except IndexError:
             ct = (self.line)
         commanddic = {"add":"C_ARITHMETIC", "sub":"C_ARITHMETIC", "neg":"C_ARITHMETIC",
                       "eq":"C_ARITHMETIC", "gt":"C_ARITHMETIC", "lt":"C_ARITHMETIC",
                       "and":"C_ARITHMETIC", "or":"C_ARITHMETIC", "not":"C_ARITHMETIC",
                       "push":"C_PUSH", "pop":"C_POP", '':"BLANK", "//":"COMMENT"}
         return commanddic[ct]


     # __ -> string
     # returns parsed first argument of command
     def arg1(self):
         try:
             return ((self.line).split())[1]
         except IndexError:
             return (self.line)

     # __ -> int
     # returns parsed second argument of command
     def arg2(self):
         return int(((self.line).split())[2])


class CodeWrit:
     def _init__(self):
         check = 0

     def setFileName(self, fileName):
         nfilename = (fileName.split(".")[0]) + ".asm"
         self.newfile = open(nfilename, "w")

# translates arithmetic commands into the hack langauge
     def writeArithmetic(self, command, linenum):
         Arithdic = {"add":"@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nM=D+M\n",
                     "sub":"@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nM=M-D\n",
                     "neg":"@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M\nM=0\nM=M-D\n",
                     "eq":"@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nD=M-D\n@EQT"+str(linenum)+"\nD;JEQ\n@SP\nA=M-1\nM=0\n@EQF"+str(linenum)+"\n0;JMP\n(EQT"+str(linenum)+")\n@SP\nA=M-1\nM=-1\n(EQF"+str(linenum)+")\n",
                     "gt":"@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nD=M-D\n@GTT"+str(linenum)+"\nD;JGT\n@SP\nA=M-1\nM=0\n@GTF"+str(linenum)+"\n0;JMP\n(GTT"+str(linenum)+")\n@SP\nA=M-1\nM=-1\n(GTF"+str(linenum)+")\n",
                     "lt":"@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nD=M-D\n@LTT"+str(linenum)+"\nD;JLT\n@SP\nA=M-1\nM=0\n@LTF"+str(linenum)+"\n0;JMP\n(LTT"+str(linenum)+")\n@SP\nA=M-1\nM=-1\n(LTF"+str(linenum)+")\n",
                     "and":"@SP\nA=M\nD=M\n@SP\nA=M-1\nM=D&M\n",            #may stop working if placed after a push command
                     "or":"@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nM=D|M\n",      #may stop working if placed without a push command before
                     "not":"@SP\nA=M-1\nM=!M\n@SP\n"}
         self.newfile.write(Arithdic[command])

     # translates the push command into the hack langauge
     def WritePushPop(self, command, segment, index):
         segdic = {"constant":"SP", "local":"LCL", "argument":"ARG",
                   "this":"THIS", "that":"THAT", "temp":"5", "pointer":"3", "static":"16"}
         if command == "C_PUSH":
             if segment == "constant":
                 com = "@"+index+"\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
             elif segment == "temp" or segment == "pointer" or segment == "static":
                 com = "@"+index+"\nD=A\n@"+segdic[segment]+"\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
             else:
                 com = "@"+index+"\nD=A\n@"+segdic[segment]+"\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
         elif command == "C_POP":
             if segment == "temp" or segment == "pointer" or segment == "static":
                 com = "@"+index+"\nD=A\n@"+segdic[segment]+"\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
             else:
                 com = "@"+index+"\nD=A\n@"+segdic[segment]+"\nD=M+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
         self.newfile.write(com)

     # closes the translated file
     def Close(self):
         self.newfile.close()


if __name__ == "__main__":
    main()
