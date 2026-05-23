# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 10:42:18 2025

@author: Student
"""

#!/usr/bin/env python3
import os, random, time, json, sys
from colorama import init, Fore, Style

init(autoreset=True)
SAVE_FILE = "casino_save.json"

# Detect if running in Spyder
IN_SPYDER = any('SPYDER' in name for name in os.environ)

def slow(text, delay=0.02, newline=True):
    """Slower printing for animation, skips delay in Spyder"""
    if IN_SPYDER:  # Disable animation in Spyder
        print(text)
    else:
        for c in text:
            print(c, end="", flush=True)
            time.sleep(delay)
        if newline: print()

def clear():
    """Clears terminal; disabled in Spyder"""
    if not IN_SPYDER:
        os.system("cls" if os.name == "nt" else "clear")
    else:
        print("\n" * 3)

def load_balance():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE) as f:
                data = json.load(f)
                return data.get("balance", 1000)
        except:
            return 1000
    return 1000

def save_balance(balance):
    with open(SAVE_FILE, "w") as f:
        json.dump({"balance": balance}, f)

def get_bet(balance):
    while True:
        try:
            bet = int(input(Fore.CYAN + f"Your balance: ${balance}. Enter your bet: $"))
            if 1 <= bet <= balance:
                return bet
            slow(Fore.YELLOW + "Invalid bet. Try again.")
        except ValueError:
            slow(Fore.YELLOW + "Please enter a valid number.")

def print_header(title):
    clear()
    print(Fore.MAGENTA + "="*40)
    print(Fore.CYAN + f"🎲 {title.center(34)} 🎲")
    print(Fore.MAGENTA + "="*40)

# ===== Game Modes =====
def slots(balance):
    print_header("SLOT MACHINE")
    bet = get_bet(balance)
    symbols = ["🍒","🍋","💎","🔔","⭐","💰"]
    reels = [random.choice(symbols) for _ in range(3)]
    slow(Fore.YELLOW + "Spinning...", 0.05)
    time.sleep(1)
    print(Fore.GREEN + " | ".join(reels))

    if len(set(reels)) == 1:
        win = bet * 10
        slow(Fore.LIGHTGREEN_EX + f"💎 JACKPOT! You won ${win}!")
        balance += win
    elif len(set(reels)) == 2:
        win = bet * 2
        slow(Fore.GREEN + f"You won ${win}!")
        balance += win
    else:
        slow(Fore.RED + "No match. You lost.")
        balance -= bet
    input(Fore.YELLOW + "\nPress Enter to return to menu...")
    return balance

def blackjack(balance):
    print_header("BLACKJACK")
    bet = get_bet(balance)
    deck = [2,3,4,5,6,7,8,9,10,10,10,10,11]*4
    random.shuffle(deck)

    def val(hand):
        v = sum(hand)
        while v > 21 and 11 in hand:
            hand[hand.index(11)] = 1
            v = sum(hand)
        return v

    player, dealer = [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]
    while True:
        slow(Fore.CYAN + f"Your hand: {player} (total: {val(player)})")
        slow(Fore.CYAN + f"Dealer shows: [{dealer[0]}, ?]")
        if val(player) == 21:
            slow(Fore.GREEN + "Blackjack! You win!")
            balance += bet * 1.5
            return balance
        move = input("Hit or Stand? (h/s): ").lower()
        if move == "h":
            player.append(deck.pop())
            if val(player) > 21:
                slow(Fore.RED + "Bust! You lost.")
                balance -= bet
                return balance
        else:
            break

    while val(dealer) < 17:
        dealer.append(deck.pop())
    slow(Fore.CYAN + f"Dealer's hand: {dealer} (total: {val(dealer)})")

    if val(dealer) > 21 or val(player) > val(dealer):
        slow(Fore.GREEN + "You win!")
        balance += bet
    elif val(player) == val(dealer):
        slow(Fore.YELLOW + "Push. Your bet is returned.")
    else:
        slow(Fore.RED + "Dealer wins. You lost.")
        balance -= bet
    input(Fore.YELLOW + "\nPress Enter to return to menu...")
    return balance

def roulette(balance):
    print_header("ROULETTE")
    bet = get_bet(balance)
    choice = input(Fore.CYAN + "Bet on (r)ed, (b)lack, or number 0–36: ").lower()
    slow(Fore.YELLOW + "Spinning wheel...", 0.05)
    time.sleep(1.5)
    num = random.randint(0,36)
    color = "red" if num % 2 == 0 else "black"
    slow(Fore.MAGENTA + f"Result: {num} ({color})")

    if choice == "r" and color == "red" or choice == "b" and color == "black":
        slow(Fore.GREEN + f"You won ${bet}!")
        balance += bet
    elif choice.isdigit() and int(choice) == num:
        win = bet * 35
        slow(Fore.LIGHTGREEN_EX + f"JACKPOT! You won ${win}!")
        balance += win
    else:
        slow(Fore.RED + "You lost.")
        balance -= bet
    input(Fore.YELLOW + "\nPress Enter to return to menu...")
    return balance

def coin_flip(balance):
    print_header("COIN FLIP")
    bet = get_bet(balance)
    side = input(Fore.CYAN + "Heads or Tails? (h/t): ").lower()
    slow(Fore.YELLOW + "Flipping coin...", 0.05)
    time.sleep(1)
    result = random.choice(["h","t"])
    if side == result:
        slow(Fore.GREEN + f"You won ${bet}!")
        balance += bet
    else:
        slow(Fore.RED + "You lost.")
        balance -= bet
    input(Fore.YELLOW + "\nPress Enter to return to menu...")
    return balance

def poker(balance):
    print_header("POKER-LITE (HIGH CARD)")
    bet = get_bet(balance)
    deck = list(range(2,15))*4
    random.shuffle(deck)
    player, dealer = deck.pop(), deck.pop()
    slow(Fore.CYAN + f"Your card: {player} | Dealer’s card: ???")
    time.sleep(1)
    slow(Fore.CYAN + f"Dealer’s card: {dealer}")
    if player > dealer:
        slow(Fore.GREEN + f"You win ${bet}!")
        balance += bet
    elif player == dealer:
        slow(Fore.YELLOW + "It's a tie! Bet returned.")
    else:
        slow(Fore.RED + "Dealer wins. You lost.")
        balance -= bet
    input(Fore.YELLOW + "\nPress Enter to return to menu...")
    return balance

# ===== Main Menu =====
def main():
    balance = load_balance()
    while True:
        clear()
        print(Fore.MAGENTA + "="*40)
        print(Fore.LIGHTCYAN_EX + f"💰 TERMINAL CASINO DELUXE 💰".center(40))
        print(Fore.MAGENTA + "="*40)
        print(Fore.YELLOW + f"Balance: ${balance}")
        print("""
1. 🎰 Slots
2. ♠️ Blackjack
3. 🔴 Roulette
4. 🪙 Coin Flip
5. 🃏 Poker-Lite
6. 💾 Save & Exit
""")
        choice = input(Fore.CYAN + "Choose a game: ").strip()
        if choice == "1":
            balance = slots(balance)
        elif choice == "2":
            balance = blackjack(balance)
        elif choice == "3":
            balance = roulette(balance)
        elif choice == "4":
            balance = coin_flip(balance)
        elif choice == "5":
            balance = poker(balance)
        elif choice == "6":
            save_balance(balance)
            slow(Fore.YELLOW + "Progress saved. Goodbye, high roller!")
            break
        else:
            slow(Fore.RED + "Invalid choice.")
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + Fore.YELLOW + "Exiting... Goodbye!")
        sys.exit(0)
