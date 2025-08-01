import random


def game_gio():
    player = input("which one are you going to choose: rock, paper or scissors? ")
    option = ["rock", "paper", "scissors"]
    computer = random.choice(option)
    return {"player": player, "computer": computer}


def which_one_is_winner(player, computer):
    if player == computer:
        return "It's a tie!"
    elif player == "rock":
        if computer == "paper":
            return "Paper covers rock. You lose."
        else:
            return "Rock smashes scissors. You win!"
    elif player == "scissors":
        if computer == "rock":
            return "Rock smashes scissors. You lose."
        else:
            return "Scissors cuts paper. You win!"
    elif player == "paper":
        if computer == "scissors":
            return "Scissors cuts paper. You lose."
        else:
            return "Paper covers rock. You win!"


match = game_gio()
print(match)
result = which_one_is_winner(match["player"], match["computer"])
print(result)
