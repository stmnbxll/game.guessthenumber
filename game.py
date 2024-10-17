import random
import customtkinter as ctk

# Инициализация приложения
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("themes\purple.json")

class GuessTheNumberApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Угадай число")
        self.geometry("350x256")
        self.iconbitmap("game.ico")
        self.resizable(False, False)

        # Метка для инструкции
        self.label = ctk.CTkLabel(self, text="Угадай число от 1 до 100")
        self.label.pack(pady=10)

        # Поле ввода для числа
        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=10)

        # Кнопка для отправки числа
        self.submit_button = ctk.CTkButton(self, text="Угадать", command=self.check_guess)
        self.submit_button.pack(pady=10)

        # Метка для вывода результатов
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(pady=10)

        # Кнопка для перезапуска игры
        self.restart_button = ctk.CTkButton(self, text="Начать заново", command=self.restart_game)
        self.restart_button.pack(pady=10)

        # Инициализация игры
        self.restart_game()

    def check_guess(self):
        player_guess = self.entry.get()

        # Проверка на пустое значение
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
        self.number_to_guess = random.randint(1, 100)
        self.attempts = 0
        self.result_label.configure(text="")
        self.submit_button.configure(state="normal")
        self.entry.delete(0, ctk.END)

if __name__ == "__main__":
    app = GuessTheNumberApp()
    app.mainloop()
