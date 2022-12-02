shapes = {
    "rock": {"win": "scissors", "score": 1},
    "paper": {"win": "rock", "score": 2},
    "scissors": {"win": "paper", "score": 3},
}

other = {
    "A": "rock",
    "B": "paper",
    "C": "scissors"
}

me = {
    "X": "rock",
    "Y": "paper",
    "Z": "scissors"
}

if __name__ == "__main__":
    score = 0
    with open("day2_input1.txt") as f:
        for line in f.readlines():
            you, i = line[:3].split(" ")
            score += shapes[me[i]]["score"]
            if me[i] == other[you]:
                # draw
                score += 3
            elif shapes[me[i]]["win"] == other[you]:
                # win
                score += 6
            # loose += 0
    print(score)
