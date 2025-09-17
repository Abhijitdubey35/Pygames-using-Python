import random

def play_best_of_n(n, leaderboard):
    possible_actions = ["rock", "paper", "scissors"]
    user_score = 0
    computer_score = 0
    rounds_played = 0
    rounds_needed = (n // 2) + 1  # Number of wins needed to win the match

    print(f"\nStarting a Best-of-{n} game!")
    print("Type 'quit' at any time to stop the current game.\n")

    while user_score < rounds_needed and computer_score < rounds_needed:
        user_action = input("Choose rock, paper, or scissors: ").lower().strip()

        if user_action == "quit":
            print("You ended the game early.\n")
            return  # End current match without updating leaderboard

        if user_action not in possible_actions:
            print("Invalid input. Please try again.\n")
            continue

        computer_action = random.choice(possible_actions)
        print(f"\nYou chose {user_action}, computer chose {computer_action}.")

        if user_action == computer_action:
            print("It's a tie!\n")
        elif (
            (user_action == "rock" and computer_action == "scissors") or
            (user_action == "paper" and computer_action == "rock") or
            (user_action == "scissors" and computer_action == "paper")
        ):
            print("You win this round!\n")
            user_score += 1
        else:
            print("Computer wins this round!\n")
            computer_score += 1

        rounds_played += 1
        print(f"Score: You {user_score} - Computer {computer_score}\n")

    # Match result
    if user_score > computer_score:
        print("🎉 You won this match!")
        leaderboard["User"] += 1
    else:
        print("💻 Computer won this match!")
        leaderboard["Computer"] += 1


def main():
    leaderboard = {"User": 0, "Computer": 0}

    print("🎮 Welcome to Rock, Paper, Scissors: Best of N Edition!")
    
    while True:
        try:
            n = input("Enter an odd number of rounds for Best-of-N (or type 'quit' to exit): ").strip()
            if n.lower() == "quit":
                break
            n = int(n)
            if n < 1 or n % 2 == 0:
                print("Please enter a positive **odd** number (e.g., 3, 5, 7).")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        play_best_of_n(n, leaderboard)

    # Final Leaderboard
    print("\n📊 Final Leaderboard:")
    print(f"You won {leaderboard['User']} match(es).")
    print(f"Computer won {leaderboard['Computer']} match(es).")
    print("Thanks for playing!")

# Run the game
main()
