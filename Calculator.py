#Python Calculator:
operator = input("Enter an operator (+,-,*,/): ")
num1     = (input("Enter the first number : "))
num2     = (input("Enter the second number : "))
#-----------------------------------------
# Easy Version:
# print(eval(num1+operator+num2))
#-----------------------------------------

if operator == '+':
    result = float(num1)+float(num2)
    print(round(result,3))
elif operator == '-':
    result = float(num1)-float(num2)
    print(round(result,3))
elif operator == '*':
    result = float(num1)*float(num2)
    print(round(result,3))
elif operator == '/':
    result = float(num1)/float(num2) 
    print(round(result,3))
else:
    print("No Feature. Sorry!")
#-------------------------------------------
