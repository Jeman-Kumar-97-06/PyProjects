import random

lowest_num = 1
highest_num = 100
answer = random.randint(lowest_num,highest_num)

guesses = 0

is_running = True

print("Welcome to Guessing Game!")
print(f"Select a number between {lowest_num} and {highest_num}")

while is_running:
    guess = input("Enter your guess: ")
    if guess.isdigit():
        guess = int(guess)
        guesses += 1
        if guess < lowest_num or guess > highest_num:
            print("That guess is out of range")
            print(f"Select a number between {lowest_num} and {highest_num}")
        elif guess<answer:
            print("Too low! Try again!")
        elif guess > answer:
            print("Too high! Try again!")
        else:
            print(f"Correct!")
            print(f"Number of guesse: ${guesses}")
            is_running=False
    else:
        print("Invalid guess :(")
        print(f"Please type a number between {lowest_num} and {highest_num}")