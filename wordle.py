# wordle.py

# Author: Alexis Demetriou (G20970098)

# Email: ADemetriou5@uclan.ac.uk

# Description: The Wordle.py program demonstrates the Wordle game in 2 modes: autoplay and interactive-play mode.
# Wordle is a word-based game. The game name is a play on the surname of its creator, Josh Wardle. The game
# experienced viral growth in late 2021: “...the number of players exploded from 90 on November 1 to 300,000 on
# January 2 and more than 2 million a week later” (statista.com). The game was bought by the New York Times for an
# undisclosed amount (estimated to be 2-3 million dollars) in January, 2022.

# to read file word by word is reused from the website:
# https://www.geeksforgeeks.org/python-program-to-read-file-word-by-word/
# The definition of the function print_frequencies is reused from the website:
# https://www.geeksforgeeks.org/python-frequency-of-each-character-in-string/and
# The definition of the function find_words_with_letters is reused from the website:
# https://stackoverflow.com/questions/5227524/use-function-to-return-a-list-of-words-containing-required-letters
# The nested-if structure is adapted from the lecture slides week 1, slide 61.

import random
import time


def print_frequencies(words: [str]):
    global sort_orders
    """
    Prints the frequencies for each letter 'a' to 'z', as found in the given list of words.
    :param words: a list of string containing the words to count the letters for
    """
    frequencies = {}  # each occurrence frequency using naive method

    for word in words:  # using naive method to get count of each element in string
        for char in word:  # take a letter from a word
            if char in frequencies:  # check if the letter is in the list
                frequencies[char] += 1
            else:  # if not, then create a new character with number one assigned
                frequencies[char] = 1

    sort_orders = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    # with this function we can assign characters with their frequency in descending order by their frequency


def find_words_with_letters(words: [str], letters: [str]) -> [str]:
    global word_length
    """
    Find all words in the given list, which match all the given letters.
    For example for letters ['a', 'd', 'n'] and words list ['and', 'din', 'aid', 'dan'], return ['and',
    'dan'].
    :param words: the list of words to be checked
    :param letters: the list of letters to be matched
    :return: a sublist of words which match the given characters
    """
    matched_words = []
    if len(letters) == word_length:  # we check if word length is 5
        for word in words:  # for each word from the text words "wordles.txt"
            for letter in letters:  # for each letter from the word
                if letter not in word:  # if the letter is not in the word
                    break  # then exclude the word

            else:  # else block executes if no break occurred
                matched_words.append(word)

    return matched_words  # send the list back to main program


def get_user_guess() -> [str]:
    """Get a user guess input, validate, and return the guess."""
    while True:  # continue looping until you get a valid guess
        guess_input = input("Enter a 5-letter word: ")

        if guess_input == 'Q' or guess_input == 'q':  # if the guess input is 'Q' or 'q'
            print("Thank you for playing Wordle! Bye!")
            quit()  # then quit the game

        # here we overwrite guess with the filtered guess
        error, guess_input = validate(guess_input)
        if error is None:  # if the guess input is correct
            break  # then stop looping

        print(error)  # show the input error to the user, as appropriate
    return guess_input  # return the guess input to the main program


def validate(guess_word: [str]) -> tuple[None, str] | tuple[str, str]:
    global dictionary_words, word_length, incorrect
    """
    Validate a guess from a user.

    Return tuple of [None if no error or a string containing
    the error message, the guess].
    :param guess:
    """
    incorrect = False
    if len(guess_word) == 0:  # if no guess is entered
        incorrect = True
        return print("You have not entered a word!"), guess_word  # return an error message and the guess input

    if len(guess_word) != word_length:  # guesses must be the same as the input word
        incorrect = True
        return print(str(guess_word) + " is not " + str(word_length) + " letters long!"), guess_word
        # return an error message and the guess input

    if guess_word not in dictionary_words:  # guesses must also be words from the word list
        incorrect = True
        return print(str(guess_word) + " is not in the list of accepted words!"), guess_word
        # return an error message and the guess input
    return None, guess_word  # return only the guess input


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
    output = ["gray" for _ in range(len(secret))]  # the output is assumed to be incorrect to start,
    # and as we progress through the checking, update each position in our output list
    counted_pos = set()

    for index, (expected_char, guess_char) in enumerate(zip(secret, check_word)):
        # first we check for correct words in the correct positions
        # and update the output accordingly
        if expected_char == guess_char:  # a correct character in the correct position
            output[index] = "green"
            counted_pos.add(index)

    for index, guess_char in enumerate(check_word):  # now we check for the remaining letters that are in incorrect positions.
        # if the guessed character is in the correct word, we need to check the other conditions. the easiest
        # one is that if we have not already guessed that letter in the correct place.
        if guess_char in secret and output[index] != "green":  # first, what are all the positions the guessed character is present in
            positions = []
            pos = secret.find(guess_char)
            while pos != -1:
                positions.append(pos)
                pos = secret.find(guess_char, pos + 1)  # have we accounted for all the positions
            for _ in positions:  # if we have not accounted for the correct position of this letter yet
                output[index] = "yellow"
                break  # break out of the "for pos in positions" loop

    return output  # return the list of parses


def find_word(words: [str], grays: [str], yellows: {}, greens: {}):
    """
    Given a list of words and constraints, it returns suitable words, if they exist, otherwise the constant 'None'.
    The constraints are:
    - grays: A list of characters which are known to not exist in the target word
    - yellows: A dictionary of characters to sets of indices. The keys are characters, and the
    corresponding values
    are sets of integers, indicating the indices where it is known that the corresponding character is NOT at.
    - greens: A dictionary of characters to sets of indices. The keys are characters, and the
    corresponding values are sets of integers, indicating the indices where it is known that the corresponding character
    is found at.
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
    words_list_alpha, words_list_beta, matched_words_list = [], [], []
    for word in words:  # for each word from the list
        for letter in grays:  # for each letter from the word
            if letter in word:  # if the letter is in the word
                break  # then exclude the word

        else:  # else block executes if no break occurred
            words_list_alpha.append(word)

    for word in words_list_alpha:  # for each word from the list
        for letter in yellows:  # for each letter from the word
            for i in range(len(word)):
                if letter in word[i] and i == yellows[letter]:
                    # if the letter is in the word and has the letter in same position
                    break  # then exclude the word

        else:  # else block executes if no break occurred
            words_list_beta.append(word)

    for word in words_list_beta:  # for each word from the list
        for letter in greens:  # for each letter from the word
            for i in range(len(word)):
                if letter in word[i] and i != greens[letter]:
                    # if the letter is in the word but has the letter in different position
                    break  # then exclude the word

        else:  # else block executes if no break occurred
            matched_words_list.append(word)

    return matched_words_list  # return the list of suitable words


if __name__ == '__main__':  # main program
    dictionary_words = []  # a list which will contain words from t a text file "wordles.txt"
    sort_orders = []  # a list which will contain sorted frequencies of characters in descending order
    word_length = 5  # word length
    num_of_guesses = 0
    incorrect = False
    start = True

    with open('wordles.txt', 'r') as file:  # opening the text file
        for line in file:  # reading each line
            for word in line.split():  # reading each word
                dictionary_words.append(word)  # assign words to the list

    print_frequencies(dictionary_words)

    all_characters = [i[0] for i in sort_orders]
    # select only letters from the dictionary and assign them to the new list "all_characters"
    five_most_freq_letters = all_characters[0:5]  # select the first five letters from the list "all_characters"

    s_words = find_words_with_letters(dictionary_words, five_most_freq_letters)

    while start:
        random_word = random.choice(dictionary_words)  # choose a secret word from the text file "wordles.txt"
        random_cpu_choice = random.choice(s_words)  # computer chooses a random world from the text file "wordles.txt"
        all_words = dictionary_words
        # print the game instructions to the user
        print("*** Welcome to the Wordle game! ***\n")
        while True:
            # the while loop will run continuously until the user enters the correct wordle or types the letter "q" in the input terminal.
            start_input = input("Select mode: [0] for Autoplay or [1] to Play against the computer. Hit [Q] to Quit: ")
            if start_input == '0':  # if the input is '0'
                print("Worldle running in autoplay mode!")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                break
            if start_input == '1':  # if the input is '1'
                print("Challenge accepted! Can you guess the Secret Word?    [type q to Quit]")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                break
            if start_input == 'Q' or start_input == 'q':  # if the input is 'q' or 'Q'
                print("Bye!")
                quit()
            else:  # else print error message
                print("Invalid input")

        start = False
        while not start and start_input == '1':  # we use a continuous loop, since there could be a number
            # of different exit conditions from the game if we want to spruce it up.
            # get the user to guess something
            guess = get_user_guess()

            if not incorrect:  # if the guess input was correct
                num_of_guesses += 1
                result = check(random_word, guess)
                print(str(num_of_guesses) + " -> " + str(result))  # then display the number of guesses and the list of parses

            incorrect = False
            if random_word == guess:  # if the secret word is the same with the guess word
                if num_of_guesses == 1:  # if the number of guess equals to 1
                    print("Lucky or Genius! You found the wordle in just " + str(num_of_guesses) + " try!!!\n")
                else:
                    print("Congratulations! You found the wordle in " + str(num_of_guesses) + " tries!\n")
                start = True  # the program will start over again
                num_of_guesses = 0

        while not start and start_input == '0':  # we use a continuous loop, since there could be a number
            # of different exit conditions from the game if we want to spruce it up.
            # get the user to guess something
            time.sleep(1)  # we give some to the computer to choose a random word for the text file "wordles.txt"
            print("trying: " + random_cpu_choice)
            num_of_guesses += 1
            # display the guess when compared against the game word
            result = check(random_word, random_cpu_choice)
            yellows_chars, greens_chars = {}, {}
            grays_chars = [random_cpu_choice[gray] for gray in range(len(result)) if result[gray] == "gray"]
            # a list of characters which are known to not exist in the target word

            for yellow in range(len(result)):
                if result[yellow] == "yellow":
                    yellows_chars[random_cpu_choice[yellow]] = yellow
                    # a dictionary of characters to sets of indices. The keys are characters, and the corresponding values

            for green in range(len(result)):
                if result[green] == "green":
                    greens_chars[random_cpu_choice[green]] = green
                    # a dictionary of characters to sets of indices. The keys are characters, and the
                    # corresponding values are sets of integers, indicating the indices where it is known
                    # that the corresponding character is found at.

            m_words = find_word(all_words, grays_chars, yellows_chars, greens_chars)
            all_words = m_words  # assign suitable words in all words
            print("-> " + str(result))

            if random_word == random_cpu_choice:  # if the secret word is the same with the computers random word
                print("found in " + str(num_of_guesses) + " tries\n")
                start = True  # the program will start over again
                num_of_guesses = 0

            random_cpu_choice = random.choice(all_words)  # computer chooses a random world from the text file "wordles.txt"
