EXP_REWARDS = {"D": 10, "C": 25, "B": 50, "A": 100, "S": 250}

COIN_REWARDS = {"D": 5, "C": 15, "B": 30, "A": 60, "S": 150}


def calculate_quest_reward(rank: str) -> tuple[int, int]:
    """
    Menghitung jumlah EXP dan Koin berdasarkan rank quest.
    """
    rank_upper = rank.upper()
    if rank_upper not in EXP_REWARDS or rank_upper not in COIN_REWARDS:
        raise ValueError(f"Rank tidak valid: {rank}")

    return EXP_REWARDS[rank_upper], COIN_REWARDS[rank_upper]


def process_level_up(current_level: int, current_exp: int) -> tuple[int, int]:
    """
    Menghitung kenaikan level berdasarkan akumulasi EXP.
    Menggunakan rumus threshold = current_level * 100.
    """
    if current_level < 1:
        raise ValueError("Level harus dimulai dari 1 atau lebih")
    if current_exp < 0:
        raise ValueError("EXP tidak bisa negatif")

    while True:
        threshold = current_level * 100
        if current_exp >= threshold:
            current_exp -= threshold
            current_level += 1
        else:
            break

    return current_level, current_exp


def process_shop_payment(current_coins: int, item_cost: int) -> int:
    """
    Memvalidasi transaksi pembelian item di shop.
    """
    if current_coins < 0 or item_cost <= 0:
        raise ValueError("Koin tidak bisa negatif dan harga item harus lebih dari 0")

    if current_coins < item_cost:
        raise ValueError("Koin tidak cukup")

    return current_coins - item_cost
