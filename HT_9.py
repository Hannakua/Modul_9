import sys


USERS = {}
  
def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return "No such user"
        except ValueError:
            return 'Give me user name and phone numberb, please'
        except IndexError:
            return 'Enter user name'
        except TypeError:
            return 'No data'
    return inner

@error_handler
def hello():
    name = input('Hello, I am Bot. What is your name? ')
    # checked  = True
    return f'Hello, {name}! Can I help you?'


def unknown_command(_):
    return "I don't understand this command. Please write command again or write help to see the possible command list."

@error_handler
def help(_):
    return "I am a bot. I accept the following commands: 'hello', 'add', 'change', 'show all', 'exit', 'goodbye', 'close'. For 'add' or 'change' commands please enter the command in sequence: user_name backspace user_number"

@error_handler
def add_user(args):
    name, phone_num = args
    USERS[name] = phone_num
    return f"Done. Contact {phone_num} for user {name} is saved."

@error_handler
def change_user(args):
    name, phone_num = args
    old_num=USERS[name]
    USERS[name] = phone_num
    return f'New phone number {phone_num} is saved for {name}. Old number {old_num} has been deleted.'

@error_handler
def phone_show(args):
    name = ''.join(args)
    number = USERS.get(name, f'user is not in phone book yet.')
    return f'Phone number for user {name} is: {number}.'


@error_handler
def show_all(_):
    result = '\n'
    if USERS == {}:
        result = "Not any record in phone book yet."
    else:
        for name, phone in USERS.items():
            result += f'Name: {name} phone: {phone}\n'
    return result

def exit(_):
    print('Good Bye!') 
    return sys.exit()

HANDLERS = {
    'help': help,
    'add': add_user,
    'show all': show_all,
    'exit': exit,
    'phone show': phone_show,
    'close': exit,
    'good bye': exit,
    'change': change_user,     
}


def find_command(user_input):
    command, *args = user_input.split()
    command = command.lstrip()

    try:
        handler = HANDLERS[command.lower()]
    except KeyError:
        if args:
            command = command + ' ' + args[0]
            args = args[1:]
        handler = HANDLERS.get(command.lower(), unknown_command)
    return handler, args


def main():
    print(hello())
    while True:
        user_input = input('Please enter command: ')
        if user_input=='':
            user_input = 'none'
        handler, *args = find_command(user_input)
        result = handler(*args)
        if not result:
            print('This information not found.')
            help()
        print(result)


if __name__ == "__main__":
    main()

# Бот принимает команды:
# "hello", отвечает в консоль "How can I help you?"
# "add ...". По этой команде бот сохраняет в памяти (в словаре например) новый контакт. 
# Вместо ... пользователь вводит имя и номер телефона, обязательно через пробел.
# "change ..." По этой команде бот сохраняет в памяти новый номер телефона для существующего контакта. 
# Вместо ... пользователь вводит имя и номер телефона, обязательно через пробел.
# "phone ...." По этой команде бот выводит в консоль номер телефона для указанного контакта. 
# Вместо ... пользователь вводит имя контакта, чей номер нужно показать.
# "show all". По этой команде бот выводит все сохраненные контакты с номерами телефонов в консоль.
# "good bye", "close", "exit" по любой из этих команд бот завершает свою роботу после того, как выведет в консоль "Good bye!".
# Все ошибки пользовательского ввода должны обрабатываться при помощи декоратора input_error. 
# Этот декоратор отвечает за возврат пользователю сообщений вида "Enter user name", "Give me name and phone please" и т.п. 
# Декоратор input_error должен обрабатывать исключения, которые возникают в функциях-handler (KeyError, ValueError, IndexError) 
# и возвращать соответствующий ответ пользователю.
# Логика команд реализована в отдельных функциях и эти функции принимают на вход одну или несколько строк и возвращают строку.
# Вся логика взаимодействия с пользователем реализована в функции main, все print и input происходят только там.
