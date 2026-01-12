weight = float(input('Enter your weight'))
unit   = input("Kilograms or Pounds? (K or L): ")
if unit == 'K':
    weight = weight * 2.205
elif unit == 'L':
    weight = weight/2.205
else :
    print('Unit not valid')

print(weight)