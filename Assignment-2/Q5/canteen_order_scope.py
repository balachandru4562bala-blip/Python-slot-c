"""
ASSIGNMENT 2 - Q5: Functions, Parameters and Scope
College Canteen Order System

Includes:
- Complete the Code: TODO 1 add_item(item, order=None)
- Bug demonstration: mutable default argument in add_item_buggy
- add_item_buggy.__defaults__ inspection
- Positional, keyword, and default parameters
- Multiple return values (subtotal, GST, grand total)
- Local, Global, and Nonlocal scope demonstrations
- Sequence test with 3 independent customers
- Alternative concept: Caller-managed explicit list vs Closure accumulator
"""

# Complete the Code section
def add_item_buggy(item, order=[]):
    order.append(item)
    return order

def add_item(item, order=None):
    # TODO 1: Create a new empty list when order is None, append the item and return
    # the list
    if order is None:
        order = []
    order.append(item)
    return order

# Canteen billing with multiple parameter types and multiple return values
CANTEEN_MENU = {
    "Tea": 10.0,
    "Coffee": 15.0,
    "Vada": 12.0,
    "Samosa": 15.0,
    "Idli": 25.0
}

DAILY_CANTEEN_SALES = 0.0  # Global variable

def calculate_canteen_bill(items_list, tax_rate=0.05, discount=0.0):
    """
    Demonstrates:
    - Positional parameter: items_list
    - Default/Keyword parameters: tax_rate=0.05, discount=0.0
    - Multiple return values: (subtotal, tax, net_total)
    """
    subtotal = sum(CANTEEN_MENU.get(item, 0.0) for item in items_list)
    discounted = subtotal - (subtotal * discount)
    tax = round(discounted * tax_rate, 2)
    net_total = round(discounted + tax, 2)
    return subtotal, tax, net_total

# Demonstrating global keyword and side effects
def record_daily_sale(amount):
    global DAILY_CANTEEN_SALES
    DAILY_CANTEEN_SALES += amount
    return DAILY_CANTEEN_SALES

# Demonstrating nonlocal keyword with closure
def make_order_accumulator():
    """Alternative concept: Closure capturing state in enclosing scope."""
    customer_order = []
    def add(item):
        nonlocal customer_order
        customer_order.append(item)
        return list(customer_order)
    return add

def run_q5():
    print("=" * 70)
    print("ASSIGNMENT 2 - Q5: CANTEEN ORDERING, DEFAULT PARAMS & SCOPE")
    print("=" * 70)

    # 1. Assignment Required Complete the Code Execution
    print("\n--- Complete the Code Expected Execution ---")
    print(add_item_buggy("Tea"), add_item_buggy("Vada"))
    print(add_item("Tea"), add_item("Vada"))

    print("\n--- add_item_buggy.__defaults__ Inspection ---")
    print(f"add_item_buggy.__defaults__ = {add_item_buggy.__defaults__}")
    print("Explanation: Default argument expressions are evaluated once when def executes.")
    print("The single list object in __defaults__ is mutated across every invocation!")

    # 2. Testing 3 Independent Customers in Sequence
    print("\n--- Three Customers in Sequence (Fixed Design) ---")
    cust1_order = add_item("Tea")
    cust1_order = add_item("Vada", cust1_order)

    cust2_order = add_item("Coffee")
    cust2_order = add_item("Samosa", cust2_order)

    cust3_order = add_item("Idli")

    print(f"Customer 1 Order: {cust1_order}")
    print(f"Customer 2 Order: {cust2_order}")
    print(f"Customer 3 Order: {cust3_order}")

    assert cust1_order == ["Tea", "Vada"]
    assert cust2_order == ["Coffee", "Samosa"]
    assert cust3_order == ["Idli"]
    print("[PASS] Each customer order is completely independent!")

    # 3. Multiple Parameters & Returning Multiple Values
    print("\n--- Multiple Parameters & Bill Calculation ---")
    sub1, tax1, net1 = calculate_canteen_bill(cust1_order, tax_rate=0.05, discount=0.10)
    print(f"Customer 1 (10% student discount): Subtotal=Rs {sub1:.2f}, GST=Rs {tax1:.2f}, Net=Rs {net1:.2f}")

    # 4. Scope Demonstrations (Local, Global, Nonlocal)
    print("\n--- Scope Demonstrations ---")
    # Global
    record_daily_sale(net1)
    print(f"Updated global DAILY_CANTEEN_SALES = Rs {DAILY_CANTEEN_SALES:.2f}")

    # Nonlocal closure
    cust4_acc = make_order_accumulator()
    print("Customer 4 item 1:", cust4_acc("Tea"))
    print("Customer 4 item 2:", cust4_acc("Vada"))

if __name__ == "__main__":
    run_q5()
