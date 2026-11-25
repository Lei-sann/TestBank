import random



def generate_deposit_amount() -> float:
    return round(random.uniform(1000, 9000), 2)

def generate_transfer_amount(balance: float) -> float:
    return round(random.uniform(500.0, min(10000.0, balance)), 2)

def generate_deposit_amount_for_insufficient_funds_transfer() -> float:
    return round(random.uniform(1000, 5000), 2)

def generate_transfer_amount_exceeding_balance(balance: float) -> float:
    return round(balance + random.uniform(1, 1000), 2)

def generate_credit_amount() -> float:
    return round(random.uniform(5000, 15000), 2)

def generate_partial_credit_repay_amount(credit_amount: float) -> float:
    return round(random.uniform(1, credit_amount - 0.01), 2)

def calculate_balance_after_deposit(
        initial_balance: float,
        deposit_amount: float) -> float:
    return initial_balance + deposit_amount

def calculate_account_1_balance_after_transfer(
        balance: float,
        transfer_amount: float) -> float:
    return balance - transfer_amount

def calculate_account_2_balance_after_transfer(
        balance: float,
        transfer_amount: float) -> float:
    return balance + transfer_amount

def calculate_balance_after_credit_request(
        balance: float,
        credit_amount: float) -> float:
    return balance + credit_amount

def calculate_balance_after_credit_repay(
        balance: float,
        credit_amount: float) -> float:
    return balance - credit_amount
