import random


def build_outcome_store(max_size):
    s = []
    for i in range(0, max_size+1):
        t = []
        for j in range(0, max_size+1):
            t.append(0)
        s.append(t)
    return s


def calculate_burnthrough(attacks, lock, damage, cap, crit_up=2):
    remaining_attacks = attacks
    hits_scored = 0
    crits_scored = 0
    all_crits = False

    while remaining_attacks > 0:
        for i in range(remaining_attacks):
            roll = random.randint(1, 6)
            if roll >= lock + crit_up:
                # crit
                crits_scored += damage
            elif roll >= lock:
                # hit
                if all_crits:
                    crits_scored += damage
                else:
                    hits_scored += damage
            else:
                # die is gone
                remaining_attacks -= 1

            # cap reached, done
            if hits_scored + crits_scored >= cap:
                if all_crits:
                    # since all current dice are crits, return crits up to the cap, dropping any extra
                    return hits_scored, (cap - hits_scored)
                else:
                    # since we had no crits in previous rolls, drop any excess hits and take the crits instead
                    return (cap - crits_scored), crits_scored

            # if any crits, every next roll is crits
            if crits_scored > 0:
                all_crits = True

    return hits_scored, crits_scored

def get_burnthrough_table(lock, attacks, damage, cap, crit_up=2, numTries=100000):
    i = 0
    results = build_outcome_store(cap)
    while i < numTries:
        h, c = calculate_burnthrough(attacks, lock, damage, cap, crit_up)
        results[h][c] += 1
        i += 1
    return results

def output_simple_table(name, results, lock, attacks, damage, cap, crit_up=2, numTries=100000):
    print(name + " ( Lock " + str(lock) + "+, attacks: " + str(attacks) + ", damage: " + str(damage) + ", burnthrough(" + str(cap) + ") )")
    line = str.ljust("", 10) + "|"
    for i in range(0, len(results), damage):
        line += str.ljust(str(i) + " crits", 10) + "|"
    print(line)

    for hits, crits in enumerate(results):
        if hits % damage > 0:
            continue
        line = str.ljust(str(hits) + " hits", 10) + "|"
        for crit, count in enumerate(crits):
            if crit % damage > 0:
                continue
            if count > 0:
                line += str.ljust(str(round(count * 100 / numTries, 1)) + "%", 10) + "|"
            else:
                line += str.ljust("-", 10) + "|"
        print(line)
    print()

def output_simple_csv(results):
    line = " ," + str(0) + " crits" + ","
    for i in range(1, len(results)):
        line += str(i) + " crits" + ","
    print(line)

    for hits, crits in enumerate(results):
        line = str(hits) + " hits" + ","
        for crit, count in enumerate(crits):
            if count > 0:
                line += str(count) + ","
            else:
                line += str(0) + ","
        print(line)


def test_ship(name, lock, attacks, damage, cap, crit_up=2, numTries=100000):
    if lock == "mauler":
        for i in range(2, 7): # because range is not inclusive but we do care about 6+
            output_simple_table(name + " vs A" + str(i) + "+", get_burnthrough_table(i, attacks, damage, cap, crit_up, numTries), i, attacks, damage, cap, crit_up, numTries)
    else:
        output_simple_table(name, get_burnthrough_table(lock, attacks, damage, cap, crit_up, numTries), lock, attacks, damage, cap, crit_up, numTries)

print("Scourge:")
test_ship("Nosferatu", 3, 3, 3, 18, 2, 100000)
test_ship("Ifrit/Raiju", 3, 4, 1, 8, 2, 100000)
print()

print("UCM:")
test_ship("St Petersburg", 3, 2, 2, 8, 2, 100000)
test_ship("Berlin/Burnaby", 3, 2, 1, 6, 2, 100000)
test_ship("Vienna", 3, 2, 1, 3, 2, 100000)
test_ship("Tokyo", 3, 3, 2, 10, 2, 100000)

print("Shaltari:")
test_ship("Chromium", 2, 1, 1, 3, 2, 100000)
test_ship("Hematite", 2, 2, 1, 12, 2, 100000)
test_ship("Hematite on WF", 2, 4, 1, 12, 2, 100000)
print()
test_ship("Mercury", "mauler", 3, 1, 6, 2, 100000)
print()
test_ship("Uranium", "mauler", 6, 1, 12, 2, 100000)

# the mauler boys

print("PHR:")
test_ship("Pandora/Orpheus/Ajax", 3, 2, 1, 3, 2, 100000)
test_ship("Hector/Bellerophon", 3, 2, 2, 6, 2, 100000)
test_ship("Sarpedon", 3, 2, 2, 10, 2, 100000)
test_ship("Romulus", 3, 5, 1, 14, 2, 100000)
test_ship("Romulus (OC)", 3, 5, 2, 14, 2, 100000)

print("Resistance:")
test_ship("Armstrong", "mauler", 2, 2, 6, 2, 100000)
