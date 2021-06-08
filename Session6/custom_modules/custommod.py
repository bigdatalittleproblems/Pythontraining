def noParam():
    print("This Function does not require any parameter")

def chitchat(name:str):
    print(f'Hello {name}, and welcome to Snakes on a DataFrame!')

def tipcalc(checkTotal:float,tipPercent:float=.15):
    tipAmount=checkTotal*tipPercent
    output=checkTotal+tipAmount
    print(f"at {tipPercent*100}% your {checkTotal} check, you are going to tip {tipAmount}, and your total check will be {output}")
    return output

# purposeful Error Please FIX.
tipcalc(205)
noParam()
chitchat("Kem Smalloffice")

