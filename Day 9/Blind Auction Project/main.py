from art import logo
print(logo)
print("Welcome to the online Blind Auction program. Get started below.")
all_bids = {}
while True:
    name_input = input("What is your name?\n")
    bid = int(input("What is your bid? $"))

    all_bids[name_input] = bid

    more_bids = input("Are there any other bidders? Type 'yes' or 'no.'\n").lower()
    if more_bids == "yes":
        print("\n" * 50)
        continue
    elif more_bids == "no":
        highest_bid = max(all_bids.values())
        highest_bid_name = max(all_bids, key=all_bids.get)
        print(f"The winner is {highest_bid_name} with a bid of ${highest_bid}.")
        break

# TODO-3: Whether if new bids need to be added
# TODO-4: Compare bids in dictionary
