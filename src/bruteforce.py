import argparse
import csv
import logging
from itertools import combinations

LOGGER = logging.getLogger(__name__)

def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

def read_csv_file(filename):

    stocks = []
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug("Reading CSV file")
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            stock = {
                'name': row['Actions #'],
                'cost': float(row['Coût par action (en euros)']),
                'profit_percentage': float(row['Bénéfice (après 2 ans)'][:-1]),
            }
            if LOGGER.isEnabledFor(logging.DEBUG):
                LOGGER.debug(f"Read stock: {stock}")
            stocks.append(stock)
    LOGGER.info(f"CSV file read successfully, {len(stocks)} stocks found")
    return stocks


def calculate_combination(combination):
    """
    Calculate cost and profit for a combination of stocks
    :param combination: tuple of stock (Dict)
    :return: total cost and profit
    """
    total_cost = 0
    total_profit = 0
    if LOGGER.isEnabledFor(logging.DEBUG): # needed to not calculate the fstrings and have a good execution time
        LOGGER.debug(f"Calculating combination: {combination}")

    for stock in combination:
        total_cost += stock['cost']
        stock_profit = stock['cost'] * (stock['profit_percentage'] / 100)
        total_profit += stock_profit

    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(f"Combination calculated: {total_cost=}, {total_profit=}")
    return total_cost, total_profit


def find_best_combination(stocks, max_budget=500):
    """
    Find the best combination of stocks for a maximum budget
    :param stocks: list of stocks (Dict)
    :param max_budget: maximum budget
    :return: best combination for this maximum budget
    """
    best_combination = []
    best_profit = 0
    best_cost = 0
    
    for size in range(len(stocks) + 1):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(f"Testing combinations of size {size}")
        # calculate cost and profit for all combination found
        for combination in combinations(stocks, size):
            total_cost, total_profit = calculate_combination(combination)
            
            if total_cost <= max_budget and total_profit > best_profit: # found a better combination
                best_combination = combination
                best_profit = total_profit
                best_cost = total_cost
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug(f"{best_combination=}, {best_profit=}, {best_cost=}")
    return best_combination, best_profit, best_cost


def main():
    # get argument from command line
    parser = argparse.ArgumentParser(description='Bruteforce stocks')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('--max_budget', type=float, default=500, help='Maximum budget')
    args = parser.parse_args()
    verbose = args.verbose
    max_budget = args.max_budget

    setup_logging(verbose=verbose)

    filename = "../data/Liste+d'actions+-+P7+Python+-+Feuille+1.csv"

    stocks = read_csv_file(filename)

    best_combination, best_profit, best_cost = find_best_combination(stocks, max_budget)

    print("RESULTS : ")
    print(f"Profit after 2 years : {best_profit:.2f}")
    print(f"Cost: {best_cost}€")

    for stock in best_combination:
        print(f"{stock['name']} - {stock['cost']}€")

if __name__ == "__main__":
    main()
