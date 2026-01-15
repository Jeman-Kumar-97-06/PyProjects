menu = {
    "pizze":3.00,
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

for key,val in menu.items():
    print(f"{key:10}:{val:.2f}")

