import random
import requests

# Function to load words from the dictionary file
def load_dictionary(url):
    response = requests.get(url)
    words = response.text.splitlines()
    return words

# Function to apply substitutions to the password
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

# Function to generate a password from the dictionary
def generate_password(words, length=3):
    password_words = random.sample(words, length)
    raw_words = password_words  # Store the raw words for printing
    password = ''.join(apply_substitutions(word) for word in password_words)
    return password, raw_words  

# Main execution
if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/dolph/dictionary/master/popular.txt"
    words = load_dictionary(url)
    
    password, raw_words = generate_password(words)
    
    print("Generated Password:", password)
    print("Raw Words Used:", ', '.join(raw_words))