import random
import requests
def load_dictionary(url):
    response = requests.get(url)
    words = response.text.splitlines()
    return words
def apply_substitutions(word):
    substitutions = {
        'a': '@',
        'e': '3',
        'i': '!',
        'o': '0',
        's': '$'
    }
    for original, substitute in substitutions.items():
        word = word.replace(original, substitute)
    return word

# Function to capitalize letters in a word
def random_capitalize(word):
    return ''.join(random.choice([char.upper(), char]) for char in word)
def capitalize_first_letter(word):
    return word.capitalize()

# Function to generate a password from the dictionary
def generate_password(words, length=3, random_case=False, capitalize_first=False):
    password_words = random.sample(words, length)
    raw_words = password_words  # Store the raw words for printing
    
    if capitalize_first:
        password = ''.join(capitalize_first_letter(apply_substitutions(word)) for word in password_words)
    else:
        password = ''.join(apply_substitutions(random_capitalize(word) if random_case else word) for word in password_words)

    return password, raw_words  

# Main execution
if __name__ == "__main__":
    url = "https://websites.umich.edu/~jlawler/wordlist"
    #"https://raw.githubusercontent.com/DwaipayanDutta/Password_Generator/refs/heads/main/words.txt"
    #https://websites.umich.edu/~jlawler/wordlist
    words = load_dictionary(url)

    # Parameters for password generation
    length = 3  # Number of words in the password
    random_case = True  # Set to True for random capitalization of letters
    capitalize_first = False  # Set to True to capitalize the first letter of each word

    password, raw_words = generate_password(words, length, random_case, capitalize_first)
    
    print("Generated Password:", password)
    print("Raw Words Used:", ', '.join(raw_words))