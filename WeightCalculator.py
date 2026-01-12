weight = float(input('Enter your weight'))
unit   = input("Kilograms or Pounds? (K or L): ")
if unit == 'K':
    weightr = weight * 2.205
    unitr = 'Lbs.'
    print(f'You weigh is : {round(weight,1)} {unitr}')
elif unit == 'L':
    weightr = weight/2.205
    unitr = 'Kgs.'
    print(f'You weigh is : {round(weight,1)} {unitr}')
else :
    print('Unit not valid')

