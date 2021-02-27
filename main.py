import random
import sqlite3


class Database:
    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

    def insert(self, card_number, pin):
        self.cursor.execute(f'INSERT INTO card (number, pin) VALUES ({card_number}, {pin})')
        self.connection.commit()

    def create_table(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
        self.connection.commit()

    def drop(self):
        self.cursor.execute('DROP TABLE IF EXISTS card;')
        self.connection.commit()

    def select(self):
        return self.cursor.execute('SELECT number, pin FROM card;')

    def exit(self):
        self.connection.close()


class BankAccount:
    def __init__(self):
        self.iin = 400000
        self.card_number = ""
        self.pin = ""
        self.balance = 0

    def generate_card_number(self):
        odd_digits = []
        even_digits = []
        even_digits_mult = []
        odd_new = []
        customer_number = random.randint(100000000, 1000000000)
        customer_number_list = list(str(self.iin) + str(customer_number))
        odd_digits = customer_number_list[-2::-2]
        even_digits = customer_number_list[-1::-2]
        for digit in even_digits:
            digit = int(digit)
            digit *= 2
            if digit > 9:
                digit -= 9
                even_digits_mult.append(digit)
            else:
                even_digits_mult.append(digit)
        
        for digit_odd in odd_digits:
            digit_odd = int(digit_odd)
            odd_new.append(digit_odd)
        
        odd_sum = sum(odd_new)
        even_sum = sum(even_digits_mult)
        overall_sum = odd_sum + even_sum
        if overall_sum % 10 == 0:
            checksum_digit = 0
        else:
            checksum_digit = 10 - (overall_sum % 10)
        self.card_number = str(self.iin) + str(customer_number) + str(checksum_digit)

    def generate_pin(self):
        self.pin = str(random.randint(1000, 10000))

    def if_login(self, data, card_number, pin):
        for row in data:
            if str(card_number) in row and str(pin) in row:
                return True
        return False

    def balance_of_account(self):
        return self.balance


def main():
    random.seed()
    db = Database('card.s3db')
    db.create_table()
    while True:
        print("\n1. Create an account\n2. Log into account\n0. Exit")
        choice = int(input())
        if choice == 1:
            bank_account = BankAccount()
            bank_account.generate_card_number()
            bank_account.generate_pin()
            print(f"\nYour card has been created\nYour card number:\n{bank_account.card_number}\nYour card PIN:\n{bank_account.pin}")
            db.insert(bank_account.card_number, bank_account.pin)
        elif choice == 2:
            print("Enter your card number:")
            entered_card_number = int(input())
            print('Enter your PIN:')
            entered_pin = int(input())
            data = db.select()
            if bank_account.if_login(data, entered_card_number, entered_pin):
                print("You have successfully logged in!")
                while True:
                    print("\n1. Balance\n2. Log out\n0. Exit")
                    choice_tologin = int(input())
                    if choice_tologin == 1:
                        balance = bank_account.balance_of_account()
                        print(f"Balance: {balance}")
                    elif choice_tologin == 2:
                        print("You have successfully logged out!")
                        break
                    elif choice_tologin == 0:
                        choice = 0
                        break
            else:
                print("Wrong card number or PIN!")
        if choice == 0:
            print("Bye!")
            db.exit()
            break


if __name__ == '__main__':
    main()