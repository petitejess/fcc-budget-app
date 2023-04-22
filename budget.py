from functools import reduce


class Category:

  def __init__(self, category):
    self.category = category
    self.ledger = []
    self.total_available_funds = 0

  def deposit(self, amount, description=""):
    self.ledger.append({"amount": abs(amount), "description": description})
    self.total_available_funds += abs(amount)

  def check_funds(self, amount):
    return True if (self.total_available_funds >= abs(amount)) else False

  def withdraw(self, amount, description=""):
    self.ledger.append({"amount": -abs(amount), "description": description})

    if (self.check_funds(amount)):
      self.total_available_funds -= abs(amount)
      return True
    else:
      return False

  def get_balance(self):
    print(self.category, self.total_available_funds)
    return self.total_available_funds

  def transfer(self, amount, destination_category):
    if (self.check_funds(amount)):
      # Withdraw from origin category
      self.withdraw(amount, f"Transfer to {destination_category.category}")

      # Deposit to destination category
      destination_category.deposit(amount, f"Transfer from {self.category}")
      return True
    else:
      return False

  def __str__(self):
    max_line_width = 30
    left_stars_width = int((max_line_width - len(self.category)) / 2)
    right_stars_width = max_line_width - left_stars_width - len(self.category)

    body_lines = []
    for record in self.ledger:
      content_description = record["description"][:23]
      content_amount = "%.2f" % record["amount"]
      remaining_space_width = max_line_width - len(content_description) - len(
        content_amount)
      body_lines.append(
        f"{content_description}{' ' * remaining_space_width}{content_amount}")

    title = f"{'*' * left_stars_width}{self.category}{'*' * right_stars_width}"
    body = "\n".join(body_lines)
    footer = f"Total: {'%.2f' % self.total_available_funds}"

    return title + "\n" + body + "\n" + footer


def create_spend_chart(categories):
  title = "Percentage spent by category"
  divider = " " * 4 + "-" * 3 * len(categories) + "-"
  y_axis = []
  x_axis = []
  percentages = {}

  for n in range(11):
    y_axis.append(n * 10)

  def agg_spending(prev_transaction, curr_transaction):
    return abs(prev_transaction["amount"]) + abs(curr_transaction["amount"])

  total_spend = 0
  total_category_spend = {}

  for category in categories:
    x_axis.append(category.category)

    spendings = list(
      filter(lambda transaction: transaction["amount"] < 0, category.ledger))
    aggregated_spend = reduce(lambda x, y: x + abs(y["amount"]), spendings, 0)

    total_category_spend[category.category] = aggregated_spend
    total_spend += aggregated_spend

  for category in categories:
    percent = total_category_spend[category.category] / total_spend * 100
    percentages[category.category] = int((percent - (percent % 10)))

  chart = []
  max_category_name_len = 0
  for i in y_axis:
    label = " " * (3 - len(str(i))) + str(i) + "|"
    points = []

    for category, percent in percentages.items():
      if (percent >= i):
        points.append("o")
      else:
        points.append(" ")

      if len(category) > max_category_name_len:
        max_category_name_len = len(category)
    chart.append(label + " " + "  ".join(points) +
                 ((len(divider) - len(label) - 8) * " "))
  chart.reverse()

  category_labels = []

  col = []
  for i in range(max_category_name_len):
    row = []

    for (cat_idx, category) in enumerate(categories):
      letter = ""
      if (len(category.category) > i):
        letter = category.category[i]
      elif cat_idx == (len(categories) - 1):
        letter = ""
      else:
        letter = " "

      row.append((" " * 5 if cat_idx == 0 else " ") + letter)

    col.append(row)

  category_labels = map(lambda row: " ".join(row), col)

  return title + "\n" + "\n".join(chart) + "\n" + divider + "\n" + "  \n".join(
    category_labels) + "  "


food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(200, "splurge!")

clothing = Category("Clothing")

food.transfer(-500, clothing)

clothing.withdraw(100, "buy buy buy!!")

auto = Category("Auto")

auto.deposit(2750, "mobil apah")
auto.withdraw(2500, "what?")

print(create_spend_chart([food, clothing, auto]))