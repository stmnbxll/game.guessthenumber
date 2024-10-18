import random
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("themes\purple.json")

class GuessTheNumberApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Угадай число")
        self.geometry("350x300")
        self.iconbitmap("game.ico")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.difficulty_label = ctk.CTkLabel(self, text="Выбери уровень сложности")
        self.difficulty_label.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.easy_button = ctk.CTkButton(self, text="Легкий (1-50)", command=lambda: self.start_game(50))
        self.easy_button.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        self.medium_button = ctk.CTkButton(self, text="Средний (1-100)", command=lambda: self.start_game(100))
        self.medium_button.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")

        self.hard_button = ctk.CTkButton(self, text="Тяжелый (1-200)", command=lambda: self.start_game(200))
        self.hard_button.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")

        self.label = ctk.CTkLabel(self, text="Угадай число")
        self.entry = ctk.CTkEntry(self)
        self.submit_button = ctk.CTkButton(self, text="Угадать", command=self.check_guess)
        self.result_label = ctk.CTkLabel(self, text="")
        self.restart_button = ctk.CTkButton(self, text="Начать заново", command=self.restart_game)

    def start_game(self, max_value):
        self.max_value = max_value
        self.number_to_guess = random.randint(1, self.max_value)
        self.attempts = 0

        self.difficulty_label.grid_forget()
        self.easy_button.grid_forget()
        self.medium_button.grid_forget()
        self.hard_button.grid_forget()

        self.label.configure(text=f"Угадай число от 1 до {self.max_value}")
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.submit_button.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.result_label.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.restart_button.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        self.entry.delete(0, ctk.END)
        self.submit_button.configure(state="normal")
        self.result_label.configure(text="")

    def check_guess(self):
        player_guess = self.entry.get()

        if not player_guess:
            self.result_label.configure(text="Введи число")
            return

        try:
            player_guess = int(player_guess)
        except ValueError:
            self.result_label.configure(text="Пожалуйста, введи действительное число")
            return

        self.attempts += 1

        if player_guess < self.number_to_guess:
            self.result_label.configure(text="Больше! Попробуй еще раз")
        elif player_guess > self.number_to_guess:
            self.result_label.configure(text="Меньше! Попробуй еще раз")
        else:
            self.result_label.configure(text=f"Поздравляю! Ты угадал число {self.number_to_guess} за {self.attempts} попыток")
            self.submit_button.configure(state="disabled")

    def restart_game(self):
        self.label.grid_forget()
        self.entry.grid_forget()
        self.submit_button.grid_forget()
        self.result_label.grid_forget()
        self.restart_button.grid_forget()

        self.difficulty_label.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.easy_button.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
        self.medium_button.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")
        self.hard_button.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")

if __name__ == "__main__":
    app = GuessTheNumberApp()
    app.mainloop()