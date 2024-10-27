# Завдання 1


from collections import UserDict
import re
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    pass


class Phone(Field):
    # реалізація класу
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate_phone(phone):
        return bool(re.match(r"^\d{10}$", phone))
    
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return True
        return False

    def edit_phone(self, old_phone_number, new_phone_number):
        if self.remove_phone(old_phone_number):
            self.add_phone(new_phone_number)
            return True
        return False

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.today()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year +1)
        return (next_birthday - today).days

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "No birthday"
        return f"Contact name: {self.name.value}, phones: [{phones}], Birthday: {birthday_str}" 


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False


    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today()
        next_week = today + timedelta(days=7)
        for record in self.data.values():
            if record.birthday:
                next_birthday = record.birthday.value.replace(year=today.year)
                if today <= next_birthday <= next_week:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays
    

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John", "15.08.1990")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    jane_record = Record("Jane", "20.11.1985")
    jane_record.add_phone("0987654321")
    book.add_record(jane_record)

    print("Contacts in AddressBook:")
    print(book)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223335")
    print("n\After editing John's phone:")
    print(john)

    found_phone = john.find_phone("5555555555")
    print (f"\nFound phone for {john.name}: {found_phone}")

    book.delete("Jane")
    print(("\nAfter deleting Jane:"))
    print(book)
    
    print("\nUpcoming birthdays in the next week:")
    upcoming = book.get_upcoming_birthdays()
    for record in upcoming:
        print(record)

    