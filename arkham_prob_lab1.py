from math import comb
import random

N_total = 33  # 30 обычных + 2 персональные + 1 базовая слабость
W = 5         # число активов-оружия в колоде Роланда
P = 1         # «Патрульный» (ally), не сбрасываем при муллигане
H = 5         # стартовая рука

def hypergeom_no_success(N, K, n):
    return comb(N-K, n) / comb(N, n)

# Теория
N_other = N_total - W - P
p_k0_b0 = comb(W, 0) * comb(P, 0) * comb(N_other, H) / comb(N_total, H)
p_k0_b1 = comb(W, 0) * comb(P, 1) * comb(N_other, H - 1) / comb(N_total, H)

p_fail_r5 = hypergeom_no_success(N_total - H, W, 5)
p_fail_r4 = hypergeom_no_success(N_total - H, W, 4)

p_theory_success = 1 - (p_k0_b0 * p_fail_r5 + p_k0_b1 * p_fail_r4)

# Эмпирика
def simulate_one_trial(seed=None):
    rng = random.Random(seed)
    deck = ['W'] * W + ['B'] * P + ['O'] * (N_total - W - P)
    rng.shuffle(deck)
    hand = deck[:H]
    rest = deck[H:]
    keep = [c for c in hand if c in ('W', 'B')]
    replace = [c for c in hand if c == 'O']
    draw_n = len(replace)
    drawn = rest[:draw_n]
    final_hand = keep + drawn
    return any(c == 'W' for c in final_hand)

def run_simulation(n_trials=200, seed=7):
    rng = random.Random(seed)
    return sum(simulate_one_trial(seed=rng.randrange(1<<30)) for _ in range(n_trials)) / n_trials

if __name__ == "__main__":
    print("p_theory_success =", p_theory_success)
    print("empirical (200)  =", run_simulation(200))