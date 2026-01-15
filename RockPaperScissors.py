import random
options = ('rock','paper','scissors')
player  = None


while True:
    computer = random.choice(options)
    player_choice = input("What's you choice? rock? paper? scissors? \n")
    if (player_choice not in options):
        print("Invalid Choice!")
    elif (player_choice.lower() == 'q'):
        break
    elif((player_choice.lower() == 'paper' and computer == 'rock') or (player_choice.lower() == 'rock' and computer == 'scissors') or (player_choice.lower() == 'scissors' and computer=='paper')):
        print('computer choice: '+computer)
        print("You win!")
    elif (player_choice.lower() == computer):
        print('computer choice: '+computer)
        print("Draw")
    else:
        print('computer choide: '+computer)
        print('You lose!') 
    again = input('Wanna Go Again? (y/n): ')
    if (again.lower() == 'y'):
        continue
    else:
        break
