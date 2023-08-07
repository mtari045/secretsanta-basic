import random

def generate_secret_santa(names):
    participants = names.copy()
    random.shuffle(participants)
    
    pairings = []
    for i in range(len(participants)):
        giver = participants[i]
        receiver = participants[(i + 1) % len(participants)]
        pairings.append((giver, receiver))
    
    return pairings

def main():
    participants = []
    while True:
        name = input("Enter participant's name (or type 'done' to finish): ")
        if name.lower() == 'done':
            break
        participants.append(name)
    
    if len(participants) < 2:
        print("You need at least two participants to do a Secret Santa.")
    elif len(participants) % 2 != 0:
        print("You need an even number of participants for Secret Santa.")
    else:
        pairings = generate_secret_santa(participants)
        print("\nSecret Santa Pairings:")
        for giver, receiver in pairings:
            print(f"{giver} -> {receiver}")

if __name__ == "__main__":
    main()
