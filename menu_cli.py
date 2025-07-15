from cipher import UltimateCipher
import sys
import re

def clear_screen():
    print("\033[H\033[J", end="")

def print_menu():
    print("\n=== Ultimate Cipher Tool ===")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")
    print("========================")

def validate_affine_key(a: int, b: int) -> bool:
    if not (1 <= a <= 25):
        print("Error: Affine key 'a' must be between 1 and 25")
        return False
    if not (0 <= b <= 25):
        print("Error: Affine key 'b' must be between 0 and 25")
        return False
    # Check if 'a' is coprime with 26
    if UltimateCipher()._gcd(a, 26) != 1:
        print("Error: Affine key 'a' must be coprime with 26")
        print("Valid values for 'a' are: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25")
        return False
    return True

def validate_vigenere_key(key: str) -> bool:
    if not key.isalpha():
        print("Error: Vigenere key must contain only alphabetic characters")
        return False
    return True

def get_input(prompt: str, validator=None, error_msg=None) -> str:
    while True:
        value = input(prompt).strip()
        if not value:
            print("Input cannot be empty. Please try again.")
            continue
        if validator and not validator(value):
            if error_msg:
                print(error_msg)
            continue
        return value

def get_int_input(prompt: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("Please enter a valid number")

def process_text(action: str):
    clear_screen()
    print(f"\n=== {action.capitalize()} Text ===")
    
    # Get text input
    text = get_input("Enter text: ")
    
    # Get Affine keys
    print("\n=== Affine Cipher Keys ===")
    while True:
        a = get_int_input("Enter Affine key 'a' (1-25): ", 1, 25)
        b = get_int_input("Enter Affine key 'b' (0-25): ", 0, 25)
        if validate_affine_key(a, b):
            break
    
    # Get Vigenere key
    print("\n=== Vigenere Cipher Key ===")
    vigenere_key = get_input(
        "Enter Vigenere key (alphabetic): ",
        lambda k: k.isalpha(),
        "Error: Vigenere key must contain only alphabetic characters"
    )
    
    # Get XOR key
    print("\n=== XOR Cipher Key ===")
    xor_key = get_input("Enter XOR key: ")
    
    # Process the text
    cipher = UltimateCipher()
    try:
        if action == "encrypt":
            result = cipher.encrypt(text, a, b, vigenere_key, xor_key)
        else:
            result = cipher.decrypt(text, a, b, vigenere_key, xor_key)
        
        print(f"\n=== Result ===")
        print(f"Original text: {text}")
        print(f"{action.capitalize()}ed text: {result}")
    except ValueError as e:
        print(f"\nError: {str(e)}")
    
    input("\nPress Enter to continue...")

def main():
    while True:
        clear_screen()
        print_menu()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            process_text("encrypt")
        elif choice == "2":
            process_text("decrypt")
        elif choice == "3":
            print("\nThank you for using Ultimate Cipher Tool!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main() 