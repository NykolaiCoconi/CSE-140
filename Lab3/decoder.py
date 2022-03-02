
def iTypeDecoder(machine_instruction):
    rs = machine_instruction[6:11]
    print("Rs: $",end = "")
    print(int(rs,2))
    rt = machine_instruction[11:16]
    print("Rt: $",end="") 
    print(int(rt,2))
    imm = machine_instruction[16:32]
    print("Immediate: ",end="") 
    print(int(imm,2), end=" ") 
    print("or (", end = "")
    print(hex(int(imm,2)), end = "") 
    print(")")
    
    

def rTypeDecoder(machine_instruction):
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
    
    
def jTypeDecoder(machine_instruction):
    imm = machine_instruction[-26:]
    
    print("Immediate: ",end="")
    print(int(imm,2), end=" ") 
    print("or (", end = "")
    print(hex(int(imm,2)), end = "") 
    print(")")
    
    
def opCodeDecoder(machine_instruction):
    #PARSING "OPCODE" STRING'S FIRST 6 CHARACTERS AND THEN CONVERTING IT TO HEX VIA BUILT IN FUNCTIONS TO CONTINUE ON AND PASS ON TO MORE FUNCTIONS
    opcode = machine_instruction[:6]
    #THESE ARE BUILT IN Python Functions
    #this is for funct specifically
    funct = machine_instruction[-6:]
    #to_dec_funct = int(funct)
    #to_dec = int(opcode)
    #print(opcode)
    #print(to_dec)
    #print(funct)
    #print(to_dec_funct)
    opcode_hex = hex(int(opcode,2))
    #this is to turn funct into hex to compare with data frame
    funct_hex = hex(int(funct,2))
    #print(to_dec_funct)
    #print(opcode_hex)
    #print(funct_hex)
    # I am thinking about making some sort of key or dict to hold all operations and their types


    '''
    Essentially made a data frame with two columns, operation name and op(hex), or for r type: operation name and funct(hex)"
    '''
    Dict = {    
            '0x8':'addi',
            '0x9':'addiu',
            '0xc':'andi',
            '0x4':'beq',
            '0x5':'bne',
            '0x24':'lbu',
            '0x25':'lhu',
            '0x30':'ll',
            '0xf':'lui',
            '0x23':'lw',
            '0xd':'ori',
            '0xa':'slti',
            '0xb':'sltiu',
            '0x28':'sb',
            '0x38':'sc',
            '0x29':'sh',
            '0x2b':'sw',
            '0x20':'add',
            '0x21':'addu',
            '0x24':'and',
            '0x8':'jr',
            '0x27':'nor',
            '0x25':'or',
            '0x2a':'slt',
            '0x2b':'sltu',
            '0x0':'sll',
            '0x2':'srl',
            '0x22':'sub',
            '0x23':'subu'
            }
    
   

    op_name = " "
    instruction_type = " "
    #0 is operation name and column 1 is hex value of opcode for I type and j type and column 1 is funct in hex if r type

    #Changed the statements so we don't go through the whole excel each time

    if opcode_hex == hex(0):
        for key in Dict:
            if funct_hex == key:
                op_name = Dict[key];
                instruction_type = "R"
   
    if opcode_hex == hex(2) and instruction_type == " ":
        instruction_type="J"
        op_name = "j"
        #print(op_name)
    if opcode_hex == hex(3) and instruction_type == " ":
        instruction_type="J"
        op_name = "jal"
        #print(op_name)    
    if instruction_type == " ":
        for key in Dict:
            if opcode_hex == key:
                op_name = Dict[key];
                instruction_type = "I"
        if instruction_type == " ":
            instruction_type="N/A"
            op_name = "N/A"
           
    print("\nInstruction Type: " + instruction_type)   
    print("Operation: " + op_name) 
    
    #REGISTER MAPPING

    if instruction_type == 'I':
        iTypeDecoder(machine_instruction)
    if instruction_type == 'J':
        jTypeDecoder(machine_instruction)
    if instruction_type == 'R':
        rTypeDecoder(machine_instruction)
    

                    
def main():
    machine_instruction = input("Enter an instruction:\n\n")
    #I AM PASSING WHOLE 32 BIT MACHINE INSTRUCTION HERE SO THAT I COULD LATER PASS THAT ON TO OTHER FUNCTIONS BASED ON WHAT THE FUNCTION IS
    opCodeDecoder(machine_instruction)
    


if __name__ == "__main__":
    main()
