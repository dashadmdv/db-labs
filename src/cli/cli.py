from prettytable import PrettyTable
from src.controller.cli_controller import CLIController


class CLI:
    def __init__(self):
        self.controller = None
        self.exit_prompt = ", 0 - exit"
        self.back_prompt = ", 0 - go back"
        self.hint_prompt = " (enter a number): "

    def run(self):
        print('Hello! Setting up the database...')
        # here the database is created
        self.controller = CLIController()
