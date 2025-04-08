import inquirer
from termcolor import colored
from inquirer.themes import load_theme_from_dict as loadth


def get_action() -> str:

    theme = {
        'Question': {
            'brackets_color': 'bright_yellow'
        },
        'List': {
            'selection_color': 'bright_blue'
        },
    }

    question = [
        inquirer.List(
            "action",
            message=colored('Choose you action', 'light_yellow'),
            choices=[
                'Import data to db',
                'Aircraft',
                'Exit'
            ]
        )
    ]

    return inquirer.prompt(question, theme=loadth(theme))['action']


get_action()

    
