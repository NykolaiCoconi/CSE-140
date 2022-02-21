import pandas as pd

def loopCode(answer):
    if answer == "1":
        machine_instruction = input("\nEnter an instruction:\n\n")
        opCodeDecoder(machine_instruction)
    else:
        print("\nCode finished")
        exit

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
    answer = input("\nEnter 1 to continue:\n")
    loopCode(answer)
    

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
    print("Shamt: $",end = "")
    print(int(shamt,2))
    print("Funct: ",end = "")
    print(int(funct,2),end = "")
    print(" or (", end = "")
    print(hex(int(funct,2)), end = "")
    print(")")
    answer = input("\nEnter 1 to continue:\n")
    loopCode(answer)
    
def jTypeDecoder(machine_instruction):
    imm = machine_instruction[-26:]
    #print(imm)
    print("Immediate: ",end="")
    print(int(imm,2), end=" ") 
    print("or (", end = "")
    print(hex(int(imm,2)), end = "") 
    print(")")
    answer = input("\nEnter 1 to continue:\n")
    loopCode(answer)
    
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
    I_type_dict = pd.read_excel('InstructionDict.xlsx',sheet_name='iType')
    R_type_dict = pd.read_excel('InstructionDict.xlsx',sheet_name='rType')
    J_type_dict = pd.read_excel('InstructionDict.xlsx',sheet_name='jType')
    
    '''Since we now have the operations and their respective hex value as an opcode in a data frame we can now compare the user 
       input(as a decimal) with the hex value with each respective operation (in decimal) and then return what operation type it is to main
    '''

    op_name = " "
    instruction_type = " "
    #0 is operation name and column 1 is hex value of opcode for I type and j type and column 1 is funct in hex if r type

    #Changed the statements so we don't go through the whole excel each time

    
    if opcode_hex == hex(0):
        for r in range(len(R_type_dict)):
            if funct_hex == R_type_dict.iloc[r, 1]:
                op_name = R_type_dict.iloc[r, 0]
                instruction_type = "R"
                #print(op_name)
    if opcode_hex == hex(2) and instruction_type == " ":
        instruction_type="J"
        op_name = "j"
        #print(op_name)
    if opcode_hex == hex(3) and instruction_type == " ":
        instruction_type="J"
        op_name = "jal"
        #print(op_name)    
    if instruction_type == " ":
        for i in range(len(I_type_dict)):
            if opcode_hex == I_type_dict.iloc[i, 1]:
                op_name = I_type_dict.iloc[i, 0]
                instruction_type="I"
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
