import six
import configparser

from pyfiglet import figlet_format
from pyconfigstore import ConfigStore
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict)

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

config = configparser.ConfigParser()

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
})

def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)


def ask(type, name, message, validator=None, choices=[]):
    questions = [
        {
            'type': type,
            'name': name,
            'message': message,
            'validator': validator,
        },
    ]
    if choices:
        questions[0].update({
            'choices': choices,
        })
    answers = prompt(questions, style=style)
    return answers


def run():
    from main import SteamGifts as SG

    def askCookie():
        cookie = ask(type='input',
                     name='cookie',
                     message='Enter PHPSESSID cookie (Only needed to provide once):')
        config['DEFAULT']['cookie'] = cookie['cookie']

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        return cookie['cookie']

    log("SteamGifts Bot", color="blue", figlet=True)
    log("Welcome to SteamGifts Bot!", "green")
    log("Created by: github.com/stilManiac", "white")

    config.read('config.ini')
    if not config['DEFAULT'].get('cookie'):
        cookie = askCookie()
    else:
        re_enter_cookie = ask(type='confirm',
                            name='reenter',
                            message='Do you want to enter new cookie?')['reenter']
        if re_enter_cookie:
            cookie = askCookie()
        else:
            cookie = config['DEFAULT'].get('cookie')

    gift_type = ask(type='list',
                 name='gift_type',
                 message='Select type:',
                 choices=[
                     'All',
                     'Wishlist',
                     'Recommended',
                     'Copies',
                     'DLC',
                     'New'
                 ])['gift_type']

    s = SG(cookie, gift_type)
    s.start()


if __name__ == '__main__':
    run()