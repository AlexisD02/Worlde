# Worlde

## Description
The Wordle.py program demonstrates the Wordle game in 2 modes: autoplay and interactive-play mode. Wordle is a word-based game created by Josh Wardle. The game experienced viral growth in late 2021, with over 2 million players a week after January 2022. The game was later acquired by the New York Times.

### External References
- File reading functionality adapted from [GeeksforGeeks](https://www.geeksforgeeks.org/python-program-to-read-file-word-by-word/)
- Function to print character frequencies reused from [GeeksforGeeks](https://www.geeksforgeeks.org/python-frequency-of-each-character-in-string/)
- Function to find words containing specified letters reused from [Stack Overflow](https://stackoverflow.com/questions/5227524/use-function-to-return-a-list-of-words-containing-required-letters)

## Features
- Auto mode: The computer guesses the secret word automatically.
- Interactive mode: The user guesses the secret word interactively.
- Demonstrates various Wordle game functions.

## Functionality
- `get_words_from_file`: Reads words from a text file.
- `bucket_sort_desc`: Sorts characters in descending order of frequency.
- `print_frequencies`: Prints the frequencies of each letter in a word list.
- `find_words_with_letters`: Finds words containing specified letters.
- `check`: Checks a guessed word against the secret word.
- `find_matched_words`: Finds a suitable word based on given constraints.
- `validate`: Validates a user's guess.
- `get_user_guess`: Gets a guess from the user and validates it.
- `wordle_demo`: Demonstrates various Wordle game functions.
- `main_game`: Executes the main game loop.

## Usage
1. Run the program.
2. Choose auto, interactive, or demonstration mode.
3. Follow the prompts to play the game or view demonstrations.
4. Guess the secret word in interactive mode or let the computer guess in auto mode.
