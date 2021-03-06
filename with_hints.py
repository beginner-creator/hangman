import random
import string 
import re

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    
    with open(WORDLIST_FILENAME, 'r') as inFile:
        wordlist = inFile.readline().split()
        print(f'{len(wordlist)} words loaded.')
        return wordlist
        

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# -----------------------------------
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''

    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    print(f'You guessed the word! {secret_word}')
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''

    return "".join([letter + " " if letter in letters_guessed else "_ " for letter in secret_word])


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''

    return "".join([c for c in string.ascii_lowercase if c not in letters_guessed])


def check_guess(guess, secret_word):
    '''
    guess: a letter that the user guessed
    secret_word: the word the user is guessing
    returns: boolean, True if the letter is in the word, False if the letter is not
    '''

    return guess in secret_word


def num_unique_letters(secret_word):
    '''
    secret_word: the work the user is guessing
    returns: the number of unique letters in secret_word
    '''

    return len("".join(set(secret_word)))


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''

    my_word = list(my_word.replace(' ', ''))
    other_word = list(other_word)
    letters_guessed = ''
    
    for letter in my_word:
        letters_guessed += letter
        
    if len(my_word) == len(other_word):
        for g, a in zip(my_word, other_word):
            if g != a and g != '_':
                return False
            elif g == a or g == '_':
                if g == '_' and a in letters_guessed:
                    return False
                continue
        return True
    else:
        return False
    

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''

    current_word = str(my_word.replace(' ',''))
    current_word = str(current_word.replace('_', '.'))
    regex = re.compile(r'\b' + current_word + r'\b')
    matches = re.findall(regex, str(wordlist))
    all_matches = []
   
    for match in matches:
        if match_with_gaps(my_word, match) is True:
            all_matches.append(match)
    return print(all_matches)
            
    if len(matches) == 0:
        print('No matches found')


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''

    lives = 6
    warnings = 3
    letters_guessed = ''

    print('Welcome to the Game of Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
        
    while not is_word_guessed(secret_word, letters_guessed) and lives > 0:
        print(get_guessed_word(secret_word, letters_guessed))
        print(f'You have {lives} guesses left.')
        print(f'Available Letters: {get_available_letters(letters_guessed)}')
        print('-------------------------')
        guess = input('Guess a letter or * for a hint: ').lower()

        if guess == secret_word:  # check if the entire word was guessed
            break
        elif guess == '*':
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        elif guess in letters_guessed:  # check for duplicates
            warnings -= 1
            print(f'You have guessed this letter before: {guess}. You have {warnings} warnings left.')
        elif guess not in string.ascii_lowercase:  # check for invalid input
            warnings -= 1
            print(f'Oops, that is not a letter: {guess}. You have {warnings} warnings left.')
        else:  # valid and not duplicates
            letters_guessed += guess
            if check_guess(guess, secret_word):
                print('Good guess!')
            elif guess in ('aeiou'):
                lives -= 2
            else:
                print(f'Oops, the letter "{guess}" is not in the word!')
                lives -= 1
        if warnings <= 0:
            warnings = 1
            lives -= 1
        if lives == 0:
            print(f'Sorry the word was: {secret_word}.')

if __name__ == "__main__": 
    
    hangman_with_hints(choose_word(wordlist))
