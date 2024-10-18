class FileReader:
    def __init__(self) -> None:
        try:
            with open("highscore.txt", "r") as file:
                self.high_score = int(file.readline().strip())
        except FileNotFoundError:
            self.high_score = 0  # Default high score if the file doesn't exist

    def update_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
            with open("highscore.txt", "w") as file:
                file.write(str(self.high_score))
                
    def reset_high_score(self) :
        with open("highscore.txt", "w") as file:
                file.write(str(0))