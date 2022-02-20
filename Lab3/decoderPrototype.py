import pandas as pd

def opcodeDecoder(opCode):
    #PARSING "OPCODE" STRING'S FIRST 6 CHARACTERS AND THEN CONVERTING IT TO HEX VIA BUILT IN FUNCTIONS TO CONTINUE ON AND PASS ON TO MORE FUNCTIONS

    #THESE ARE BUILT IN Python Functions
    to_dec = int(opCode[:6],2)
    to_hex = hex(to_dec)
    #print(to_dec)
    #print(to_hex)
    # I am thinking about making some sort of key or dict to hold all operations and their types
    I_type_dict = pd.read_excel('InstructionDict.xlsx',sheet_name='iType')
    R_type_dict = pd.read_excel('InstructionDict.xlsx',sheet_name='rType')
    J_type_dict = pd.read_excel('InstructionDict.xlsx',sheet_name='jType')
    #print(I_type_dict)
    #print(J_type_dict)
    #print(R_type_dict)
    '''Since we now have the operations and their respective hex value as an opcode in a data frame we can now compare the user 
       input(as a decimal) with the hex value with each respective operation (in decimal) and then return what operation type it is to main
    '''

    '''
    SOME SIMPLE EXAMPLES ON HOW TO ACCESS EACH COLUMN IN THE DATA FRAMES
    print(I_type_dict.loc[:,"op(hex)"])
    print(I_type_dict.loc[:,"Operation"])
    print(R_type_dict.loc[:,"funct(hex)"])
    print(R_type_dict.loc[:,"Operation"])
    print(J_type_dict.loc[:,"op(hex)"])
    print(J_type_dict.loc[:,"Operation"])
    '''
def main():
    
    
    machine_instruction = input("Enter an instruction:\n")
    #I AM PASSING WHOLE 32 BIT MACHINE INSTRUCTION HERE SO THAT I COULD LATER PASS THAT ON TO OTHER FUNCTIONS BASED ON WHAT THE FUNCTION IS
    opcodeDecoder(machine_instruction)
    

if __name__ == "__main__":
    main()