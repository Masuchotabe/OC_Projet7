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
                'cost': int(row['Coût par action (en euros)']),
                'profit_percentage': float(row['Bénéfice (après 2 ans)'][:-1])
            }
            stock['profit'] = stock['cost'] * (stock['profit_percentage'] / 100)
            if LOGGER.isEnabledFor(logging.DEBUG):
                LOGGER.debug(f"Read stock: {stock}")
            stocks.append(stock)
    LOGGER.info(f"CSV file read successfully, {len(stocks)} stocks found")
    return stocks


def find_best_combination(stocks, max_budget=500):
    """
    Find the best combination of stocks for a maximum budget with basic greedy algorithm.
    :param stocks: list of stocks (Dict)
    :param max_budget: maximum budget
    :return: best combination for this maximum budget
    """
    best_combination = []
    total_profit = 0
    total_cost = 0

    # sort stocks by profit percentage
    stocks.sort(key=lambda stock: stock['profit_percentage'], reverse=True)

    for stock in stocks:
        stock_profit = stock['cost'] * (stock['profit_percentage'] / 100)
        if total_cost + stock['cost'] < max_budget:
            total_cost += stock['cost']
            total_profit += stock_profit
            best_combination.append(stock)

    return best_combination, total_profit, total_cost


def find_best_combination_dp(stocks, max_budget=500):
    """
    Find the best combination of stocks for a maximum budget with dynamic programming
    :param stocks: list of stocks (Dict)
    :param max_budget: maximum budget
    :return: best combination for this maximum budget
    """
    # création table vide de longueur max budget + 1 et hauteur nb stock + 1
    dp = [[0 for _ in range(max_budget + 1) ] for _ in range(len(stocks) + 1)]
    for stock_index in range(1, len(stocks)+1):  # parcours des lignes du tableau à partir de 1
        for actual_budget in range(1, max_budget + 1):
            # calcul pour chaque budget de 1 en 1 entre 1 et le budget max
            if stocks[stock_index-1]['cost'] <= actual_budget:
                # calcul avec cout de l'objet en cours --> on prend la valeur de la ligne précédente pour un budget = Buget actuel - cout de l'action actuelle
                actual_result = dp[stock_index-1][actual_budget-stocks[stock_index-1]['cost']] + stocks[stock_index-1]['profit']
                previous_result = dp[stock_index-1][actual_budget]
                if actual_result > previous_result:
                    dp[stock_index][actual_budget] = actual_result
                else:
                    dp[stock_index][actual_budget] = previous_result
                dp[stock_index][actual_budget] = max(actual_result, previous_result)
            else:  # on ne peut pas prendre cette action, on garde le résultat de l'objet précédent
                dp[stock_index][actual_budget] = dp[stock_index-1][actual_budget]

    best_combination = []

    budget = max_budget
    for i in range(len(stocks), 0, -1):
        if dp[i][budget] != dp[i-1][budget]:
            best_combination.append(stocks[i-1])
            budget -= stocks[i-1]['cost']


    best_combination.reverse()
    total_profit = dp[len(stocks)][max_budget]
    total_cost = sum([stock['cost'] for stock in best_combination])
    return best_combination, total_profit, total_cost


def main():
    # get argument from command line
    parser = argparse.ArgumentParser(description='Optimized stocks')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('--max_budget', type=float, default=500, help='Maximum budget')
    args = parser.parse_args()
    verbose = args.verbose
    max_budget = args.max_budget

    setup_logging(verbose=verbose)

    filename = "../data/Liste+d'actions+-+P7+Python+-+Feuille+1.csv"

    stocks = read_csv_file(filename)

    best_combination, best_profit, best_cost = find_best_combination_dp(stocks, max_budget)

    print("RESULTS : ")
    print(f"Profit after 2 years : {best_profit:.2f}")
    print(f"Cost: {best_cost}€")

    for stock in best_combination:
        print(f"{stock['name']} - {stock['cost']}€")

if __name__ == "__main__":
    main()
