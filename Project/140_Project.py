#Create global variables pc, hi, and lo
pc = next_pc = hi = lo = 0

#More Globals
total_clock_cycles = branch_target = jump_target = 0
current_machine_code = op_name = instruction_type = ""
rs = rt = rd = shamt = imm = funct = sign_extension = ""

#Control Switches
MemtoReg = RegDst = "00"
RegWrite = Branch = ALUSrc = MemWrite = MemRead = Jump = 0
alu_op = "000"
alu_cntrl = "0000"

registerfile = d_mem = [0] * 32

#Putting these in so we can use actual hex values to get the key to to d-mem. Update: got rid of hex
#Got rid of type decoder definitions, only need decoder

def Decode():
    global op_name, instruction_type, jump_target, rs, rt, rd, shamt, imm, funct, sign_extension, branch_target

    #Reset Variables
    branch_target = jump_target = 0
    rs = rt = rd = shamt = imm = funct = sign_extension = ""

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
        
        rs = int(machine_instruction[6:11],2)
        rt = int(machine_instruction[11:16],2)
        imm = machine_instruction[16:32]

        #Used for Sign Extension
        check = imm[0]
        if check == "0":
            sign_extension = "0000000000000000" + imm
        else:
            sign_extension = "1111111111111111" + imm

        return
        


    if instruction_type == 'J':
        imm = machine_instruction[-26:]

        if op_name == 'jal':
            registerfile[31] = next_pc         #Set $ra to next_pc if jal
            Writeback(2, 0, 31, next_pc)
        
        #Expand next_pc into a 32 bit address
        next_pc_binary = bin(next_pc).replace("0b", "")
        while len(next_pc_binary) < 32:
            next_pc_binary = "0" + next_pc_binary

        #Take first 4 bits of next_pc
        significant_bits = next_pc_binary[:4]
        #Multiply the immediate by 4
        mult_imm = imm + "00"
        #Concatnate significant bits of next_pc and the immediate * 4
        jump_target_bin = significant_bits + mult_imm
        #Change binary to decimal for target address
        jump_target = int(jump_target_bin,2)
        print ("Jump Target: " + str(jump_target)) #Testing

        return


    if instruction_type == 'R':
        rs = int(machine_instruction[6:11],2)
        rt = int(machine_instruction[11:16],2)
        rd = int(machine_instruction[16:21],2)
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
    current_machine_code = machine_codes[(pc)]
    next_pc = pc + 4
    pc = pc + 4 #PC here is temporary, actual pc is chosen later
    print("Next PC: " + str(pc)) #Testing
    return 


def Execute():
    #Create a function named Execute() that executes computations with ALU. The register values
    #and sign-extended offset values retrieved/computed by Decode() function will be used for
    #computation.
    global alu_zero, branch_target, registerfile

    comp_result = 0

    #and
    if alu_cntrl == '0000':
        comp_result = registerfile[rs] & registerfile[rt]
        registerfile[rd] = comp_result
        Writeback(2,0,registerfile[rd],hex(comp_result))
        if comp_result == 0:
            alu_zero = 1
    #or
    if alu_cntrl == '0001':
        comp_result = registerfile[rs] | registerfile[rt]
        registerfile[rd] = comp_result
        Writeback(2,0,registerfile[rd],hex(comp_result))
        if comp_result == 0:
            alu_zero = 1
    #add
    if alu_cntrl == '0010':
        #SW
        if ALUSrc == 1 and MemWrite == 1:
            Mem()
            return
        #LW
        if MemtoReg == '01':
            Mem()
            return
        comp_result = registerfile[rs] + registerfile[rt]
        registerfile[rd] = comp_result
        Writeback(2,0,registerfile[rd],hex(comp_result))
        if comp_result == 0:
            alu_zero = 1
    #sub/beq
    if alu_cntrl == '0110':
        comp_result = registerfile[rs] - registerfile[rt]
        registerfile[rd] = comp_result
        Writeback(2,0,registerfile[rd],hex(comp_result))
        if comp_result == 0:
            alu_zero = 1
    #slt
    if alu_cntrl == '0111':
        if registerfile[rs] < registerfile[rt]:
            alu_zero = 1
        else:
            alu_zero = 0
        registerfile[rd] = hex(alu_zero)
        print(hex(alu_zero))
        Writeback(2,0,registerfile[rd],hex(alu_zero))
            
    #NOR
    if alu_cntrl == '1100':
        comp_result = ~(registerfile[rs] | registerfile[rt])
        registerfile[rd] = comp_result
        Writeback(2,0,registerfile[rd],hex(comp_result))
        if comp_result == 0:
            alu_zero = 1


   
    #offset_to_dec = int(sign_extension,10)
    #shift_left_offset = offset_to_dec * 4
    #branch_target = shift_left_offset + next_pc

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
        print(int(registerfile[rs],2)+int(sign_extension,2))
        registerfile[rt] = d_mem[int(registerfile[rs],2)+int(sign_extension,2)]
        #Writeback(2, 0, rt, d_mem[int(registerfile[rs],2)+int(sign_extension,2)])
    #store word
    # M[R[rs]+SignExtImm]=R[rt]    
    if MemWrite == 1:
        print(int(registerfile[rs],2)+int(sign_extension,2))
        d_mem[int(registerfile[rs],2)+int(sign_extension,2)] = registerfile[rt] 
        #Writeback(3, 0, (int(registerfile[rs],2)+int(sign_extension,2)), registerfile[rt])
    return

def Writeback(type, next, register, modification):
    global total_clock_cycles
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
        print(str(Register_Dict[register]) + " is modified to " + str(hex(modification)))
    if type == 3:
        print("memory " + register + " is modified to " + modification)
    if type == 4:
        total_clock_cycles = total_clock_cycles + 1
        print("\ntotal_clock_cycles "+ str(total_clock_cycles) + ":")
    

    return


#Control Unit Should be done, but the InstType is iffy cause in the slides there are two types
def ControlUnit():
    global RegWrite, RegDst, Branch, ALUSrc, MemWrite, MemtoReg, MemRead, Jump, alu_op, funct, alu_cntrl
    alu_op = "00"
    alu_cntrl = "0000"

    if instruction_type == "R":
        RegDst = "01"
        MemtoReg = "00"
        Branch = ALUSrc = MemWrite =  MemRead = Jump = 0
        RegWrite = 1
        alu_op = "10"   

    if instruction_type == "I":
        if op_name == 'lw':
            RegDst = "00"
            MemtoReg = "01"
            Branch = Jump = MemWrite = 0
            ALUSrc = MemRead = RegWrite = 1
            alu_op = "00"
        if op_name == 'sw':
            RegDst = "00"
            MemtoReg = "00"
            Branch = MemRead = Jump = RegWrite = 0
            ALUSrc = MemWrite = 1
            alu_op = "00"
        if op_name == 'beq':
            RegDst = "00"
            MemtoReg = "00"
            ALUSrc = MemWrite = MemRead = Jump = RegWrite = 0
            Branch = 1
            alu_op = "01"

    if instruction_type == "J":
        if op_name == "j":
            RegDst = "00"
            MemtoReg = "00"
            RegWrite = Branch = ALUSrc = MemWrite = MemRead = 0
            Jump = 1
            alu_op = "00"
        if op_name == "jal":
            RegDst = "10"
            MemtoReg = "10"
            Branch = ALUSrc = MemWrite = MemRead = 0
            RegWrite = Jump = 1
            alu_op = "00"
    
    #Take alu_op and funct of the opcode and get the alu_cntrl for execute to use
    if alu_op == "00":
        alu_cntrl = "0010"
    if alu_op == "01":
        alu_cntrl = "0110"
    if alu_op == "10":
        if funct == "100000":   #Add
            alu_cntrl = "0010"
        if funct == "100010":   #subtract
            alu_cntrl = "0110"
        if funct == "100100":   #and
            alu_cntrl = "0000"
        if funct == "100101":   #or
            alu_cntrl = "0001"
        if funct == "101010":   #slt
            alu_cntrl = "0111"
        if funct == "100111":   #nor
            alu_cntrl = "1100"

    return    




def main():
    global lines, total_clock_cycles, machine_codes
    filename = "sample_part1.txt" #Testing

    #filename = input("Enter the program file name to run: \n\n")

    #Take filename and open into list
    with open(filename) as file:
        lines = file.readlines()
    #print(lines)

    #Put list into int style opening where increments are by 4
    #Must be dictionary to have empty spaces
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
            Writeback(4, 0, 0, 0) #Clock Cycle Counter

            Fetch()
            Decode()
            Execute()
        

    print("\nprogram terminated: ")
    print("total execution time is " + str(total_clock_cycles) + " cylces")

if __name__ == "__main__":
    main()