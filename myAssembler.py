start=""
while start[:11] != "myAssembler": # if the starting word is not "myAssembler", we keep taking input until it is.
    start=input()

start = start[12:]+".asm"

############################## 
inputList = [line.rstrip() for line in open(start)] # stores every line from the .asm file as a list in inputList

# Removing all the comments from our code, i.e. everything in a line written after #
for i in range(len(inputList)):
    for j in range(len(inputList[i])):
        if inputList[i][j] == "#":
            inputList[i] = inputList[i][:j]
            inputList[i] = inputList[i].strip() # removes all the white spaces
            break
############################## 

############################## 
register = {"$zero":0,"$at":1,"$v0":2,"$v1":3,"$a0":4,"$a1":5,"$a2":6,"$a3":7,"$t0":8,"$t1":9,"$t2":10,"$t3":11,"$t4":12,"$t5":13,"$t6":14,"$t7":15,"$s0":16,"$s1":17,"$s2":18,"$s3":19,"$s4":20,"$s5":21,"$s6":22,"$s7":23,"$t8":24,"$t9":25,"$k0":26,"$k1":27,"$gp":28,"$sp":29,"$fp":30,"$ra":31}

rTypes = ["add","addu","and","nor","or","slt","sltu","sub","subu"]
iTypes = ["addi","addiu","andi","ori","slti","sltiu"]
offsetTypes = ["lbu","lhu","ll","lw","sb","sc","sh","sw"]
shiftTypes = ["sll","srl"]
############################## 

############################## 
#### Functions to check syntax ####
allRegisters = ["$zero","$at","$v0","$v1","$a0","$a1","$a2","$a3","$t0","$t1","$t2","$t3","$t4","$t5","$t6","$t7","$s0","$s1","$s2","$s3","$s4","$s5","$s6","$s7","$t8","$t9","$k0","$k1","$gp","$sp","$fp","$ra","$0","$1","$2","$3","$4","$5","$6","$7","$8","$9","$10","$11","$12","$13","$14","$15","$16","$17","$18","$19","$20","$21","$22","$23","$24","$25","$26","$27","$28","$29","$30","$31"]

def registerSyntaxCheck(reg):
    if reg not in allRegisters:
        return True # True if synatx is wrong
    else:
        return False # False if synatx is right

def constantSyntaxCheck(cons):
    if cons[:2] != "0x" and cons.strip('-').isnumeric() == False: # checks if the first argument is either a hex number or number, or a -ve number
        return True # True if synatx is wrong
    else:
        return False # False if synatx is right
#### Functions to check syntax ####

#### Mathematical Functions ####
# Function converts decimal num into binary number, by adding extra zeroes upto the specified number of digits (dig)
def decToBin(num, dig):
    temp = bin(num).replace("0b", "")
    while dig > len(temp):
        temp = "0" + temp
    return temp

# If the hex number is less than 8 bits, this function will make it 8 bits by adding extra zeroes into it
def eightBitHex(hex):
    temp = hex
    while len(temp)<10:
        temp = temp.replace("0x","0x0")
    return temp

# Function converts binary num into hexadecimal
def binToHex(num):
    n = int(num, 2) # in-built function to convert binary into decimal
    m = hex(n) # in-built function to convert decimal into hexadecimal
    return(m)

# Function returns the two's compliment of input binary num
def negative(num):
    temp = ""
    
    # Firstly, we invert the num binary string and store the new string in temp
    for i in num:
        if i == "0":
            temp = temp + "1"
        else:
            temp = temp + "0"

    # Now, we store the string "temp" as a list in x 
    tempList = [i for i in temp]

    # Now, to add 1 to the binary num, we carry out binary addition
    for i in range(len(temp)-1,-1,-1):
        if tempList[i] == "0":
            tempList[i] = "1"
            break
        tempList[i] = "0"

    return ''.join(tempList)
#### Mathematical Functions ####

#### Functions to calculate assembled binary code ####
def calculateRtype(x):
    # Opcode + rd + rs + rt + shamt + func
    # "000000" + 5bits + 5bits + 5bits + "00000" + 6bits

    rd, rt, rs = "", "", ""
    temp = x.args

    if temp[0] in register: # if the register is a named register,
        rd = decToBin(register[temp[0]], 5) # we simply get its number using the register dictionary, and store its 5 bit binary number in rd,
    else: # else we remove the $ and store the 5 bit binary of the number left.
        rd = decToBin(int(temp[0][1:]), 5)
    
    if temp[1] in register: # if the register is a named register,
        rs = decToBin(register[temp[1]], 5) # we simply get its number using the register dictionary, and store its 5 bit binary number in rs,
    else: # else we remove the $ and store the 5 bit binary of the number left.
        rs = decToBin(int(temp[1][1:]), 5)
    
    if temp[2] in register: # if the register is a named register,
        rt = decToBin(register[temp[2]], 5) # we simply get its number using the register dictionary, and store its 5 bit binary number in rt,
    else: # else we remove the $ and store the 5 bit binary of the number left.
        rt = decToBin(int(temp[2][1:]), 5)

    if(x.name == "add"):
        return("000000" + rs + rt + rd + "00000" + "100000")
    elif(x.name == "addu"):
        return("000000" + rs + rt + rd + "00000" + "100001")
    elif(x.name == "and"):
        return("000000" + rs + rt + rd + "00000" + "100100")
    elif(x.name == "nor"):
        return("000000" + rs + rt + rd + "00000" + "100111")
    elif(x.name == "or"):
        return("000000" + rs + rt + rd + "00000" + "100101")
    elif(x.name == "slt"):
        return("000000" + rs + rt + rd + "00000" + "101010")
    elif(x.name == "sltu"):
        return("000000" + rs + rt + rd + "00000" + "101011")
    elif(x.name == "sub"):
        return("000000" + rs + rt + rd + "00000" + "100010")
    elif(x.name == "subu"):
        return("000000" + rs + rt + rd + "00000" + "100011")
    
def calculateIOtype(x):
    # Opcode + rs + rt + Immediate
    # 6bits + 5bits + 5bits + 16bits

    rt, rs, immediate = "", "", ""
    temp = x.args

    if temp[0] in register: # if the register is a named register,
        rt = decToBin(register[temp[0]], 5) # we simply get its number using the register dictionary, and store its 5 bit binary number in rt,
    else: # else we remove the $ and store the 5 bit binary of the number left.
        rt = decToBin(int(temp[0][1:]), 5)
    
    if temp[1] in register: # if the register is a named register,
        rs = decToBin(register[temp[1]], 5) # we simply get its number using the register dictionary, and store its 5 bit binary number in rs,
    else: # else we remove the $ and store the 5 bit binary of the number left.
        rs = decToBin(int(temp[1][1:]), 5)
    
    if temp[2][:2] == "0x":
        immediate = decToBin(int(temp[2][2:], 16), 16)
    elif temp[2][:1] == "-":
        immediate = negative(decToBin(int(temp[2][1:]), 16))
    else:
        immediate = decToBin(int(temp[2]), 16)

    if(x.name == "addi"):
        return("001000" + rs + rt + immediate) 
    elif(x.name == "addiu"):
        return("001001" + rs + rt + immediate)
    elif(x.name == "andi"):
        return("001100" + rs + rt + immediate)
    elif(x.name == "ori"):
        return("001101" + rs + rt + immediate)
    elif(x.name == "slti"):
        return("001010" + rs + rt + immediate)
    elif(x.name == "sltiu"):
        return("001011" + rs + rt + immediate)
    elif(x.name == "lbu"):
        return("100100" + rs + rt + immediate)
    elif(x.name == "lhu"):
        return("100101" + rs + rt + immediate)
    elif(x.name == "ll"):
        return("110000" + rs + rt + immediate)
    elif(x.name == "lw"):
        return("100011" + rs + rt + immediate)
    elif(x.name == "sb"):
        return("101000" + rs + rt + immediate)
    elif(x.name == "sc"):
        return("111000" + rs + rt + immediate)
    elif(x.name == "sh"):
        return("101001" + rs + rt + immediate)
    elif(x.name == "sw"):
        return("101011" + rs + rt + immediate)

def calculateStype(x):
    # Opcode + rd + rs + rt + shamt + func
    # "000000" + "00000" + 5bits + 5bits + 5bits + 6bits

    rd, rt, shamt = "", "", ""
    temp = x.args

    if temp[0] in register: # if the register is a named register,
        rd = decToBin(register[temp[0]], 5) # we simply get its number using the register dictionary, and store its 5 bit binary number in rd,
    else: # else we remove the $ and store the 5 bit binary of the number left.
        rd = decToBin(int(temp[0][1:]), 5)
    
    if temp[1] in register: # if the register is a named register,
        rt = decToBin(register[temp[1]], 5) # we simply get its number using the register dictionary, and store its 5 bit binary number in rt,
    else: # else we remove the $ and store the 5 bit binary of the number left.
        rt = decToBin(int(temp[1][1:]), 5)
    
    if temp[2][:2] == "0x":
        shamt = decToBin(int(temp[2][2:], 16), 5)
    elif temp[2][:1] == "-":
        shamt = negative(decToBin(int(temp[2][1:]), 5))
    else:
        shamt = decToBin(int(temp[2]), 5)

    if(x.name == "sll"):
        return("000000" + "00000" + rt + rd + shamt + "000000")
    elif(x.name == "srl"):
        return("000000" + "00000" + rt + rd + shamt + "000010")

def calculateLui(x):
    # Opcode + rs + rt + Immediate
    # "001111" + "00000" + 5bits + 16bits

    rt, immediate = "", ""
    temp = x.args

    if temp[0] in register: # if the register is a named register,
        rt = decToBin(register[temp[0]], 5) # we simply get its number using the register dictionary, and store its 5 bit binary number in rt,
    else: # else we remove the $ and store the 5 bit binary of the number left.
        rt = decToBin(int(temp[0][1:]), 5)

    if temp[1][:2] == "0x":
        immediate = decToBin(int(temp[1][2:], 16), 16)
    elif temp[1][:1] == "-":
        immediate = negative(decToBin(int(temp[1][1:]), 16))
    else:
        immediate = decToBin(int(temp[1]), 16)

    return("001111" + "00000" + rt + immediate)
#### Functions to calculate assembled binary code ####
##############################

##############################
# To store the label, name and arguments(registers and immediates) of every MIPS instruction, we make this class named "instruction"
class instruction():
    def __init__(self, labels, name, args):
        self.labels = labels
        self.name = name
        self.args = args

instructionList = [] # this list will store all the objects of 'instruction' class
assembledList = [] # this list will store the hexadecimal form of every instruction
##############################

##############################
# We read each instruction line one by one using this for loop
loopIndex = -1 # To count the number of interations for the loop below
for i in inputList:
    loopIndex = loopIndex + 1

    # we start by creating three temporary variables, to store the label, name and arguments of every instruction in a list as an object
    temp_label = "NULL" # this will be a string
    temp_name = "" # this will be a string
    temp_args = [] # this will be a list of strings
    
    ### this loop stores the label in temp_label
    for j in range(len(i)):
        if i[j] == ":": # if loop contains ":", everything before it is the label
            temp_label = i[:j] # store the label in temp_label
            inputList[loopIndex] = i[j+1:] # remove the label
            inputList[loopIndex] = inputList[loopIndex].strip() # remove extra white spaces
            i = inputList[loopIndex] # also make changes to the i variable for further modifications
            break
    # if there is no label, temp_label will remain NULL
    
    ### this loop stores the name of the instruction in temp_name
    for j in range(len(i)):
        if i[j] == " ": # as soon as we hit an empty space, we can say that everything before it was the name of the instruction
            temp_name = i[:j] # store the name in temp_name
            inputList[loopIndex] = i[j:] # remove the name
            inputList[loopIndex] = inputList[loopIndex].strip() # remove extra white spaces
            i = inputList[loopIndex] # also make changes to the i variable for further modifications
            break

    ## SYNTAX CHECKING : Instruction Name ##
    if temp_name not in rTypes and temp_name not in iTypes and temp_name not in offsetTypes and temp_name not in shiftTypes and temp_name != "lui":
        print("Cannot assemble the assembly code at line", (loopIndex + 1))
        input("Press ENTER to exit")
        exit(0)
    ## SYNTAX CHECKED ##

    ### now we split all the arguments separated by a comma and store it in the temp_args list
    # r-type instruction arguments are stored as : [$rd, $rs, $rt]
    # i-type instruction arguments are stored as : [$rt, $rs, immediate/offset]
    # shift instruction arguments are stored as : [$rd, $rt, shamt]
    # lui arguments are stored as : [$rt, immediate]
    temp_args = i.split(",") 
    
    for j in range(len(temp_args)): # remove extra white spaces
        temp_args[j] = temp_args[j].strip()

    # if the instruction is in offset(register) form, we need to separate that too
    if temp_name in offsetTypes:
        for j in range(len(temp_args[1])):
            if temp_args[1][j] == "(": # everything before the '(' will be the offset
                temp_args.append(temp_args[1][:j]) # appends the offset in the temp_args list
                temp_args[1] = temp_args[1][j+1:-1] # remove the offset and the brackets, to simply keep the register name
                break

    ## SYNTAX CHECKING : Instruction Arguments ##
    if temp_name in rTypes:
        if registerSyntaxCheck(temp_args[0]) or registerSyntaxCheck(temp_args[1]) or registerSyntaxCheck(temp_args[2]):
            print("Cannot assemble the assembly code at line", (loopIndex + 1))
            input("Press ENTER to exit")
            exit(0)

    elif temp_name in iTypes or temp_name in offsetTypes or temp_name in shiftTypes:
        if registerSyntaxCheck(temp_args[0]) or registerSyntaxCheck(temp_args[1]) or constantSyntaxCheck(temp_args[2]):
            print("Cannot assemble the assembly code at line", (loopIndex + 1))
            input("Press ENTER to exit")
            exit(0)

    else: # for lui
        if registerSyntaxCheck(temp_args[0]) or constantSyntaxCheck(temp_args[1]):
            print("Cannot assemble the assembly code at line", (loopIndex + 1))
            input("Press ENTER to exit")
            exit(0)
    ## SYNTAX CHECKED ##

    # now we add the label, name and argument of the current instruction as an object of class "instruction" into the list instructionList
    instructionList.append(instruction(temp_label, temp_name, temp_args))
##############################

##############################
# Now we calucalte and store hex version of every instruction in assembledList
for i in range(len(inputList)):
    
    if instructionList[i].name in rTypes:
        assembledBinary = calculateRtype(instructionList[i])

    elif instructionList[i].name in iTypes or instructionList[i].name in offsetTypes:
        assembledBinary = calculateIOtype(instructionList[i])
    
    elif instructionList[i].name in shiftTypes:
        assembledBinary = calculateStype(instructionList[i]) 

    elif instructionList[i].name == "lui":
        assembledBinary = calculateLui(instructionList[i])

    # converts the binary number into hexadecimal form, then makes it 8 bit by adding extra zeroes, then appends it into assembledList
    assembledList.append(eightBitHex(binToHex(assembledBinary)))
##############################

##############################
# Now we create a new text file and write all our assembled instructions in HEX in it
start = start[:-3] + "txt"
file1 = open(start, "a+")
for i in assembledList:
    file1.write(i + "\n")
file1.close()
##############################

print("File Created Successfully.")