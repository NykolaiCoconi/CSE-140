#Create global variables pc, hi, and lo
pc = next_pc = hi = lo = 0

#More Globals
total_clock_cycles = branch_target = jump_target = 0
current_machine_code = op_name = instruction_type = ""
rs = rt = rd = shamt = imm = funct = physical_address = ""

#Control Switches
RegWrite = RegDst = Branch = ALUSrc = MemWrite = MemtoReg = MemRead = Jump = 0
InstType = "00"

registerfile = d_mem = [0] * 32

#Putting these in so we can use actual hex values to get the key to to d-mem. Update: got rid of hex
#Got rid of type decoder definitions, only need decoder

def Decode():
    global op_name, instruction_type, jump_target, rs, rt, rd, shamt, imm, funct, physical_address, branch_target

    #Reset Variables
    branch_target = jump_target = 0
    rs = rt = rd = shamt = imm = funct = physical_address = ""

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
    
    #print("\nInstruction Type: " + instruction_type)    #Testing
    #print("Operation: " + op_name)                      #Testing
    
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

        branch_target = next_pc + (int(imm,2)*4)        #Can't use the special calulations you want cause the "addresses" are not addresses
        
        #print ("Branch Target: " + str(branch_target)) #Testing

        return
        


    if instruction_type == 'J':
        imm = machine_instruction[-26:]

        if op_name == 'jal':
            d_mem[31] = next_pc         #Set $ra to next_pc if jal
            Writeback(2, 0, 31, next_pc)
        
        jump_target = (int(imm,2)*4)    #Can't use the special calulations you want cause the "addresses" are not addresses
        #print (jump_target) #Testing
        return


    if instruction_type == 'R':
        rs = machine_instruction[6:11]
        rt = machine_instruction[11:16]
        rd = machine_instruction[16:21]
        shamt = machine_instruction[21:26]
        funct = machine_instruction[-6:]

        return
    
    return
    
    


#Semi-working, got confused on what they want here, but there is a basic setup to get back the
#correct code to the main program
#Fixed my confusion, no need for any logic here, that is later

def Fetch():
    global current_machine_code, pc, next_pc
    #print("") #Testing
    print("Current PC: " + str(pc)) #Testing
    current_machine_code = machine_codes[pc]
    next_pc = pc + 4
    pc = pc + 4 #PC here is temporary, actual pc is chosen later
    print("Next PC: " + str(pc)) #Testing
    return 


def Execute(alu_op,reg_val1,reg_val2,offset):
    #Create a function named Execute() that executes computations with ALU. The register values
    #and sign-extended offset values retrieved/computed by Decode() function will be used for
    #computation.

    global alu_zero, branch_target

    comp_result = 0
    
    if alu_op == '0000':
        comp_result = reg_val1 and reg_val2
    if alu_op == '0001':
        comp_result = reg_val1 or reg_val2
    if alu_op == '0010':
        comp_result = reg_val1 + reg_val2
        if comp_result <= 0:
            alu_zero = 1
    if alu_op == '0110':
        reg_val2 *= -1
        comp_result = reg_val1 + reg_val2
        if comp_result <= 0:
            alu_zero = 1
    if alu_op == '0111':
        comp_result = reg_val1 - reg_val2
        if comp_result < 0:
            alu_zero = 1


    offset_to_dec = int(offset,10)
    shift_left_offset = offset_to_dec * 4
    #need to do the last part
    # the last thing needed is " The
    #second step is to add the shift-left-2 output with the PC+4 value."
    #update this later(note to myself)
    #branch_target = shift_left_ofsset + value of PC+4

def Mem():
    global d_mem, registerfile

    #load word
    # R[rt] = M[R[rs]+SignExtImm]
    if MemtoReg == 1 and MemRead == 1:
        registerfile[rt] = d_mem[rs+physical_address]
        Writeback(2, 0, rt, d_mem[rs+physical_address])

    #store word
    # M[R[rs]+SignExtImm]=R[rt]    
    if MemWrite == 1:
        d_mem[rs+physical_address] = registerfile[rt] 
        Writeback(3, 0, (rs+physical_address), registerfile[rt])



    return

def Writeback(type, next, register, modification):
    Register_Dict = {    
            '0':'$zero','1':'$at','2':'$v0','3':'$v1','4':'$a0','5':'$a1','6':'$a2',
            '7':'$a3','8':'$t0','9':'$t1','10':'$t2','11':'$t3','12':'$t4','13':'$t5',
            '14':'$t6','15':'$t7','16':'$s0', '17':'$s1','18':'$s2','19':'$s3','20':'$s4',
            '21':'$s5', '22':'$s6','23':'$s7','24':'$t8','25':'$t9','26':'$k0','27':'$k1','28':'$gp',
            '29':'$sp','31':'$fp', '31':'$ra'
    }

    if type == 1:
        print("pc is modified to " + str(next))
    if type == 2:
        print(str(Register_Dict[str(register)]) + " is modified to " + str(hex(modification)))
    if type == 3:
        print("memory " + register + " is modified to " + modification)

    return


#Control Unit Should be done, but the InstType is iffy cause in the slides there are two types
def ControlUnit():
    global RegWrite, RegDst, Branch, ALUSrc, InstType, MemWrite, MemtoReg, MemRead, Jump

    if instruction_type == "R":
        Branch = ALUSrc = MemWrite = MemtoReg = MemRead = Jump = 0
        RegWrite = RegDst = 1
        InstType = "10"

    if instruction_type == "I":
        if op_name == 'lw':
            Branch = Jump = RegDst = MemWrite = 0
            ALUSrc = MemtoReg = MemRead = RegWrite = 1
            InstType = "00"
        if op_name == 'sw':
            Branch = MemtoReg = MemRead = Jump = RegWrite = RegDst = 0
            ALUSrc = MemWrite = 1
            InstType = "00"
        if op_name == 'beq':
            ALUSrc = MemWrite = MemtoReg = MemRead = Jump = RegWrite = RegDst = 0
            Branch = 1
            InstType = "01"

    if instruction_type == "J":
        RegWrite = RegDst = Branch = ALUSrc = MemWrite = MemtoReg = MemRead = 0
        Jump = 1
        InstType = "00"

    return    




def main():
    filename = "sample_part2.txt" #Testing

    #filename = input("Enter the program file name to run: \n\n")

    #Take filename and open into list
    global lines, total_clock_cycles
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

    #print(machine_codes) #Testing

    #Loop where most of the code happens:
    for i in range(0,len(lines)):
        if lines[i] != "":  
            #moved clock counter here so that it only updates at the beginning
            total_clock_cycles = total_clock_cycles + 1
            print("\ntotal_clock_cycles "+ str(total_clock_cycles) + ":")

            Fetch()
            Decode()
            #Execute()
        

    print("\nprogram terminated: ")
    print("total execution time is " + str(total_clock_cycles) + " cylces")

if __name__ == "__main__":
    main()