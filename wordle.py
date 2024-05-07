# wordle.py

# Author: Alexis Demetriou

# Email: ADemetriou5@uclan.ac.uk

# Description: The Wordle.py program demonstrates the Wordle game in 2 modes: autoplay and interactive-play mode.
# Wordle is a word-based game. The game name is a play on the surname of its creator, Josh Wardle. The game
# experienced viral growth in late 2021: “...the number of players exploded from 90 on November 1 to 300,000 on
# January 2 and more than 2 million a week later” (statista.com). The game was bought by the New York Times for an
# undisclosed amount (estimated to be 2-3 million dollars) in January 2022.

# to read file word by word is reused from the website:
# https://www.geeksforgeeks.org/python-program-to-read-file-word-by-word/
# The definition of the function print_frequencies is reused from the website:
# https://www.geeksforgeeks.org/python-frequency-of-each-character-in-string/and
# The definition of the function find_words_with_letters is reused from the website:
# https://stackoverflow.com/questions/5227524/use-function-to-return-a-list-of-words-containing-required-letters
# The nested-if structure is adapted from the lecture slides week 1, slide 61.

import random
import time


def get_words_from_file(file_with_words_path):
    # Initialize an empty list to store words
    words_list = []

    # Open the file in read mode
    with open(file_with_words_path, 'r') as file:
        # Read each line in the file
        for line in file:
            # Remove leading and trailing whitespace and store the word
            word = line.strip()
            words_list.append(word)

    return words_list


def bucket_sort_desc(frequencies):
    max_freq = max(frequencies.values())  # Find the maximum frequency
    buckets = [[] for _ in range(max_freq + 1)]

    # Distribute characters into buckets based on their frequencies
    [buckets[max_freq - freq].append(char) for char, freq in frequencies.items()]

    # Concatenate characters from buckets into a single list
    sorted_chars = []
    [sorted_chars.extend(bucket) for bucket in buckets]

    return sorted_chars


def print_frequencies(words: [str]):
    """
    Prints the frequencies for each letter 'a' to 'z', as found in the given list of words.
    :param words: a list of string containing the words to count the letters for
    """
    frequencies = {}
    # Count the frequencies of each letter in the words
    for word in words:
        for char in word:
            if char in frequencies:  # Ensure the character is a letter
                frequencies[char] += 1  # Convert to lowercase and increment frequency
            else:
                frequencies[char] = 1

    sorted_chars = bucket_sort_desc(frequencies)

    # Print the frequencies
    [print(char + ": " + str(frequencies[char])) for char in sorted_chars]


def find_top_chars(words: [str]):
    frequencies = {}
    # Count the frequencies of each letter in the words
    for word in words:
        for char in word:
            if char in frequencies:  # Ensure the character is a letter
                frequencies[char] += 1  # Convert to lowercase and increment frequency
            else:
                frequencies[char] = 1

    sorted_chars = bucket_sort_desc(frequencies)

    return sorted_chars[0:5]


def find_words_with_letters(words: [str], letters: [str]) -> [str]:
    """
    Find all words in the given list, which match all the given letters.
    For example for letters ['a', 'd', 'n'] and words list ['and', 'din', 'aid', 'dan'], return ['and', 'dan'].
    :param words: the list of words to be checked
    :param letters: the list of letters to be matched
    :return: a sublist of words which match the given characters
    """
    sublist_words = []
    for word in words:
        for letter in letters:
            if letter not in word:
                break
        else:
            sublist_words.append(word)

    return sublist_words  # send the list back to main program


def check(secret: str, check_word: str) -> [str]:
    """
    Given a secret word and a check_word, which must be of equal length, return a list of words which
    are either 'gray', 'yellow' or 'green'. The semantics match the rules of Wordle:
    - 'gray' if the checked character does not appear in the secret word
    - 'yellow' if the checked character does appear in the secret word, but not in the same position
    - 'green' if the checked character matches the character at the same position in the secret word.
    For example for the secret word 'store' and check_word 'raise', it should return the list
    ['yellow', 'gray', 'gray', 'yellow', 'green']
    :param secret: a word to be checked against
    :param check_word: another word of equal length to be checked based on Wordle's rules
    :return: a list containing the values 'gray', 'yellow', 'green'
    """
    list_wordle = []

    # Iterate over each pair of corresponding letters in the secret and check_word
    for secret_letter, check_letter in zip(secret, check_word):
        if secret_letter == check_letter:
            list_wordle.append("green")
        elif check_letter in secret:
            list_wordle.append("yellow")
        else:
            list_wordle.append("gray")

    return list_wordle


def find_word(words: [str], grays: [str], yellows: {}, greens: {}):
    """
    Given a list of words and constraints, it returns a suitable word, if it exists, otherwise the constant 'None'.
    The constraints are:
    - grays: A list of characters which are known to not exist in the target word
    - yellows: A dictionary of characters to sets of indices. The keys are characters, and the corresponding values
        are sets of integers, indicating the indices where it is known that the corresponding character is NOT at.
    - greens: A dictionary of characters to sets of indices. The keys are characters, and the corresponding values
        are sets of integers, indicating the indices where it is known that the corresponding character is found at.
    For example, the call:
        find_word(['batch', 'ozone'], 'abcd', {'n': {2}, 'z': {2, 3}}, {'o': {0, 2}, 'e': {4}})
    It looks for a word in the given list so that it does not contain any of the characters 'a', 'b', 'c', 'd'.
    Also it contains 'n' but not at index 2, and 'z' but not at indices 2, or 3.
    Finally, it contains 'o' at indices 0, 2, and it also contains 'e' at index 4.
    This for example excludes 'batch' but could return 'ozone'.
    remember that the indices are 0-base which means the first position is index 0, and the last one (5th) is index 4.
    :param words: the list of words to be checked against the constraints
    :param grays: a list of characters in the form of a string (gray constraint)
    :param yellows: a dictionary of characters to set of indices (yellow constraint)
    :param greens: a dictionary of characters to set of indices (green constraint)
    :return: a word from the given list which satisfies the constraints, or None if none is found
    """
    matched_words = []
    possible_matched_words = []
    possible_matched_words2 = []

    # Check gray constraint
    for word in words:
        for gray_letter in grays:
            if gray_letter in word:
                break
        else:
            possible_matched_words.append(word)

    for word in possible_matched_words:
        # Check yellow constraint
        for yellow_letter, yellow_indices in yellows.items():
            if yellow_letter not in word:
                break
            found = False
            # Find all occurrences of yellow_letter in the word
            letter_indices = [i for i, char in enumerate(word) if char == yellow_letter]
            # Check if any occurrence satisfies the constraint
            for index in letter_indices:
                if index in yellow_indices:
                    found = True
                    break
            if found:
                break
        else:
            # If no violation is found, add the word to possible_matched_words2
            possible_matched_words2.append(word)

    for word in possible_matched_words2:
        # Check green constraint
        found = True
        for green_letter, green_indices in greens.items():
            if green_letter in word:
                # Get all indices of green_letter in the word
                letter_indices = [i for i, char in enumerate(word) if char == green_letter]
                # Check if all specified indices are covered
                for index in green_indices:
                    if index not in letter_indices:
                        found = False
                        break
                if not found:
                    break
            else:
                found = False
                break
        if found:
            matched_words.append(word)

    if matched_words:
        return matched_words[0]
    else:
        return None


def find_matched_words(words: [str], grays: [str], yellows: {}, greens: {}):
    """
    Given a list of words and constraints, it returns a suitable word, if it exists, otherwise the constant 'None'.
    The constraints are:
    - grays: A list of characters which are known to not exist in the target word
    - yellows: A dictionary of characters to sets of indices. The keys are characters, and the corresponding values
        are sets of integers, indicating the indices where it is known that the corresponding character is NOT at.
    - greens: A dictionary of characters to sets of indices. The keys are characters, and the corresponding values
        are sets of integers, indicating the indices where it is known that the corresponding character is found at.
    For example, the call:
        find_word(['batch', 'ozone'], 'abcd', {'n': {2}, 'z': {2, 3}}, {'o': {0, 2}, 'e': {4}})
    It looks for a word in the given list so that it does not contain any of the characters 'a', 'b', 'c', 'd'.
    Also it contains 'n' but not at index 2, and 'z' but not at indices 2, or 3.
    Finally, it contains 'o' at indices 0, 2, and it also contains 'e' at index 4.
    This for example excludes 'batch' but could return 'ozone'.
    remember that the indices are 0-base which means the first position is index 0, and the last one (5th) is index 4.
    :param words: the list of words to be checked against the constraints
    :param grays: a list of characters in the form of a string (gray constraint)
    :param yellows: a dictionary of characters to set of indices (yellow constraint)
    :param greens: a dictionary of characters to set of indices (green constraint)
    :return: a word from the given list which satisfies the constraints, or None if none is found
    """
    matched_words = []
    possible_matched_words = []
    possible_matched_words2 = []

    # Check gray constraint
    for word in words:
        for gray_letter in grays:
            if gray_letter in word:
                break
        else:
            possible_matched_words.append(word)

    for word in possible_matched_words:
        # Check yellow constraint
        for yellow_letter, yellow_indices in yellows.items():
            if yellow_letter not in word:
                break
            found = False
            # Find all occurrences of yellow_letter in the word
            letter_indices = [i for i, char in enumerate(word) if char == yellow_letter]
            # Check if any occurrence satisfies the constraint
            for index in letter_indices:
                if index in yellow_indices:
                    found = True
                    break
            if found:
                break
        else:
            # If no violation is found, add the word to possible_matched_words2
            possible_matched_words2.append(word)

    for word in possible_matched_words2:
        # Check green constraint
        found = True
        for green_letter, green_indices in greens.items():
            if green_letter in word:
                # Get all indices of green_letter in the word
                letter_indices = [i for i, char in enumerate(word) if char == green_letter]
                # Check if all specified indices are covered
                for index in green_indices:
                    if index not in letter_indices:
                        found = False
                        break
                if not found:
                    break
            else:
                found = False
                break
        if found:
            matched_words.append(word)

    if matched_words:
        return matched_words
    else:
        return None


# class WordValidator:
#     def __init__(self):
#         self.items = []

def validate(guess_word: [str], words_list: [list]) -> tuple[None, bool] | tuple[str, bool]:
    """
    Validate a guess from a user.

    Return tuple of [None if no error or a string containing
    the error message, the guess].
    :param guess_word:
    """
    word_length = 5
    if not guess_word:
        return "You have not entered a word!", True
    elif len(guess_word) != word_length:
        return guess_word + " is not " + str(word_length) + " letters long!", True
    elif guess_word.lower() not in words_list:
        return guess_word + " is not in the list of accepted words!", True
    elif any(char.isdigit() for char in guess_word):
        return guess_word + " contains digits!", True
    elif any(not char.isalpha() for char in guess_word):
        return guess_word + " contains symbols!", True
    else:
        return None, False


def get_user_guess(words_list: [list]) -> tuple[str, bool]:
    """Get a user guess input, validate, and return the guess."""
    while True:  # continue looping until you get a valid guess
        guess_input = input("Enter a 5-letter word: ")

        if guess_input.lower() == 'quit' or guess_input.lower() == 'q':  # if the guess input is 'quit'
            print("Thank you for playing Wordle! Bye!")
            quit()  # then quit the game

        # here we overwrite guess with the filtered guess
        error, incorrect = validate(guess_input, words_list)
        if error is not None:  # if the guess input is correct
            print(error)  # show the input error to the user, as appropriate
            continue  # then stop looping
        else:
            break

    return guess_input, incorrect  # return the guess input to the main program


def wordle_demo(words_list: [list]):
    print_frequencies(wordles)
    print()
    print(find_words_with_letters(['and', 'din', 'aid', 'dan'], ['a', 'd', 'n']))
    print(find_words_with_letters(words_list, ['s', 'e', 'a', 'o', 'r']))
    print()
    print(check('level', 'sofas'))
    print(check('store', 'crazy'))
    print(check('crane', 'raise'))
    print()
    print(find_word(['batch', 'ozone'], ['a', 'b', 'c', 'd'], {'n': {2}, 'z': {2, 3}}, {'o': {0, 2}, 'e': {4}}))
    print(find_word(words_list, ['i', 'o', 'u', 'l', 'd', 'w', 't'], {'s': {1, 2}, 'p': {3}}, {'s': {0}, 'a': {2}}))
    print(find_word(words_list, ['m'], {'p': {2, 3}, 'd': {0}}, {'a': {1, 4}}))
    print(find_word(words_list, ['a', 'e', 'i', 'o', 'u', 'y', 'r', 'w', 't'], {}, {}))
    print()


def main_game():
    print("*** Welcome to the text-based Wordle game. ***\n")
    print("I have guessed a secret word. Can you find it?")

    while True:
        random_word = random.choice(wordles)  # choose a secret word from the text file "wordles.txt"
        num_of_guesses = 0
        # print the game instructions to the user

        while True:
            # the while loop will run continuously until the user enters the correct wordle or types the letter "quit"
            # in the input terminal.
            print("Type:\n\"1\" for auto game,\n"
                  "\"2\" for interactive game,\n"
                  "\"3\" for wordle functions demonstration or\n"
                  "\"Quit\" or \"q\" to exit")
            start_input = input('Enter your choice: ')
            if start_input.lower() in ["quit", "q"]:  # if the input is 'quit'
                print("Bye!")
                quit()
            elif start_input == '1':  # if the input is '0'
                print("Worldle running in autoplay mode!")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                break
            elif start_input == '2':  # if the input is '1'
                print("Challenge accepted! Can you guess the Secret Word?    [type \"quit\" or \"q\" to Quit]")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                break
            elif start_input == '3':  # if the input is '1'
                print("~~~~~~~~~~~~~~~~~~~~")
                wordle_demo(wordles)
                break
            else:  # else print error message
                print("Invalid input")

        while True and start_input == '2':  # we use a continuous loop, since there could be a number
            # of different exit conditions from the game if we want to spruce it up.
            # get the user to guess something
            guess, incorrect = get_user_guess(wordles)

            if not incorrect:  # if the guess input was correct
                num_of_guesses += 1
                # then display the number of guesses and the list of parses
                print(str(num_of_guesses) + " -> " + str(check(random_word, guess)))

            if random_word == guess:  # if the secret word is the same with the guess word
                if num_of_guesses == 1:  # if the number of guess equals to 1
                    print("Lucky or Genius! You found the wordle in just " + str(num_of_guesses) + " try!!!\n")
                else:
                    print("Congratulations! You found the wordle in " + str(num_of_guesses) + " tries!\n")
                break

        if start_input == '1':  # we use a continuous loop, since there could be a number
            # of different exit conditions from the game if we want to spruce it up.
            # get the user to guess something
            all_words = wordles
            s_words = find_words_with_letters(wordles, find_top_chars(wordles))
            random_cpu_choice = random.choice(s_words)
            yellow_chars, green_chars = {}, {}
            grays_chars = []
            added_letters = set()  # Set to keep track of added letters

            while True:
                time.sleep(1)  # we give some to the computer to choose a random word for the text file "wordles.txt"
                print("Trying: " + random_cpu_choice)
                num_of_guesses += 1
                # display the guess when compared against the game word
                result = check(random_word, random_cpu_choice)
                print("-> " + str(result))

                if random_word == random_cpu_choice:  # if the secret word is the same with the computers random word
                    print("found in " + str(num_of_guesses) + " tries\n")
                    break  # the program will start over again

                # Iterate over each character and its corresponding color
                for index, colour in enumerate(result):
                    if colour == "gray":
                        letter = random_cpu_choice[index]
                        if letter not in added_letters:  # Check if letter has already been added
                            grays_chars.append(letter)  # Append letter to grays_chars list
                            added_letters.add(letter)  # Add letter to set of added letters

                # a list of characters which are known to not exist in the target word
                for index, colour in enumerate(result):
                    if colour == "yellow":
                        letter = random_cpu_choice[index]
                        if letter in yellow_chars:
                            yellow_chars[letter].add(index)
                        else:
                            yellow_chars[letter] = {index}

                    elif colour == "green":
                        letter = random_cpu_choice[index]
                        if letter in green_chars:
                            green_chars[letter].add(index)
                        else:
                            green_chars[letter] = {index}

                all_words = find_matched_words(all_words, grays_chars, yellow_chars, green_chars)

                if all_words is None:
                    print("No suitable words found. Exiting game.")
                    break

                print()
                # computer chooses a random world from the text file "wordles.txt"
                random_cpu_choice = random.choice(all_words)


if __name__ == '__main__':  # main program
    file_path = 'wordles.txt'  # Path to the text file
    wordles = get_words_from_file(file_path)  # Get all words from the text file

    main_game()
