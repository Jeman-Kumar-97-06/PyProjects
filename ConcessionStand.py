menu = {
    "pizza":3.00,
    "nachos":4.50,
    "popcorn":6.00,
    "fries":2.50,
    "chips":1.00,
    "pretzel":3.50,
    "soda":3.00,
    "lemonade":4.25
}

cart = []
total = 0

print("------------MENU------------")

for key,val in menu.items():
    print(f"{key:10}:{val:.2f}")

print("----------------------------")

while True:
    food = input("Select an item (q to quit): ")
    if food.lower() == 'q':
        break
    elif food in menu:
        cart.append(food)

print('---------------------------')
for food in cart:
    total = total + menu.get(food)
    print(food,end=' ')

print(f"Total is : ${total:.2f}")

         