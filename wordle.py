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

from random import choice
from time import sleep
from typing import Optional, Union, List


class FileHandler:
    def __init__(self, file_with_words_path: [str], words_list: [list]):
        """
        Initializes a FileHandler object with the provided file path and an empty list to store words.
        :param file_with_words_path: a string representing the path to the file containing words
        :param words_list: a list to store the words read from the file
        """
        self.file_with_words_path = file_with_words_path
        self.words_list = words_list

    def get_words_from_file(self) -> [list]:
        """
        Reads words from the file and returns them as a list.
        :return: a list containing the words read from the file
        """
        # Open the file in read mode
        with open(self.file_with_words_path, 'r') as file:
            # Read each line in the file, remove leading and trailing whitespace and store the word
            self.words_list = [line.strip() for line in file]

        return self.words_list


class FrequencySorter:
    def __init__(self, words: [list]):
        """
        Initializes a FrequencySorter object with the provided list of words.
        :param words: a list of words to be used for frequency sorting
        """
        self.words = words
        self.frequencies = {}

    def bucket_sort_desc(self) -> [list]:
        """
        Performs bucket sort in descending order based on character frequencies.
        :return: a sorted list of characters based on their frequencies
        """
        max_freq = max(self.frequencies.values())  # Find the maximum frequency
        buckets = [[] for _ in range(max_freq + 1)]  # Create buckets for each possible frequency
        sorted_chars = []

        # Distribute characters into buckets based on their frequencies
        [buckets[max_freq - freq].append(char) for char, freq in self.frequencies.items()]

        # Concatenate characters from buckets into a single list
        [sorted_chars.extend(bucket) for bucket in buckets]

        return sorted_chars

    def sort_frequencies(self, command: [str]) -> Optional[List[str]]:
        """
        Prints the frequencies for each letter 'a' to 'z', as found in the given list of words.
        :param command: a list of string containing the words to count the letters for
        """
        self.frequencies = {}
        # Count the frequencies of each letter in the words
        for word in self.words:
            for char in word:
                if char in self.frequencies:  # Ensure the character is a letter
                    self.frequencies[char] += 1  # Convert to lowercase and increment frequency
                else:
                    self.frequencies[char] = 1

        sorted_chars = self.bucket_sort_desc()

        if command == "print":
            [print(char + ": " + str(self.frequencies[char])) for char in sorted_chars]  # Print the frequencies
        elif command == "returntopfive":
            return sorted_chars[:5]


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


def check(secret: [str], check_word: [str]) -> [str]:
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


def find_matched_words(words: [str], grays: [str], yellows: {}, greens: {}, command: [str]) -> Union[str, List[str], None]:
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
    Also, it contains 'n' but not at index 2, and 'z' but not at indices 2, or 3.
    Finally, it contains 'o' at indices 0, 2, and it also contains 'e' at index 4.
    This for example excludes 'batch' but could return 'ozone'.
    remember that the indices are 0-base which means the first position is index 0, and the last one (5th) is index 4.
    :param words: the list of words to be checked against the constraints
    :param grays: a list of characters in the form of a string (gray constraint)
    :param yellows: a dictionary of characters to set of indices (yellow constraint)
    :param greens: a dictionary of characters to set of indices (green constraint)
    :param command: either "word" or "list" to specify the return type
    :return: a word from the given list which satisfies the constraints, or None if none is found
    """
    matched_words = []

    # Check gray constraint
    for word in words:
        for gray_letter in grays:
            if gray_letter in word:
                break
        else:
            # Check yellow constraint
            for yellow_letter, yellow_indices in yellows.items():
                if yellow_letter not in word:
                    break
                # Find all occurrences of yellow_letter in the word
                letter_indices = [i for i, char in enumerate(word) if char == yellow_letter]
                # Check if any occurrence satisfies the constraint
                if set(letter_indices).intersection(yellow_indices):
                    break
            else:
                # Check green constraint
                found = True
                for green_letter, green_indices in greens.items():
                    if green_letter in word:
                        # Get all indices of green_letter in the word
                        letter_indices = [i for i, char in enumerate(word) if char == green_letter]
                        # Check if all specified indices are covered
                        if set(letter_indices).intersection(green_indices):
                            break
                    else:
                        found = False
                        break
                if found:
                    matched_words.append(word)

    if matched_words:
        if command == "word":
            return matched_words[0]
        elif command == "list":
            return matched_words
    else:
        return None


class WordValidator:
    def __init__(self, words_list: [list], word_length: [int]):
        """
        Initialize the WordValidator object.
        :param words_list: A list of accepted words.
        """
        self.words_list = words_list
        self.word_length = word_length

    def validate(self, guess_word: [str]) -> tuple[None, bool] | tuple[str, bool]:
        """
        Validate a guess from a user.
        Return tuple of [None if no error or a string containing
        the error message, the guess].
        :param guess_word: The word guessed by the user.
        :return: A tuple containing an error message and a boolean indicating if the guess is incorrect.
        """
        if not guess_word:
            # If the guess word is empty, return an error message and True flag indicating an incorrect guess
            return "You have not entered a word!", True
        elif len(guess_word) != self.word_length:
            # If the guess word length is not equal to the expected word length, return an error message and True flag
            return guess_word + " is not " + str(self.word_length) + " letters long!", True
        elif guess_word.lower() not in self.words_list:
            # If the guess word is not in the list of accepted words, return an error message and True flag
            return guess_word + " is not in the list of accepted words!", True
        elif any(char.isdigit() for char in guess_word):
            # If the guess word contains digits, return an error message and True flag
            return guess_word + " contains digits!", True
        elif any(not char.isalpha() for char in guess_word):
            # If the guess word contains symbols other than alphabetic characters, return an error message and True flag
            return guess_word + " contains symbols!", True
        else:
            # If none of the above conditions are met, return None (indicating no error) and False flag
            return None, False

    def get_user_guess(self) -> tuple[str, bool]:
        """
        Get a user guess input, validate, and return the guess.
        :return: A tuple containing the user guess and a boolean indicating if the guess is incorrect.
        """
        while True:  # continue looping until you get a valid guess
            guess_input = input("Enter a 5-letter word: ")

            if guess_input.lower() == 'quit' or guess_input.lower() == 'q':  # if the guess input is 'quit'
                print("Thank you for playing Wordle! Bye!")
                quit()  # then quit the game

            # here we overwrite guess with the filtered guess
            error, incorrect = self.validate(guess_input)

            if error is not None:  # if the guess input is correct
                print(error)  # show the input error to the user, as appropriate
                continue  # then stop looping
            else:
                break

        return guess_input, incorrect  # return the guess input to the main program


class WordleDemo:
    def __init__(self, words_list: [list]):
        """
        Initialize the WordleDemo object.
        :param words_list: A list of words to be used in the wordle demonstration.
        """
        self.words_list = words_list

    def wordle_demo(self):
        """
        Demonstrates various wordle-related functions.
        - Sorts and prints the frequencies of each letter in the words list.
        - Finds words containing specified letters.
        - Checks word compatibility.
        - Finds matched words based on constraints.
        """
        sorter.sort_frequencies("print")
        print()
        print(find_words_with_letters(['and', 'din', 'aid', 'dan'], ['a', 'd', 'n']))
        print(find_words_with_letters(self.words_list, ['s', 'e', 'a', 'o', 'r']))
        print()
        print(check('level', 'sofas'))
        print(check('store', 'crazy'))
        print(check('crane', 'raise'))
        print()
        print(find_matched_words(['batch', 'ozone'], ['a', 'b', 'c', 'd'], {'n': {2}, 'z': {2, 3}}, {'o': {0, 2}, 'e': {4}}, "word"))
        print(find_matched_words(self.words_list, ['i', 'o', 'u', 'l', 'd', 'w', 't'], {'s': {1, 2}, 'p': {3}}, {'s': {0}, 'a': {2}}, "word"))
        print(find_matched_words(self.words_list, ['m'], {'p': {2, 3}, 'd': {0}}, {'a': {1, 4}}, "word"))
        print(find_matched_words(self.words_list, ['a', 'e', 'i', 'o', 'u', 'y', 'r', 'w', 't'], {}, {}, "word"))
        print()


class WordleGame:
    def __init__(self, words_list: [list]):
        """
        Initialize the WordleGame object.
        :param words_list: A list of words for the game.
        """
        self.words_list = words_list

    def main_game(self):
        """
        Start the main Wordle game loop.
        """
        print("*** Welcome to the text-based Wordle game. ***\n")
        print("I have guessed a secret word. Can you find it?")

        while True:
            random_word = choice(self.words_list)  # choose a secret word from the text file "wordles.txt"

            while True:
                # the while loop will run continuously until the user enters the correct wordle or types the letter "quit"
                # in the input terminal.
                print("Type:\n\"1\" for auto game,\n"
                      "\"2\" for interactive game,\n"
                      "\"3\" for wordle functions demonstration or\n"
                      "\"Quit\" or \"q\" to exit")
                start_input = input('Enter your choice: ').lower()
                if start_input in ["quit", "q"]:  # if the input is 'quit'
                    print("Bye!")
                    quit()
                elif start_input == '1':  # if the input is '1'
                    print("Worldle running in autoplay mode!")
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    self.autoplay_game(random_word)
                    break
                elif start_input == '2':  # if the input is '2'
                    print("Challenge accepted! Can you guess the Secret Word?    [type \"quit\" or \"q\" to Quit]")
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    self.interactive_game(random_word)
                    break
                elif start_input == '3':  # if the input is '3'
                    print("~~~~~~~~~~~~~~~~~~~~")
                    wordle_demo.wordle_demo()
                    break
                else:  # else print error message
                    print("Invalid input")

    def autoplay_game(self, random_word: [str]):
        """
        Start the Wordle game in autoplay mode.
        :param random_word: The secret word chosen for the game.
        """
        num_of_guesses = 0
        all_words = self.words_list
        s_words = find_words_with_letters(self.words_list, sorter.sort_frequencies("returntopfive"))
        random_cpu_choice = choice(s_words)
        yellow_chars, green_chars = {}, {}
        grays_chars = []
        added_letters = set()  # Set to keep track of added letters

        while True:
            sleep(1)  # we give some to the computer to choose a random word for the text file "wordles.txt"
            print("Trying: " + random_cpu_choice)
            num_of_guesses += 1
            # display the guess when compared against the game word
            result = check(random_word, random_cpu_choice)
            print("-> " + str(result))

            if random_word == random_cpu_choice:  # if the secret word is the same with the computers random word
                print("found in " + str(num_of_guesses) + " tries\n")
                break  # the program will start over again

            # Iterate over each character and its corresponding color
            for i, colour in enumerate(result):
                if colour == "gray":
                    letter = random_cpu_choice[i]
                    if letter not in added_letters:  # Check if letter has already been added
                        grays_chars.append(letter)  # Append letter to grays_chars list
                        added_letters.add(letter)  # Add letter to set of added letters

            # a list of characters which are known to not exist in the target word
            for i, colour in enumerate(result):
                if colour == "yellow":
                    letter = random_cpu_choice[i]
                    if letter in yellow_chars:
                        yellow_chars[letter].add(i)
                    else:
                        yellow_chars[letter] = {i}
                elif colour == "green":
                    letter = random_cpu_choice[i]
                    if letter in green_chars:
                        green_chars[letter].add(i)
                    else:
                        green_chars[letter] = {i}

            all_words = find_matched_words(all_words, grays_chars, yellow_chars, green_chars, "list")

            if not all_words:
                print("No suitable words found. Exiting game.")
                break

            print()
            # computer chooses a random world from the list
            random_cpu_choice = choice(all_words)

    @staticmethod
    def interactive_game(random_word: [str]):
        """
        Start the Wordle game in interactive mode.
        :param random_word: The secret word chosen for the game.
        """
        num_of_guesses = 0

        while True:
            guess, incorrect = validator.get_user_guess()

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


if __name__ == '__main__':  # main program
    file_path = 'wordles.txt'  # Path to the text file
    words_list = []
    word_length = 5

    file_handler = FileHandler(file_path, words_list)
    words_list = file_handler.get_words_from_file()

    main_game = WordleGame(words_list)
    sorter = FrequencySorter(words_list)
    validator = WordValidator(words_list, word_length)
    wordle_demo = WordleDemo(words_list)

    main_game.main_game()
