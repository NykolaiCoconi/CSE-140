import pandas as pd

def opcodeDecoder(opCode):
    #PARSING "OPCODE" STRING'S FIRST 6 CHARACTERS AND THEN CONVERTING IT TO HEX VIA BUILT IN FUNCTIONS TO CONTINUE ON AND PASS ON TO MORE FUNCTIONS
    #print(opCode[-6:])
    #THESE ARE BUILT IN Python Functions
    #this is for funct specifically
    to_dec_funct = int(opCode[-6:],2)
    to_dec = int(opCode[:6],2)
    to_hex = hex(to_dec)
    #this is to turn funct into hex to compare with data frame
    to_hex_funct = hex(to_dec_funct)
    #print(to_dec_funct)
    #print(to_hex[2:])
    #print(to_hex_funct[2:])
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

    #for some reason this works for I type but not all the way I still need to fix it up a bit
    for j in range(len(J_type_dict)):
        if to_hex[2:] == J_type_dict.iloc[j, 1]:
            op_name = J_type_dict.iloc[j, 0]
            instruction_type="J"
    
    for i in range(len(I_type_dict)):
        if to_hex[2:] == I_type_dict.iloc[i, 1]:
            op_name = I_type_dict.iloc[i, 0]
            instruction_type="I"
    #Im using the to_hex_funct variable since this takes the last 6 bits of a 32 bit and converts it to the hex of a funct which is stored in our R type dictionary
    for r in range(len(R_type_dict)):
        if to_hex_funct[-2:] == R_type_dict.iloc[r, 1]:
            op_name = R_type_dict.iloc[r, 0]
            instruction_type="R"
            
    print(instruction_type)   
    
    print(op_name) 

                    
def main():
    
    
    machine_instruction = input("Enter an instruction:\n")
    #I AM PASSING WHOLE 32 BIT MACHINE INSTRUCTION HERE SO THAT I COULD LATER PASS THAT ON TO OTHER FUNCTIONS BASED ON WHAT THE FUNCTION IS
    opcodeDecoder(machine_instruction)
    

if __name__ == "__main__":
    main()