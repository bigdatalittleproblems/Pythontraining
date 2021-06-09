def noParam():
    print("This Function does not require any parameter")
noParam()

def chitchat(name:str):
    print(f'Hello {name}, and welcome to Snakes on a DataFrame!')
chitchat("Ken Smalloffice")

def chitchatV2(name:str):
    txtOutput=f'Hello {name}, and welcome to Snakes on a DataFrame!'
    print(txtOutput)
    return txtOutput
chitchatV2("Coolio Foolio")

# Challenge Make function that multiplies 2 numbers and returns the product

def tipcalc(checkTotal:float,tipPercent:float=.15):
    tipAmount=round(checkTotal*tipPercent,2)
    output=round(checkTotal+tipAmount,2)
    print(f"at {tipPercent*100}% your {checkTotal} check, you are going to tip {tipAmount}, and your total check will be {output}")
    return output
tipcalc(205)

def test():
    print(__name__)
test()


# purposeful Error Please FIX.

