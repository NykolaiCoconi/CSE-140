#Where we are reading the machine code from. Changed later to user input
filename = "sample_part1.txt"

#Create global variables pc, hi, and lo
pc = next_pc = hi = lo = "0x0"

#More Globals
total_clock_cycles = branch_target = jump_target = 0
current_machine_code = op_name = instruction_type = ""
rs = rt = rd = shamt = imm = funct = physical_address = ""

#Control Switches
RegWrite = RegDst = Branch = ALUSrc = InstType = MemWrite = MemtoReg = MemRead = Jump = 0

registerfile = [0] * 32

#Putting these in so we can use actual hex values to get the key to to d-mem

#Got rid of type decoder definitions, only need decoder


def Decode():
    global op_name, instruction_type, jump_target, rs, rt, rd, shamt, imm, funct, physical_address

    machine_instruction = current_machine_code
    #PARSING "OPCODE" STRING'S FIRST 6 CHARACTERS AND THEN CONVERTING IT TO HEX VIA BUILT IN FUNCTIONS TO CONTINUE ON AND PASS ON TO MORE FUNCTIONS
    opcode = machine_instruction[:6]
    #this is for funct specifically
    funct = machine_instruction[-6:]
    opcode_hex = hex(int(opcode,2))
    #this is to turn funct into hex to compare with data frame
    funct_hex = hex(int(funct,2))
    '''
    Essentially made a data frame with two columns, operation name and op(hex), or for r type: operation name and funct(hex)"
    '''
    I_Dict = {    
            '0x8':'addi','0x9':'addiu','0xc':'andi','0x4':'beq','0x5':'bne','0x24':'lbu','0x25':'lhu',
            '0x30':'ll','0xf':'lui','0x23':'lw','0xd':'ori','0xa':'slti','0xb':'sltiu','0x28':'sb',
            '0x38':'sc','0x29':'sh','0x2b':'sw'
    }
    R_Dict = {
            '0x20':'add','0x21':'addu','0x24':'and','0x8':'jr','0x27':'nor','0x25':'or','0x2a':'slt',
            '0x2b':'sltu','0x0':'sll','0x2':'srl','0x22':'sub','0x23':'subu'
    }
   
    op_name = ""
    instruction_type = ""
    #0 is operation name and column 1 is hex value of opcode for I type and j type and column 1 is funct in hex if r type

    if opcode_hex == hex(0):
        for key in R_Dict:
            if funct_hex == key:
                op_name = R_Dict[key]
                instruction_type = "R"
    if opcode_hex == hex(2) and instruction_type == "":
        instruction_type="J"
        op_name = "j"
    if opcode_hex == hex(3) and instruction_type == "":
        instruction_type="J"
        op_name = "jal"
    if instruction_type == "":
        for key in I_Dict:
            if opcode_hex == key:
                op_name = I_Dict[key]
                instruction_type = "I"
        if instruction_type == "":
            instruction_type="N/A"
            op_name = "N/A"
           
    ControlUnit()

    print("\nInstruction Type: " + instruction_type)   
    print("Operation: " + op_name) 
    
    if instruction_type == 'I':
        rs = machine_instruction[6:11]
        rt = machine_instruction[11:16]
        imm = machine_instruction[16:32]

        #Used for Sign Extension
        check = imm[0]
        if check == "0":
            physical_address = "0000" + imm
        else:
            physical_address = "1111" + imm
        


    if instruction_type == 'J':
        imm = machine_instruction[-26:]
        
        #Shift-Left-2: 
        print(next_pc)
        jump_target = next_pc + imm + "00" #Very Confused Here
        print(jump_target)


        

    if instruction_type == 'R':
        rs = machine_instruction[6:11]
        rt = machine_instruction[11:16]
        rd = machine_instruction[16:21]
        shamt = machine_instruction[21:26]
        funct = machine_instruction[-6:]
        
    
    


#Semi-working, got confused on what they want here, but there is a basic setup to get back the
#correct code to the main program
#Fixed my confusion, no need for any logic here, that is later

def Fetch():
    global current_machine_code, pc, next_pc
    current_machine_code = machine_codes[int(pc,16)]
    next_pc = hex(int(pc, 16) + int("0x4", 16))
    pc = hex(int(pc, 16) + int("0x4", 16))
    print(pc)
    return 

def Mem():



    return

def Writeback():



    return

#Control Unit Should be done, but the InstType is iffy cause in the slides there are two types
def ControlUnit():
    global RegWrite, RegDst, Branch, ALUSrc, InstType, MemWrite, MemtoReg, MemRead, Jump

    if instruction_type == "R":
        Branch = ALUSrc = MemWrite = MemtoReg = MemRead = Jump = 0
        RegWrite = RegDst = InstType = 1

    if instruction_type == "I":
        if op_name == 'lw':
            Branch = Jump = RegDst = InstType = MemWrite = 0
            ALUSrc = MemtoReg = MemRead = RegWrite = 1
        if op_name == 'sw':
            Branch = MemtoReg = MemRead = Jump = RegWrite = RegDst = InstType = 0
            ALUSrc = MemWrite = 1
        if op_name == 'beq':
            ALUSrc = MemWrite = MemtoReg = MemRead = Jump = RegWrite = RegDst = 0
            Branch = InstType = 1

    if instruction_type == "J":
        RegWrite = RegDst = Branch = ALUSrc = InstType = MemWrite = MemtoReg = MemRead = 0
        Jump = 1

    return    




def main():

    #Make d-mem for memory entries (global)
    global d_mem
    d_mem = {}
    for i in range(0,32):
        d_mem[i] = 0

    #print(d_mem)


    #Take filename and open into list
    global lines
    with open(filename) as file:
        lines = file.readlines()
    #print(lines)

    #Put list into int style opening where increments are by 4
    #Must be dictionary to have empty spaces
    global machine_codes
    machine_codes = {}
    j=0
    for i in range(0,len(lines)*4):
        if i%4 != 0:
            machine_codes[i] = ""
        else:
            machine_codes[i] = lines[j].strip()
            j = j + 1

    #print(machine_codes)

    #Loop where most of the code happens:
    for i in range(0,len(lines)):
        if lines[i] != "": 
            Fetch()
            Decode()
            
    


if __name__ == "__main__":
    main()