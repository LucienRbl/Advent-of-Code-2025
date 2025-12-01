#! /usr/bin/env python3

def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]
    
def count_dial_stop_on_zeros(sequence: list[str]) -> int:
    number_of_zeros = 0
    current_number = 50
    for input in sequence:
        if input.startswith('R'):
            input = input.split('R')[1]
            current_number += int(input)
        elif input.startswith('L'):
            input = input.split('L')[1]
            current_number -= int(input)
        current_number %= 100
        if current_number == 0:
            number_of_zeros += 1
    return number_of_zeros

def count_dial_pass_upon_zeros(sequence: list[str]) -> int:
    number_of_zeros = 0
    current_number = 50
    for input in sequence:
        if input.startswith('R'):
            input = input.split('R')[1]
            steps = int(input)
            for _ in range(steps):
                current_number += 1
                current_number %= 100
                if current_number == 0:
                    number_of_zeros += 1
        elif input.startswith('L'):
            input = input.split('L')[1]
            steps = int(input)
            for _ in range(steps):
                current_number -= 1
                current_number %= 100
                if current_number == 0:
                    number_of_zeros += 1
    return number_of_zeros

if __name__ == '__main__':
    print(count_dial_stop_on_zeros(read_file('input.txt')))
    print(count_dial_pass_upon_zeros(read_file('input.txt')))
