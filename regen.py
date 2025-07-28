import random
import csv
from datetime import datetime

# --- Introduction / Disclaimer ---
print("This tool generates realistic-looking credit card data for testing purposes.")
print("** All generated data is fictional and NOT linked to real accounts. **\n")

# Prompt user for BIN and validate it
while True:
    bin_input = input("Enter BIN (6–12 digits): ").strip()
    if not bin_input.isdigit():
        print("Invalid input. Please enter only digits for the BIN.")
        continue
    if not (6 <= len(bin_input) <= 12):
        print("BIN length must be between 6 and 12 digits. Please try again.")
        continue
    # If valid, break out of loop
    break

# Prompt for number of card profiles (default 100 if input is empty)
num_input = input("How many card profiles to generate? (Press Enter for default 100): ").strip()
if num_input == "":
    num_cards = 100
else:
    try:
        num_cards = int(num_input)
        if num_cards < 1:
            print("Number of profiles must be at least 1. Defaulting to 100.")
            num_cards = 100
    except ValueError:
        print("Invalid number. Defaulting to 100 profiles.")
        num_cards = 100

# Get current date for expiry calculations
now = datetime.now()
current_year = now.year
current_month = now.month

# Prepare to collect generated data (for optional CSV saving)
card_profiles = []  # will hold tuples of (card_number, expiry, cvv, zip)

# Print header for output table
print(f"\nGenerating {num_cards} fake card profile(s) using BIN prefix {bin_input}...")
print(f"{'Card Number':<16}  {'Expiry':<7}  {'CVV':<3}  {'ZIP':<5}")
print("-" * 36)  # separator line for clarity

# Generate each card profile
for _ in range(num_cards):
    # 1. Generate a 16-digit card number with Luhn check:
    prefix = bin_input
    # Determine how many random digits to add (to make 15 digits before the check digit)
    digits_needed = 15 - len(prefix)  
    # Generate the filler digits randomly
    account_digits = "".join(str(random.randint(0, 9)) for _ in range(digits_needed))
    partial_number = prefix + account_digits  # 15-digit number (without the check digit)
    # Compute Luhn check digit for the partial number:
    total = 0
    # Starting from the rightmost digit of partial_number, double every second digit
    for i, digit_char in enumerate(reversed(partial_number)):
        digit = int(digit_char)
        if i % 2 == 0:
            # i=0 is the rightmost digit of partial_number (which is in the "units" place of the full number)
            # Double every second digit (so this actually doubles the digits in the odd positions of the full number)
            doubled = digit * 2
            # If doubling results in two digits, sum them (equivalent to subtracting 9 for any result 10-18)
            total += doubled if doubled < 10 else doubled - 9
        else:
            # For the other digits, just add them as is
            total += digit
    # Calculate the check digit that makes the total a multiple of 10
    check_digit = (10 - (total % 10)) % 10
    card_number = partial_number + str(check_digit)

    # 2. Generate a realistic expiration date 1–5 years in the future:
    years_ahead = random.randint(1, 5)
    exp_year = current_year + years_ahead
    if years_ahead == 1:
        # If only 1 year ahead, choose a month at or beyond the current month to ensure ~1 year minimum
        exp_month = random.randint(current_month, 12)
    else:
        exp_month = random.randint(1, 12)
    # Format expiry as MM/YY (two-digit month and two-digit year)
    expiry = f"{exp_month:02d}/{exp_year % 100:02d}"

    # 3. Generate a random 3-digit CVV (000–999):
    cvv = f"{random.randint(0, 999):03d}"

    # 4. Generate a random 5-digit ZIP code (00000–99999):
    zip_code = f"{random.randint(0, 99999):05d}"

    # Print the generated profile line
    print(f"{card_number:<16}  {expiry:<7}  {cvv:<3}  {zip_code:<5}")
    # Store the profile for later saving
    card_profiles.append((card_number, expiry, cvv, zip_code))

# Ask user if they want to save the results to a CSV file
save_choice = input("\nSave results to CSV file? (y/n): ").strip().lower()
if save_choice.startswith('y'):
    filename = f"{bin_input}_cards.csv"
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(["Card Number", "Expiry", "CVV", "ZIP"])
        # Write each card profile as a row
        for profile in card_profiles:
            writer.writerow(profile)
    print(f"Results saved to {filename}")
else:
    print("Results were not saved to a file.")

