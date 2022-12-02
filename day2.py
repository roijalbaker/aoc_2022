shapes = {
    "rock": {"win": "scissors", "lose": "paper", "score": 1},
    "paper": {"win": "rock", "lose": "scissors", "score": 2},
    "scissors": {"win": "paper", "lose": "rock", "score": 3},
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

me2 = {
    "X": "lose",
    "Y": "draw",
    "Z": "win"
}

if __name__ == "__main__":
    score = 0
    score2 = 0
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

            other_shape = shapes[other[you]]
            if me2[i] == "draw":
                score2 += 3 + other_shape["score"]
            elif me2[i] == "win":
                score2 += 6 + shapes[other_shape["lose"]]["score"]
            elif me2[i] == "lose":
                score2 += 0 + shapes[other_shape["win"]]["score"]

    print(score)
    print(score2)
