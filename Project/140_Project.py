#Where we are reading the machine code from. Changed later to user input
filename = "sample_part1.txt"

#Create global variables pc, hi, and lo
pc = 0
next_pc = 0
hi = 0
lo = 0

#More Globals
total_clock_cycles = branch_target = jump_target = 0
current_machine_code = op_name = instruction_type = " "

#Control Switches
RegWrite = RegDst = Branch = ALUSrc = InstType = MemWrite = MemtoReg = MemRead = Jump = 0

registerfile = [0] * 32

#Got rid of type decoder definitions, only need decoder

def Decode():
    global op_name, instruction_type

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
   
    op_name = " "
    instruction_type = " "
    #0 is operation name and column 1 is hex value of opcode for I type and j type and column 1 is funct in hex if r type

    if opcode_hex == hex(0):
        for key in R_Dict:
            if funct_hex == key:
                op_name = R_Dict[key]
                instruction_type = "R"
    if opcode_hex == hex(2) and instruction_type == " ":
        instruction_type="J"
        op_name = "j"
    if opcode_hex == hex(3) and instruction_type == " ":
        instruction_type="J"
        op_name = "jal"
    if instruction_type == " ":
        for key in I_Dict:
            if opcode_hex == key:
                op_name = I_Dict[key]
                instruction_type = "I"
        if instruction_type == " ":
            instruction_type="N/A"
            op_name = "N/A"
           
    
    print("\nInstruction Type: " + instruction_type)   
    print("Operation: " + op_name) 
    
    if instruction_type == 'I':
        rs = machine_instruction[6:11]
        rt = machine_instruction[11:16]
        imm = machine_instruction[16:32]
        print("Rs: $",end = "")
        print(int(rs,2))
        print("Rt: $",end="") 
        print(int(rt,2))
        print("Immediate: ",end="") 
        print(int(imm,2), end=" ") 
        print("or (", end = "")
        print(hex(int(imm,2)), end = "") 
        print(")")

    if instruction_type == 'J':
        imm = machine_instruction[-26:]
        print("Immediate: ",end="")
        print(int(imm,2), end=" ") 
        print("or (", end = "")
        print(hex(int(imm,2)), end = "") 
        print(")")

    if instruction_type == 'R':
        rs = machine_instruction[6:11]
        rt = machine_instruction[11:16]
        rd = machine_instruction[16:21]
        shamt = machine_instruction[21:26]
        funct = machine_instruction[-6:]
        print("Rs: $",end = "")
        print(int(rs,2))
        print("Rt: $",end = "")
        print(int(rt,2))
        print("Rd: $",end = "")
        print(int(rd,2))
        print("Shamt: ",end = "")
        print(int(shamt,2))
        print("Funct: ",end = "")
        print(int(funct,2),end = "")
        print(" or (", end = "")
        print(hex(int(funct,2)), end = "")
        print(")")
    
    


#Semi-working, got confused on what they want here, but there is a basic setup to get back the
#correct code to the main program
#Fixed my confusion, no need for any logic here, that is later

def Fetch():
    global current_machine_code, pc, next_pc
    current_machine_code = machine_codes[pc]
    next_pc = pc + 4
    return 

def Mem():



    return

def Writeback():



    return

def ControlUnit():



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
            
    


if __name__ == "__main__":
    main()