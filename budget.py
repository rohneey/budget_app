class Category:
    withdrawals = 0

    def __init__(self, name):
        self.name = name
        self.ledger = list()

    def __str__(self):
        category_name = self.name.center(30, '*') + '\n'
        for item in self.ledger:
            row = f'{item["description"][:23]:23}' + f'{item["amount"]:>7.2f}' + '\n'
            category_name += row
        balance = f'Total: {self.get_balance():.2f}'
        category_name += balance
        return category_name

    def deposit(self, amount, description=''):    # method appends an object to the ledger list
        deposit = {'amount': float(amount), 'description': description}
        self.ledger.append(deposit)

    def withdraw(self, amount, description=''):    # method withdraws money from balance
        if self.check_funds(float(amount)) is True:
            withdrawal = {'amount': float(-amount), 'description': description}
            self.ledger.append(withdrawal)
            self.withdrawals += float(amount)      # add spent money to total category's spendings
            print(self.withdrawals)
            return True
        else:
            return False

    def get_balance(self):                         # method checks current balance
        total = 0
        for item in self.ledger:
            total += item['amount']
        return total

    def transfer(self, amount, budget_category):   # method transfers money to another category
        if self.check_funds(float(amount)) is True:
            withdrawal_description = f'Transfer to {budget_category.name}'
            deposit_description = f'Transfer from {self.name}'
            withdrawal = {
                'amount': float(-amount),
                'description': withdrawal_description
            }
            deposit = {
                'amount': float(amount),
                'description': deposit_description
            }

            self.withdrawals += float(amount)
            self.ledger.append(withdrawal)
            budget_category.ledger.append(deposit)
            return True
        else:
            return False

    def check_funds(self, amount):                  # method checks if there're still enough money to withdraw/transfer  
        total = 0
        for item in self.ledger:
            total += item['amount']
        if amount <= total:
            return True
        else:
            return False


def create_spend_chart(categories):
    category = Category
    spendings_by_category = dict()
    percentages_by_category = dict()
    total_withdrawals = 0

    for category in categories:
        spendings_by_category[category.name] = round(category.withdrawals, 2) # dict with withdrawals by category
        total_withdrawals += category.withdrawals
    for key, value in spendings_by_category.items():                          # dict with percentage spent in each category
        percentages_by_category[key] = round(
            ((value / total_withdrawals) * 100), 2)

    chart = f'Percentage spent by category\n'                                 # barchart title

    percents = [f'{str(i):>3}|' for i in range(100, -1, -10)]                 # y-axis with percentage labels
    for i in percents:
        chart += i
        for j in percentages_by_category.values():                            # percentage bars
            if j > float(i.rstrip('|')):
                chart += ' o '
            else:
                chart += '   '
        chart += ' \n'

    dashes = '-' * (len(categories) * 3 + 1)                                  # horizontal line below the bars
    chart += 4 * ' ' + str(dashes) + '\n'

    max_length = max(spendings_by_category.keys(), key=len)

    for i in range(len(max_length)):                                          # category names vertically written
        chart += ' ' * 4
        for name in spendings_by_category.keys():
            if i < len(name):
                chart += ' ' + name[i] + ' '
            else:
                chart += ' ' * 3
        chart += ' \n'

    chart = chart.rstrip() + '  '

    return chart