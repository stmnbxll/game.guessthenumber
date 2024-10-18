import random
import customtkinter as ctk
import pygame
import tkinter.messagebox as messagebox
import json
import os

pygame.mixer.init()

def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("themes/purple.json")

class GuessTheNumberApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Угадай число")
        self.geometry("400x450")
        self.iconbitmap("game.ico")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)

        self.difficulty_label = ctk.CTkLabel(self, text="Выбери уровень сложности")
        self.difficulty_label.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.easy_button = ctk.CTkButton(self, text="Легкий (1-50)", command=lambda: self.start_game(50), height=70)
        self.easy_button.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.medium_button = ctk.CTkButton(self, text="Средний (1-100)", command=lambda: self.start_game(100), height=70)
        self.medium_button.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.hard_button = ctk.CTkButton(self, text="Тяжелый (1-200)", command=lambda: self.start_game(200), height=70)
        self.hard_button.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        self.label = ctk.CTkLabel(self, text="Угадай число")
        self.entry = ctk.CTkEntry(self)
        self.submit_button = ctk.CTkButton(self, text="Угадать", command=self.check_guess)
        self.result_label = ctk.CTkLabel(self, text="")
        self.restart_button = ctk.CTkButton(self, text="Начать заново", command=self.restart_game)

        self.achievements_button = ctk.CTkButton(self, text="Посмотреть достижения", command=self.show_achievements)
        self.stats_button = ctk.CTkButton(self, text="Посмотреть статистику", command=self.show_stats)

        self.achievements = {
            "Новичок": False,
            "Счастливчик": False,
            "Профессионал": False,
            "Заядлый игрок": False,
            "Суперзвезда": False,
            "Экстрасенс": False,
            "Мастер угадываний": False,
        }
        self.games_played = 0
        self.total_attempts = 0
        self.record_attempts = float('inf')
        self.guesses_made = 0

        self.load_achievements()
        self.load_stats()

    def load_achievements(self):
        if os.path.exists("achievements.json"):
            with open("achievements.json", "r") as file:
                self.achievements = json.load(file)

    def save_achievements(self):
        with open("achievements.json", "w") as file:
            json.dump(self.achievements, file)

    def load_stats(self):
        if os.path.exists("stats.json"):
            with open("stats.json", "r") as file:
                data = json.load(file)
                self.games_played = data.get("games_played", 0)
                self.total_attempts = data.get("total_attempts", 0)
                self.record_attempts = data.get("record_attempts", float('inf'))
                self.guesses_made = data.get("guesses_made", 0)

    def save_stats(self):
        with open("stats.json", "w") as file:
            json.dump({
                "games_played": self.games_played,
                "total_attempts": self.total_attempts,
                "record_attempts": self.record_attempts,
                "guesses_made": self.guesses_made
            }, file)

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

        self.stats_button.grid(row=5, column=0, padx=20, pady=5, sticky="nsew")
        self.achievements_button.grid(row=6, column=0, padx=20, pady=5, sticky="nsew")

        self.entry.delete(0, ctk.END)
        self.submit_button.configure(state="normal")
        self.result_label.configure(text="")
        play_sound("sounds/restart_game.mp3")

        self.games_played += 1
        self.save_stats()

        if self.games_played == 1 and not self.achievements["Новичок"]:
            self.achievements["Новичок"] = True
            self.show_achievement_notification("Новичок!")
            self.save_achievements()

        if self.games_played == 10 and not self.achievements["Заядлый игрок"]:
            self.achievements["Заядлый игрок"] = True
            self.show_achievement_notification("Заядлый игрок!")
            self.save_achievements()

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
        self.total_attempts += 1
        self.save_stats()

        if player_guess < self.number_to_guess:
            self.result_label.configure(text="Больше! Попробуй еще раз")
            play_sound("sounds/wrong_guess.mp3")
        elif player_guess > self.number_to_guess:
            self.result_label.configure(text="Меньше! Попробуй еще раз")
            play_sound("sounds/wrong_guess.mp3")
        else:
            self.guesses_made += 1
            self.save_stats()
            self.result_label.configure(
                text=f"Поздравляю! Ты угадал число {self.number_to_guess} за {self.attempts} попыток")
            self.submit_button.configure(state="disabled")
            play_sound("sounds/correct_guess.mp3")

            if self.attempts < self.record_attempts:
                self.record_attempts = self.attempts
                self.save_stats()

            self.check_achievements()

    def check_achievements(self):
        if self.attempts == 1 and not self.achievements["Суперзвезда"]:
            self.achievements["Суперзвезда"] = True
            self.show_achievement_notification("Суперзвезда!")
            self.save_achievements()

        if self.attempts <= 3 and not self.achievements["Счастливчик"]:
            self.achievements["Счастливчик"] = True
            self.show_achievement_notification("Счастливчик!")
            self.save_achievements()

        if self.attempts <= 5 and not self.achievements["Профессионал"]:
            self.achievements["Профессионал"] = True
            self.show_achievement_notification("Профессионал!")
            self.save_achievements()

        if self.games_played >= 10 and not self.achievements["Заядлый игрок"]:
            self.achievements["Заядлый игрок"] = True
            self.show_achievement_notification("Заядлый игрок!")
            self.save_achievements()

        if self.attempts <= 3:
            if not hasattr(self, 'successful_attempts'):
                self.successful_attempts = 0
            self.successful_attempts += 1
        else:
            self.successful_attempts = 0

        if self.successful_attempts >= 5 and not self.achievements["Экстрасенс"]:
            self.achievements["Экстрасенс"] = True
            self.show_achievement_notification("Экстрасенс!")
            self.save_achievements()

        if self.guesses_made >= 10 and not self.achievements["Мастер угадываний"]:
            self.achievements["Мастер угадываний"] = True
            self.show_achievement_notification("Мастер угадываний!")
            self.save_achievements()

    def show_achievement_notification(self, achievement):
        messagebox.showinfo("Достижение", f"Поздравляю! Ты достиг: {achievement}")

    def show_achievements(self):
        achievements_text = ""
        for achievement, status in self.achievements.items():
            status_text = "Достигнуто" if status else "Не достигнуто"
            achievements_text += f"{achievement}: {status_text}\n"
        messagebox.showinfo("Достижения", achievements_text)

    def show_stats(self):
        record_attempts_display = self.record_attempts if self.record_attempts != float('inf') else 0
        stats_text = (
            f"Общее количество сыгранных игр: {self.games_played}\n"
            f"Общее количество попыток: {self.total_attempts}\n"
            f"Рекордная попытка: {record_attempts_display}\n"
            f"Количество угаданных чисел: {self.guesses_made}"
        )
        messagebox.showinfo("Статистика", stats_text)

    def restart_game(self):
        self.label.grid_forget()
        self.entry.grid_forget()
        self.submit_button.grid_forget()
        self.result_label.grid_forget()
        self.restart_button.grid_forget()
        self.achievements_button.grid_forget()
        self.stats_button.grid_forget()

        self.difficulty_label.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.easy_button.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        self.medium_button.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.hard_button.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        self.entry.delete(0, ctk.END)
        self.result_label.configure(text="")
        self.submit_button.configure(state="normal")

if __name__ == "__main__":
    app = GuessTheNumberApp()
    app.mainloop()
