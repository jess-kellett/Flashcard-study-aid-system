import random
import httpx

Base = "http://127.0.0.1:8000"

cards = httpx.get(f"{Base}/cards").json()
random.shuffle(cards)

score = 0 
for card in cards: 
    print(f"\n[{card['topic']}] {card['question']}")
    input("  (press Enter to reveal)")
    print(f"  Answer: {card['answer']}")
    if input("  Did you get it? [y/n] ").lower() == "y":
        score += 1

print(f"\n{score} / {len(cards)} correct")