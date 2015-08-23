# My sollution for mastermind.py

# --- MASTERMIND ---

import random

generated = str(random.randint(1000, 9999))


# randomly generated numbers

first = int(generated[0])
second = int(generated[1])
third = int(generated[2])
fourth = int(generated[3])

# inputted generated numbers

print("Guess the 4 numbers in as few tries as possible\n")

count = 0

print(generated)

while True:
    count = count + 1
    data = input(">")

    if(len(data) < 4) or (len(data) < 4):
        print("Please enter a four digit number")
    else:

        # now to deal with the data

        in_first = int(data[0])
        in_second = int(data[1])
        in_third = int(data[2])
        in_fourth = int(data[3])

        correct = 0

        if in_first == first:
            correct = correct + 1
        if in_second == second:
            correct = correct + 1
        if in_third == third:
            correct = correct + 1
        if in_fourth == fourth:
            correct = correct + 1

        print("*" * correct)

        if(correct == 4):
            print("Well done... That took you [" + str(count) + "] attempts!")



