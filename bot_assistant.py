from collections import UserDict


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        return "Add record succes"


class Record:
    def __init__(self, name, *phones):
        self.name = name
        self.phones = []
        for item in phones:
            self.add_phone(item)

    def add_phone(self, phone):
        for item in self.phones:
            if item == phone:
                return "The phone is exist"
        self.phones.append(phone)
        return "Add phone succes"

    def change_phone(self, old_phone, new_phone):
        if old_phone == new_phone:
            return "Old and new phones should be different"
        for item in self.phones:
            if item == new_phone:
                return "The new phone is already exist"
        for i, item in enumerate(self.phones):
            if item == old_phone:
                self.phones[i] = new_phone
                return "Change succes"
        return "The phone is not found"

    def remove_phone(self, phone):
        for item in self.phones:
            if item == phone:
                self.phones.remove(phone)
                return "Remove phone success"
        return "The phone is not found"


class Field:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value
    
    def __ne__(self, other):
        return self.value != other.value


class Name(Field):
    pass


class Phone(Field):
    pass


def input_error(func):
    def wrapper(*args):
        try:
            if not args[1].isalpha():
                raise KeyError
            if func.__name__ != "phone":
                for i in range(2, len(args)):
                    if not args[i].isdecimal():
                        raise ValueError
            return func(*args)
        except KeyError:
            return "Enter user name correctly"
        except ValueError:
            return "Enter phone(s) number(s) correctly"
        except IndexError:
            return "Give me name (and phone(s) is needed) please"
    return wrapper


@input_error
def add(*args):
    for key in address_book.data.keys():
        if key.casefold() == args[1].casefold():
            return "The contact is exist"
    return address_book.add_record(Record(Name(args[1].title()), *map(Phone, args[2:])))


@input_error
def change(*args):
    for key in address_book.data.keys():
        if key.casefold() == args[1].casefold():
            return address_book.data[args[1].title()].change_phone(Phone(args[2]), Phone(args[3]))
    return "The name is not found"


def exit():
    return "Good bye!"


def hello():
    return "Can I help you?"


def no_command():
    return "Unknown command"


@input_error
def phone(*args):
    for key, value in address_book.items():
        if key.casefold() == args[1].casefold():
            return f"The contact:\n{key}: {', '.join([i.value for i in value.phones])}\n"
    return "The contact is not found"


def show_all():
    if not address_book:
        result = "The address book is empty"
    else:
        result = "All contacts:\n"
        for key, value in address_book.items():
            result += f"{key}: {', '.join([i.value for i in value.phones])}\n"
    return result


def parser(text: str) -> tuple[callable, tuple[str]|None]:
    if text.casefold().startswith("add"):
        return add, text.strip().split()
    elif text.casefold().startswith("change"):
        return change, text.strip().split()
    elif text.casefold() == "good bye" or text.casefold() == "bye" or text.casefold() == "close" or text.casefold() == "exit":
        return exit, None
    elif text.casefold() == "hello":
        return hello, None
    elif text.casefold().startswith("phone"):
        return phone, text.strip().split()
    elif text.casefold() == "show all":
        return show_all, None
    return no_command, None


def main():
    while True:
        user_input = input(">>> ")
        command, data = parser(user_input)
        if data:
            result = command(*data)
        else:
            result = command()
        print(result)
        if result == "Good bye!":
            break


if __name__ == "__main__":
    address_book = AddressBook()
    main()