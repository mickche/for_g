import json
from pathlib import Path
from textual import events, on
from textual.app import App
from textual.containers import Center, Container, Grid, Horizontal, Middle
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, RadioButton, RadioSet, Static

STATS_FILE = Path("highscore.json")

EASY_TASKS = {
    1: {
        "question": "print(5 + 3)\nЗапитання: Що виведе в термінал?",
        "options": ["53", "8", "5 + 3"],
        "correct": 1,
    },
    2: {
        "question": "x = 'Python'\nprint(len(x))\nЗапитання: Яке значення повернула функція len()?",
        "options": ["5", "6", "7"],
        "correct": 1,
    },
    3: {
        "question": "Завдання 3: Оберіть стрічку коду, у якій допущено синтаксичну помилку:",
        "code_lines": [
            "a = 10",
            "b = 20",
            "if a < b",
            "    print('a менше b')",
            "print('Готово')",
        ],
        "correct": 2,
    },
    4: {
        "question": "name = 'Анна'\nprint('{name}!')\nЩо треба поставити?",
        "options": ["f", "str", "format"],
        "correct": 0,
    },
    5: {
        "question": "print(type(10.5))\nЗапитання: Який тип даних поверне ця функція?",
        "options": ["<class 'int'>", "<class 'float'>", "<class 'str'>"],
        "correct": 1,
    },
    6: {
        "question": "print(10 // 3)\nЗапитання: Що поверне оператор цілочисельного ділення?",
        "options": ["3.333", "3", "1"],
        "correct": 1,
    },
    7: {
        "question": "a = [1, 2, 3]\nprint(a[0])\nЗапитання: Що виведе в термінал?",
        "options": ["1", "2", "IndexError"],
        "correct": 0,
    },
    8: {
        "question": "Завдання 8: Яка з цих змінних оголошена З ПОМИЛКОЮ синтаксису?",
        "options": ["my_var = 5", "1_variable = 10", "_value = 'hello'"],
        "correct": 1,
    },
    9: {
        "question": "is_active = True\nprint(not is_active)\nЗапитання: Що виведе в термінал?",
        "options": ["True", "False", "None"],
        "correct": 1,
    },
}

NORMAL_TASKS = {
    1: {
        "question": "print(1 + 5)\nЗапитання: Що виведе в термінал?",
        "options": ["1+5", "6", "print(1+5)"],
        "correct": 1,
    },
    2: {
        "question": "Завдання 2: Оберіть стрічку коду, у якій допущено синтаксичну помилку:",
        "code_lines": [
            "def calculate_total(a, b):",
            "    total = a + b",
            "    if total > 10",
            "        print('Більше 10')",
            "    return total",
        ],
        "correct": 2,
    },
    3: {
        "question": "answer = input('...:')\nprint('Ваша відповідь: {answer}')\nЩо треба поставити?",
        "options": ["f", "str", "format"],
        "correct": 0,
    },
    4: {
        "question": "nums = [10, 20, 30, 40]\nprint(nums[1:3])\nЗапитання: Що виведе в термінал?",
        "options": ["[10, 20]", "[20, 30]", "[20, 30, 40]"],
        "correct": 1,
    },
    5: {
        "question": "text = 'python'\nprint(text.upper())\nЗапитання: Що виведе результат виконання методу?",
        "options": ["PYTHON", "Python", "python"],
        "correct": 0,
    },
    6: {
        "question": "Завдання 6: Оберіть варіант із неправильним оголошенням структури даних:",
        "options": [
            "items = [1, 2, 'three']",
            "items = (1, 2, 3)",
            "items = [1, 2 3]",
        ],
        "correct": 2,
    },
    7: {
        "question": "x = 5\nx += 3\nprint(x)\nЗапитання: Яким буде підсумкове значення x?",
        "options": ["53", "8", "15"],
        "correct": 1,
    },
    8: {
        "question": "Завдання 8: Оберіть стрічку з помилкою у роботі зі словником (dict):",
        "code_lines": [
            "user = {'name': 'Alex', 'age': 25}",
            "print(user['name'])",
            "print(user.age)",
            "user['age'] = 26",
        ],
        "correct": 2,
    },
    9: {
        "question": "for i in range(3):\n    print(i, end=' ')\nЗапитання: Що з'явиться в терміналі?",
        "options": ["1 2 3 ", "0 1 2 ", "0 1 2 3 "],
        "correct": 1,
    },
}

HARD_TASKS = {
    1: {
        "question": "print(2 ** 4)\nЗапитання: Що виведе в термінал?",
        "options": ["8", "16", "64"],
        "correct": 1,
    },
    2: {
        "question": "nums = [3, 1, 4, 2]\nnums.sort()\nprint(nums)\nЗапитання: Що виведе метод sort()?",
        "options": ["[4, 3, 2, 1]", "[1, 2, 3, 4]", "[3, 1, 4, 2]"],
        "correct": 1,
    },
    3: {
        "question": "Завдання 3: Оберіть рядок, у якому правильно обробляється виняток:",
        "code_lines": [
            "try:",
            "    x = 10 / 0",
            "except ZeroDivisionError:",
            "    print('Ділення на нуль!')",
            "print('Кінець')",
        ],
        "correct": 2,
    },
    4: {
        "question": "def greet(name='Гість'):\n    return f'Привіт, {name}'\nprint(greet())\nЗапитання: Що поверне функція?",
        "options": ["Привіт, Гість", "Привіт, name", "TypeError"],
        "correct": 0,
    },
    5: {
        "question": "text = 'python'\nprint(text[::-1])\nЗапитання: Що виведе цей зріз?",
        "options": ["python", "nohtyp", "p"],
        "correct": 1,
    },
    6: {
        "question": "Завдання 6: Оберіть рядок із синтаксичною помилкою у функції:",
        "code_lines": [
            "def add_numbers(a, b):",
            "    result = a + b",
            "    return result",
            "print(add_numbers(5 10))",
        ],
        "correct": 3,
    },
    7: {
        "question": "a = (1, 2, 3)\na[0] = 5\nЗапитання: Чому виникне помилка TypeError?",
        "options": ["Кортеж (tuple) не можна змінювати", "Неправильний індекс", "Число має бути в лапках"],
        "correct": 0,
    },
    8: {
        "question": "person = {'name': 'Анна'}\nprint(person.get('age', 18))\nЗапитання: Що виведе метод get()?",
        "options": ["None", "KeyError", "18"],
        "correct": 2,
    },
    9: {
        "question": "x = [1, 2, 3]\nprint(len(x * 2))\nЗапитання: Яка довжина буде у нового списку?",
        "options": ["3", "6", "9"],
        "correct": 1,
    },
}

TASKS_MAP = {
    "btn_easy": EASY_TASKS,
    "btn_normal": NORMAL_TASKS,
    "btn_hard": HARD_TASKS,
}

NEXT_DIFFICULTY = {
    "btn_easy": "btn_normal",
    "btn_normal": "btn_hard",
    "btn_hard": None,
}


class HighScoreScreen(Screen):
    def compose(self):
        high_score = self.app.high_score
        high_correct = self.app.high_score_correct
        high_total = self.app.high_score_total

        score_text = (
            f"[b]🏆 Ваші досягнення[/b]\n\n"
            f"Рекорд успішності: [yellow]{high_score}%[/yellow]\n"
            f"Правильних відповідей: [green]{high_correct}[/green] з {high_total}"
        )

        return [
            Middle(
                Center(
                    Container(
                        Static("Найкращий результат", id="title"),
                        Static(score_text, id="stats-text"),
                        Button("Назад", id="btn_back", variant="primary"),
                        id="menu-box",
                    )
                )
            ),
            Footer(),
        ]

    @on(Button.Pressed, "#btn_back")
    def action_go_back(self):
        self.app.pop_screen()


class ResultScreen(Screen):
    def compose(self):
        correct = self.app.correct_count
        incorrect = self.app.incorrect_count
        total = correct + incorrect
        percentage = round((correct / total * 100)) if total > 0 else 0

        self.app.update_high_score(percentage, correct, total)

        stats_text = (
            f"[b]Вітаємо! Ви пройшли всі рівні![/b]\n\n"
            f"Правильних відповідей: [green]{correct}[/green]\n"
            f"Неправильних відповідей: [red]{incorrect}[/red]\n"
            f"Усього відповідей: {total}\n"
            f"Успішність: [yellow]{percentage}%[/yellow]"
        )

        return [
            Middle(
                Center(
                    Container(
                        Static("Підсумки вікторини", id="title"),
                        Static(stats_text, id="stats-text"),
                        Button("Головне меню", id="btn_menu", variant="success"),
                        id="menu-box",
                    )
                )
            ),
            Footer(),
        ]

    @on(Button.Pressed, "#btn_menu")
    def action_go_main_menu(self):
        self.app.reset_stats()
        self.app.pop_screen_until(lambda screen: isinstance(screen, QuizApp))


class SettingsScreen(Screen):
    def compose(self):
        return [
            Middle(
                Center(
                    Container(
                        Static("Меню Налаштувань", id="title"),
                        Button("Змінити тему", id="btn_theme", variant="primary"),
                        Button("Назад", id="btn_back", variant="error"),
                        id="menu-box",
                    )
                )
            ),
            Footer(),
        ]

    @on(Button.Pressed, "#btn_back")
    def action_go_back(self):
        self.app.pop_screen()

    @on(Button.Pressed, "#btn_theme")
    def action_toggle_theme(self):
        self.app.action_change_toggle()


class DifficultyScreen(Screen):
    def compose(self):
        return [
            Middle(
                Center(
                    Container(
                        Static("Оберіть складність", id="title"),
                        Button("Легкий", id="btn_easy", variant="success"),
                        Button("Нормальний", id="btn_normal", variant="warning"),
                        Button("Складний", id="btn_hard", variant="error"),
                        Button("Назад", id="btn_back", variant="default"),
                        id="menu-box",
                    )
                )
            ),
            Footer(),
        ]

    @on(Button.Pressed, "#btn_easy")
    def select_easy(self):
        self.app.push_screen(QuizGridScreen("btn_easy"))

    @on(Button.Pressed, "#btn_normal")
    def select_normal(self):
        self.app.push_screen(QuizGridScreen("btn_normal"))

    @on(Button.Pressed, "#btn_hard")
    def select_hard(self):
        self.app.push_screen(QuizGridScreen("btn_hard"))

    @on(Button.Pressed, "#btn_back")
    def action_go_back(self):
        self.app.pop_screen()


class TaskRadioScreen(Screen):
    def __init__(self):
        super().__init__()
        self.answered = False
    def compose(self):
        task = self.app.current_task

        if "code_lines" in task:
            options_list = [f"{i + 1}: {line}" for i, line in enumerate(task["code_lines"])]
        else:
            options_list = task.get("options", [])

        return [
            Header(),
            Static(task["question"]),
            RadioSet(*[RadioButton(opt) for opt in options_list]),
            Button("Відповісти", id="btn_action", variant="success"),
            Button("Назад", id="btn_back", name="back", variant="error"),
            Footer(),
        ]

    @on(Button.Pressed, "#btn_action")
    def handle_action_button(self, event: Button.Pressed):
        action_btn = event.button

        if not self.answered:
            radio_set = self.query_one(RadioSet)

            if radio_set.pressed_index is None:
                self.notify("Будь ласка, оберіть варіант відповіді!", severity="warning")
                return

            self.answered = True

            if radio_set.pressed_index == self.app.current_task["correct"]:
                self.app.correct_count += 1
                self.notify("Правильно!", severity="information")
            else:
                self.app.incorrect_count += 1
                self.notify("Неправильно!", severity="error")

            action_btn.label = "Наступний рівень"
            action_btn.variant = "primary"

        else:
            current_num = self.app.current_task_num
            current_diff = self.app.current_difficulty

            if current_num < 9:
                next_num = current_num + 1
                self.app.current_task_num = next_num
                self.app.current_task = TASKS_MAP[current_diff][next_num]
                self.app.switch_screen(TaskRadioScreen())
            else:
                next_diff = NEXT_DIFFICULTY.get(current_diff)
                if next_diff:
                    self.app.current_difficulty = next_diff
                    self.app.current_task_num = 1
                    self.app.current_task = TASKS_MAP[next_diff][1]
                    self.notify("Вітаємо! Перехід на новий рівень складності!", severity="information")
                    self.app.switch_screen(TaskRadioScreen())
                else:
                    self.app.switch_screen(ResultScreen())

    @on(Button.Pressed, "#btn_back")
    def action_go_back(self):
        self.app.pop_screen()

class QuizGridScreen(Screen):
    def __init__(self, difficulty_id: str = "btn_easy"):
        super().__init__()
        self.difficulty_id = difficulty_id

    def compose(self):
        return [
            Header(),
            Static("Оберіть завдання"),
            Grid(*[
                Button(str(num), id=f"task_{num}", classes="circle-btn") 
                for num in range(1, 10)
            ]),
            Button("Назад", id="btn_back", name="back", variant="error"),
            Footer(),
        ]

    @on(Button.Pressed, "#btn_back")
    def action_go_back(self):
        self.app.pop_screen()

    @on(Button.Pressed, ".circle-btn")
    def handle_task_selection(self, event: Button.Pressed):
        task_num = int(str(event.button.label))
        selected_tasks = TASKS_MAP.get(self.difficulty_id, {})

        if task_num in selected_tasks:
            self.app.current_difficulty = self.difficulty_id
            self.app.current_task_num = task_num
            self.app.current_task = selected_tasks[task_num]
            self.app.push_screen(TaskRadioScreen())
        else:
            self.notify(f"Завдання №{task_num} ще немає", severity="warning")


class QuizApp(App):
    BINDINGS = [
        ("q", "quit", "Вихід"),
        ("t", "change_toggle", "Змінити тему"),
    ]
    
    DEFAULT_CSS = """
    #menu-layout {
        width: 80;
        height: auto;
        align: center middle;
    }

    #menu-box {
        width: 40;
        height: auto;
        border: heavy $primary;
        padding: 1;
        margin-right: 2;
    }

    #stats-box {
        width: 35;
        height: auto;
        border: heavy $accent;
        padding: 1;
    }

    #menu-box Button {
        width: 100%;
        margin-bottom: 1;
    }

    #title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    """

    CSS_PATH = "style.css"

    def __init__(self):
        super().__init__()
        self.current_task = None
        self.current_task_num = 1
        self.current_difficulty = "btn_easy"
        self.correct_count = 0
        self.incorrect_count = 0
        
        self.high_score = 0
        self.high_score_correct = 0
        self.high_score_total = 0
        
        self.load_high_score()

    def load_high_score(self):
        if STATS_FILE.exists():
            try:
                with open(STATS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
                    self.high_score_correct = data.get("high_score_correct", 0)
                    self.high_score_total = data.get("high_score_total", 0)
            except Exception:
                pass

    def save_high_score(self):
        data = {
            "high_score": self.high_score,
            "high_score_correct": self.high_score_correct,
            "high_score_total": self.high_score_total
        }
        try:
            with open(STATS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def reset_stats(self):
        self.correct_count = 0
        self.incorrect_count = 0
        self.current_task_num = 1
        self.current_difficulty = "btn_easy"

    def update_high_score(self, percentage, correct, total):
        if percentage > self.high_score:
            self.high_score = percentage
            self.high_score_correct = correct
            self.high_score_total = total
            self.save_high_score()
            self.refresh_stats_display()

    def refresh_stats_display(self):

        try:
            stats_widget = self.query_one("#side-stats-text", Static)
            stats_widget.update(self.get_stats_text())
        except Exception:
            pass

    def get_stats_text(self) -> str:
        return (
            f"[b]🏆 Статистика[/b]\n\n"
            f"Рекорд:\n[yellow]{self.high_score}%[/yellow]\n\n"
            f"Правильних:\n[green]{self.high_score_correct}[/green] з {self.high_score_total}"
        )

    def compose(self):
        return [
            Middle(
                Center(
                    Horizontal(
                        Container(
                            Static("Головне меню", id="title"),
                            Button("Старт", id="btn_start", variant="success"),
                            Button("Рекорд (High Score)", id="btn_highscore", variant="warning"),
                            Button("Налаштування", id="btn_about", variant="primary"),
                            Button("Вихід", id="btn_exit", variant="error"),
                            id="menu-box",
                        ),
                        Container(
                            Static(self.get_stats_text(), id="side-stats-text"),
                            id="stats-box",
                        ),
                        id="menu-layout"
                    )
                )
            ),
            Footer(),
        ]

    def on_mount(self):
        self.refresh_stats_display()

    @on(Button.Pressed, "#btn_start")
    def start_quiz(self):
        self.reset_stats()
        self.push_screen(DifficultyScreen())

    @on(Button.Pressed, "#btn_highscore")
    def open_highscore_screen(self):
        self.push_screen(HighScoreScreen())

    @on(Button.Pressed, "#btn_about")
    def open_about_screen(self):
        self.push_screen(SettingsScreen())

    @on(Button.Pressed, "#btn_exit")
    def exit_app(self):
        self.exit()

    def action_change_toggle(self):
        self.theme = "textual-light" if self.theme == "textual-dark" else "textual-dark"

    def action_press_start(self):
        self.start_quiz()

    def action_press_about(self):
        self.open_about_screen()

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter" and isinstance(self.focused, Button):
            self.focused.press()


if __name__ == "__main__":
    app = QuizApp()
    app.run()