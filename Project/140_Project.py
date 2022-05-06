#Create global variables for pc
pc = next_pc = 0
#More Globals
total_clock_cycles = branch_target = jump_target = 0
current_machine_code = op_name = instruction_type = ""
rs = rt = rd = shamt = imm = funct = sign_extension = ""
end_check = 0
#Control Switches
MemtoReg = RegDst = "00"
RegWrite = Branch = ALUSrc = MemWrite = MemRead = Jump = 0
alu_op = "000"
alu_cntrl = "0000"
#Register and d_mem
registerfile = ['0x0'] * 32
d_mem = { 
            '0x00':'0x0', '0x04':'0x0','0x08':'0x0','0x0c':'0x0','0x10':'0x0',
            '0x14':'0x0','0x18':'0x0','0x1c':'0x0','0x20':'0x0','0x24':'0x0',
            '0x28':'0x0','0x2c':'0x0','0x30':'0x0','0x34':'0x0','0x38':'0x0',
            '0x3c':'0x0','0x40':'0x0','0x44':'0x0','0x48':'0x0','0x4c':'0x0',
            '0x50':'0x0','0x54':'0x0','0x58':'0x0','0x5c':'0x0','0x60':'0x0',
            '0x64':'0x0','0x68':'0x0','0x6c':'0x0','0x70':'0x0','0x74':'0x0',
            '0x78':'0x0','0x7c':'0x0'
        }
#Putting these in so we can use actual hex values to get the key to d-mem.

def Decode():
    global op_name, instruction_type, jump_target, rs, rt, rd, shamt, imm, funct 
    global sign_extension, branch_target
    #Reset Variables
    branch_target = jump_target = 0
    rs = rt = rd = shamt = imm = funct = sign_extension = ""
    #Set local variable from the global
    machine_instruction = current_machine_code
    #PARSING "OPCODE" STRING'S FIRST 6 CHARACTERS AND THEN CONVERTING IT 
    #TO HEX VIA BUILT IN FUNCTIONS TO CONTINUE ON AND PASS ON TO MORE FUNCTIONS
    opcode = machine_instruction[:6]
    funct = machine_instruction[-6:] #this is for funct specifically
    #Turn opcode and funct to hex
    opcode_hex = hex(int(opcode,2))
    funct_hex = hex(int(funct,2))
    '''
    Essentially made a data frame with two columns, operation name and op(hex), or     
    for r type: operation name and funct(hex)"
    '''
    I_Dict = {                   
        '0x8':'addi','0x9':'addiu','0xc':'andi','0x4':'beq','0x5':'bne',
        '0x24':'lbu','0x25':'lhu','0x30':'ll','0xf':'lui','0x23':'lw',
        '0xd':'ori','0xa':'slti','0xb':'sltiu','0x28':'sb','0x38':'sc',
        '0x29':'sh','0x2b':'sw'
    }
    R_Dict = {     
        '0x20':'add','0x21':'addu','0x24':'and','0x8':'jr','0x27':'nor',
        '0x25':'or','0x2a':'slt','0x2b':'sltu','0x0':'sll','0x2':'srl',
        '0x22':'sub','0x23':'subu'
    }
    #Clear opname and instruction type
    op_name = ""
    instruction_type = ""
    #0 is operation name and column 1 is hex value of opcode for I type and j type 
    #and column 1 is funct in hex if r type
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
    #Run Control Unit for flags       
    ControlUnit()
    #print("\nInstruction Type: " + instruction_type)    #Testing
    #print("Operation: " + op_name)                      #Testing
    #Decode 
    if instruction_type == 'I':
        rs = int(machine_instruction[6:11],2)
        rt = int(machine_instruction[11:16],2)
        imm = machine_instruction[16:32]
        #Used for Sign Extension
        check = imm[0]
        #Sign Extend
        if check == "0":
            sign_extension = "0000000000000000" + imm
        else:
            sign_extension = "1111111111111111" + imm
        return
    if instruction_type == 'J':
        imm = machine_instruction[-26:]
        #Expand next_pc into a 32 bit address
        next_pc_binary = bin(next_pc).replace("0b", "")
        while len(next_pc_binary) < 32:
            next_pc_binary = "0" + next_pc_binary
        #Take first 4 bits of next_pc
        significant_bits = next_pc_binary[:4]
        #Multiply the immediate by 4
        mult_imm = imm + "00"
        #Concatenate significant bits of next_pc and the immediate * 4
        jump_target_bin = significant_bits + mult_imm
        #Change binary to decimal for target address
        jump_target = int(jump_target_bin,2)
        #print ("Jump Target: " + str(jump_target)) #Testing
        return
    if instruction_type == 'R':
        rs = int(machine_instruction[6:11],2)
        rt = int(machine_instruction[11:16],2)
        rd = int(machine_instruction[16:21],2)
        shamt = machine_instruction[21:26]
        funct = machine_instruction[-6:]
        return
    return

def Fetch(type):
    global current_machine_code, pc, next_pc, end_check
    if type == 0:       #Fetch: make 0 the pc for first mips instruction
        pc = 0
    if type == 1:       #Fetch: make next_pc the pc, standard fetch
        pc = next_pc
    if type == 2:       #Fetch: make jump target the pc, for jal and j
        pc = jump_target
    if type == 3:       #Fetch: make branch target the pc, for beq
        #print(branch_target)   #Testing
        pc = branch_target
    if type == 4:       #Fetch: make $ra the pc, for ra
        pc = registerfile[31]
    #This checks to make sure it doesn't run on empty mips code
    if pc >= len(machine_codes) or machine_codes[pc] == "":
        end_check = 1
    if end_check == 0:
        current_machine_code = machine_codes[pc]
        next_pc = pc + 4
        #print("") #Testing
    #Writeback what the pc was changed to
    if type != 0:
        Writeback(1, pc, 0, 0)
    #print("Current PC: " + str(pc)) #Testing
    #print("Next PC: " + str(next_pc)) #Testing
    return 

def Execute():
    #Create a function named Execute() that executes computations with ALU. The register values
    #and sign-extended offset values retrieved/computed by Decode() function will be used for
    #computation.
    global alu_zero, branch_target, registerfile
    comp_result = 0
    #and
    if alu_cntrl == '0000':
        if RegDst == "01" and MemtoReg == "00" and Branch == ALUSrc == MemWrite ==  MemRead == Jump == 0 and RegWrite == 1:
            comp_result = int(registerfile[rs],16) & int(registerfile[rt],16)
            registerfile[rd] = hex(comp_result)
            Writeback(2,0,rd,hex(comp_result))
            if comp_result == 0:
                alu_zero = 1
    #or
    if alu_cntrl == '0001':
        if RegDst == "01" and MemtoReg == "00" and Branch == ALUSrc == MemWrite ==  MemRead == Jump == 0 and RegWrite == 1:
            comp_result = int(registerfile[rs],16) | int(registerfile[rt],16)
            registerfile[rd] = hex(comp_result)
            Writeback(2,0,rd,hex(comp_result))
            if comp_result == 0:
                alu_zero = 1
    #add
    if alu_cntrl == '0010':
        #Jal
        if RegDst == "10" and MemtoReg == "10" and Branch == ALUSrc == MemWrite == MemRead == 0 and RegWrite == Jump == 1:
            registerfile[31] = next_pc         #Set $ra to next_pc
            Writeback(2, 0, 31, hex(next_pc))
            Fetch(2)
            return
        #J
        if RegDst == "00" and MemtoReg == "00" and RegWrite == Branch == ALUSrc == MemWrite == MemRead == 0 and Jump == 1:
            Fetch(2)
            return
        #SW
        if RegDst == "00" and MemtoReg == "00" and Branch == MemRead == Jump == RegWrite == 0 and ALUSrc == MemWrite == 1:
            Mem()
            Fetch(1)
            return
        #LW
        if RegDst == "00" and MemtoReg == "01" and Branch == Jump == MemWrite == 0 and ALUSrc == MemRead == RegWrite == 1:
            Mem()
            Fetch(1)
            return
        #Add
        if RegDst == "01" and MemtoReg == "00" and Branch == ALUSrc == MemWrite ==  MemRead == Jump == 0 and RegWrite == 1:
            comp_result = int(registerfile[rs],16) + int(registerfile[rt],16)
            registerfile[rd] = hex(comp_result)
            Writeback(2,0,rd,hex(comp_result))
            if comp_result == 0:
                alu_zero = 1
    #sub/beq
    if alu_cntrl == '0110':
        comp_result = int(registerfile[rs],16) - int(registerfile[rt],16)
        #Sub
        if RegDst == "01" and MemtoReg == "00" and Branch == ALUSrc == MemWrite ==  MemRead == Jump == 0 and RegWrite == 1:
            registerfile[rd] = hex(comp_result)
            Writeback(2,0,rd,hex(comp_result))
        #Beq
        if comp_result == 0 and RegDst == "00" and MemtoReg == "00" and ALUSrc == MemWrite == MemRead == Jump == RegWrite == 0 and Branch == 1:
            offset_to_dec = int(sign_extension,2)
            shift_left_offset = offset_to_dec * 4
            alu_zero = 1
            branch_target = shift_left_offset + next_pc
            Fetch(3)
            return      
    #slt
    if alu_cntrl == '0111':
        if RegDst == "01" and MemtoReg == "00" and Branch == ALUSrc == MemWrite ==  MemRead == Jump == 0 and RegWrite == 1:
            if int(registerfile[rs],16) < int(registerfile[rt],16):
                alu_zero = 1
            else:
                alu_zero = 0
            registerfile[rd] = hex(alu_zero)
            #print(hex(alu_zero)    #Testing
            Writeback(2,0,rd,hex(alu_zero))         
    #NOR
    if alu_cntrl == '1100':
        if RegDst == "01" and MemtoReg == "00" and Branch == ALUSrc == MemWrite ==  MemRead == Jump == 0 and RegWrite == 1:
            comp_result = ~(int(registerfile[rs],16) | int(registerfile[rt],16))
            registerfile[rd] = hex(comp_result)
            Writeback(2,0,rd,hex(comp_result))
            if comp_result == 0:
                alu_zero = 1
    #jr
    if alu_cntrl == '0011':
        if RegDst == "01" and MemtoReg == "00" and Branch == ALUSrc == MemWrite ==  MemRead == Jump == 0 and RegWrite == 1:
            Fetch(4)
            return
    Fetch(1)
    return

def Mem():
    global d_mem, registerfile, RegWrite, RegDst, Branch, ALUSrc, MemWrite, MemtoReg, MemRead
    global sign_extension, rt, rd, rs
    #load word
    # R[rt] = M[R[rs]+SignExtImm]
    if RegDst == alu_op == "00" and MemtoReg == "01" and Branch == Jump == MemWrite == 0 and ALUSrc == MemRead == RegWrite == 1:
        registerfile[rt] = d_mem[hex(int(registerfile[rs],16)+int(sign_extension,2))]
        #Writeback change to register files
        Writeback(2,0,rt,d_mem[hex(int(registerfile[rs],16)+int(sign_extension,2))])
    #store word
    # M[R[rs]+SignExtImm]=R[rt]    
    if RegDst == alu_op == MemtoReg == "00" and Branch == MemRead == Jump == RegWrite == 0 and ALUSrc == MemWrite == 1:
        d_mem[hex(int(registerfile[rs],16)+int(sign_extension,2))] = registerfile[rt] 
        #Writeback change to d_mem
        Writeback(3,0,(hex(int(registerfile[rs],16)+int(sign_extension,2))),registerfile[rt])
    return

def Writeback(type, next, register, modification):
    global total_clock_cycles
    #Dictionary for easier writing of the register file updated
    Register_Dict = {    
            '0':'$zero','1':'$at','2':'$v0','3':'$v1','4':'$a0',
            '5':'$a1','6':'$a2','7':'$a3','8':'$t0','9':'$t1',
            '10':'$t2','11':'$t3','12':'$t4','13':'$t5','14':'$t6',
            '15':'$t7','16':'$s0', '17':'$s1','18':'$s2','19':'$s3',
            '20':'$s4','21':'$s5', '22':'$s6','23':'$s7','24':'$t8',
            '25':'$t9','26':'$k0','27':'$k1','28':'$gp','29':'$sp',
            '31':'$fp', '31':'$ra'
    }
    if type == 1:       #Writing out the pc modification
        print("pc is modified to " + hex(next))
    if type == 2:       #Writing out the register modification
        print(Register_Dict[str(register)]+ " is modified to " + modification)
    if type == 3:       #Writing out the memory modification
        print("memory " + register + " is modified to " + modification)
    if type == 4:       #Writing out the current clock cycle
        total_clock_cycles = total_clock_cycles + 1
        print("\ntotal_clock_cycles "+ str(total_clock_cycles) + ":")
    return

def ControlUnit():
    global RegWrite, RegDst, Branch, ALUSrc, MemWrite, MemtoReg, MemRead, Jump, alu_op, funct, alu_cntrl
    #Reset alu op and control
    alu_op = "00"
    alu_cntrl = "0000"
    if instruction_type == "R":     #Set R type flags
        RegDst = "01"
        MemtoReg = "00"
        Branch = ALUSrc = MemWrite =  MemRead = Jump = 0
        RegWrite = 1
        alu_op = "10"
    if instruction_type == "I":     #Set I type flags
        #LW
        if op_name == 'lw':
            RegDst = "00"
            MemtoReg = "01"
            Branch = Jump = MemWrite = 0
            ALUSrc = MemRead = RegWrite = 1
            alu_op = "00"
        #SW  
        if op_name == 'sw':
            RegDst = "00"
            MemtoReg = "00"
            Branch = MemRead = Jump = RegWrite = 0
            ALUSrc = MemWrite = 1
            alu_op = "00"
        #Beq
        if op_name == 'beq':
            RegDst = "00"
            MemtoReg = "00"
            ALUSrc = MemWrite = MemRead = Jump = RegWrite = 0
            Branch = 1
            alu_op = "01"
    if instruction_type == "J":     #Set J type flags
        #J    
        if op_name == "j":
            RegDst = "00"
            MemtoReg = "00"
            RegWrite = Branch = ALUSrc = MemWrite = MemRead = 0
            Jump = 1
            alu_op = "00"
        #Jal
        if op_name == "jal":
            RegDst = "10"
            MemtoReg = "10"
            Branch = ALUSrc = MemWrite = MemRead = 0
            RegWrite = Jump = 1
            alu_op = "00"
    #Take alu_op and funct of the opcode and get the alu_cntrl for execute to use
    if alu_op == "00":
        alu_cntrl = "0010"  #jump, jump/link, sw, lw
    if alu_op == "01":
        alu_cntrl = "0110"  #beq
    if alu_op == "10":
        if funct == "100000":   #add
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
        if funct == "001000":   #jr
            alu_cntrl = "0011"
    return    

def main():
    global lines, total_clock_cycles, machine_codes, registerfile, d_mem
    #filename = "sample_part2.txt" #Testing
    #Get user input for filename
    filename = input("Enter the program file name to run: \n\n")
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
    #Set up prefilled variables
    if filename == "sample_part1.txt":
        #register presets
        registerfile[9] = '0x20'
        registerfile[10] = '0x5'
        registerfile[16] = '0x70'
        #d_mem presets
        d_mem['0x70'] = '0x5'
        d_mem['0x74'] = '0x10'
    if filename == "sample_part2.txt":
        #register presets
        registerfile[16] = '0x20'
        registerfile[4] = '0x5'
        registerfile[5] = '0x2'
        registerfile[7] = '0xa'
    #Loop where the code happens:
    #Get first binary line, all others will be chosen in 
    #execute and choice sent to fetch
    Fetch(0)
    while end_check == 0:  
        Writeback(4, 0, 0, 0) #Clock Cycle Counter
        Decode()
        Execute()
    #Code ending where it prints the total cycles
    print("\nprogram terminated: ")
    print("total execution time is " + str(total_clock_cycles) + " cylces")
    #print(d_mem)
if __name__ == "__main__":
    main()
