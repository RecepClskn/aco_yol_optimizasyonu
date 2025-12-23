#Ad: Recep
#Soyad: Çalışkan
#Numara: 2312721004
#Github Repo: https://github.com/RecepClskn/aco_yol_optimizasyonu.git

import numpy as np

def ant_colony_optimization(
    D,
    n_ants,
    n_iter,
    alpha=1.0,
    beta=3.0,
    rho=0.5,
    start_index=0,
    seed=None,
):
    """
    D: distance matrix (km), shape (n,n)
    Returns: best_tour (list of indices including return to start), best_length_km, history(list)
    """
    if seed is not None:
        np.random.seed(seed)

    D = np.array(D, dtype=float)
    n = D.shape[0]

    # self distances 0; avoid division by zero
    eps = 1e-12
    invD = 1.0 / np.maximum(D, eps)

    pher = np.ones((n, n), dtype=float)
    best_len = float("inf")
    best_tour = None
    history = []

    nodes = np.arange(n)

    for _ in range(n_iter):
        iter_best = float("inf")
        iter_best_tour = None

        tours = []
        lens = []

        for _a in range(n_ants):
            tour = [start_index]
            visited = set(tour)

            while len(tour) < n:
                i = tour[-1]

                desirability = np.zeros(n, dtype=float)
                for j in nodes:
                    if j not in visited and np.isfinite(D[i, j]) and i != j:
                        desirability[j] = (pher[i, j] ** alpha) * (invD[i, j] ** beta)

                s = desirability.sum()
                if s <= 0:
                    # fallback: choose any unvisited
                    candidates = [j for j in nodes if j not in visited]
                    nxt = int(np.random.choice(candidates))
                else:
                    probs = desirability / s
                    nxt = int(np.random.choice(nodes, p=probs))

                tour.append(nxt)
                visited.add(nxt)

            # return to start
            tour.append(start_index)

            length = 0.0
            ok = True
            for k in range(len(tour) - 1):
                a, b = tour[k], tour[k + 1]
                d = D[a, b]
                if not np.isfinite(d):
                    ok = False
                    break
                length += d

            if not ok:
                length = float("inf")

            tours.append(tour)
            lens.append(length)

            if length < iter_best:
                iter_best = length
                iter_best_tour = tour

        # Evaporation
        pher *= (1.0 - rho)

        # Deposit (only finite tours)
        for tour, length in zip(tours, lens):
            if not np.isfinite(length) or length <= 0:
                continue
            deposit = 1.0 / length
            for k in range(len(tour) - 1):
                a, b = tour[k], tour[k + 1]
                pher[a, b] += deposit

        # Track global best
        if iter_best < best_len:
            best_len = iter_best
            best_tour = iter_best_tour

        history.append(best_len)

    return best_tour, best_len, history
