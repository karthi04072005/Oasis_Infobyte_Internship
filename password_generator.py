import random
import string

def generate_command_line_password():
    """
    Runs the command-line password generator application.
    """
    print("--- 🔒 Random Password Generator ---")
    print("--------------------------------------")

    # 1. GET PASSWORD LENGTH
    try:
        # Get user input for length and convert it to an integer
        length = int(input("Enter the desired password length: "))
        if length <= 0:
            print("Error: Password length must be a positive number.")
            return
    except ValueError:
        print("Error: Invalid input. Please enter a whole number for length.")
        return

    # 2. GET CHARACTER TYPE PREFERENCES
    use_letters = input("Include letters? (y/n): ").strip().lower() == 'y'
    use_numbers = input("Include numbers? (y/n): ").strip().lower() == 'y'
    use_symbols = input("Include symbols? (y/n): ").strip().lower() == 'y'

    # 3. BUILD THE CHARACTER POOL
    # This string will hold all possible characters for the password
    character_pool = ""
    # This list will hold one guaranteed character from each selected set
    password_guaranteed = []

    if use_letters:
        character_pool += string.ascii_letters  # e.g., 'abc...xyzABC...XYZ'
        password_guaranteed.append(random.choice(string.ascii_letters))
    if use_numbers:
        character_pool += string.digits      # e.g., '0123456789'
        password_guaranteed.append(random.choice(string.digits))
    if use_symbols:
        character_pool += string.punctuation  # e.g., '!@#$%^&*'
        password_guaranteed.append(random.choice(string.punctuation))

    # 4. VALIDATE INPUT
    # Check if the user selected at least one character type
    if not character_pool:
        print("Error: You must select at least one character type (letters, numbers, or symbols).")
        return

    # Check if the requested length is at least as long as the number of guaranteed characters
    if length < len(password_guaranteed):
        print(f"Error: Length must be at least {len(password_guaranteed)} to include all selected character types.")
        return

    # 5. GENERATE THE PASSWORD
    # First, get the remaining characters needed
    remaining_length = length - len(password_guaranteed)
    
    # Create a list of random characters from the *entire* pool
    password_remaining = [random.choice(character_pool) for _ in range(remaining_length)]

    # Combine the guaranteed characters with the remaining ones
    final_password_list = password_guaranteed + password_remaining

    # Shuffle the final list to ensure randomness (so symbols aren't always at the end)
    random.shuffle(final_password_list)

    # 6. DISPLAY THE PASSWORD
    # Join the list of characters back into a single string
    password = "".join(final_password_list)

    print("\n--------------------------------------")
    print(f"✅ Your generated password is:")
    print(f"\n{password}\n")

# This line makes sure the function runs when you execute the script
if __name__ == "__main__":
    generate_command_line_password()