class User:
    def _init_(self, username, password):
        self.username = username
        self.password = password

class FoodItem:
    def _init_(self, item_id, name, price):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.ratings = []
        self.reviews = []

    def leave_review(self, user):
        rating = int(input("Enter your rating (1-5): "))
        review = input("Leave a review: ")
        self.ratings.append(rating)
        self.reviews.append((user.username, review))
        print("Thank you for your feedback!")

class Payment:
    def _init_(self, user, total_amount):
        self.user = user
        self.total_amount = total_amount
        self.payment_status = "Pending"
        self.credit_card_number = None

    def process_payment(self):
        self.credit_card_number = input("Enter your credit card number: ")
        # In a real-world scenario, you would use a secure payment gateway to process the payment
        # Here, we'll just assume the payment is successful for demonstration purposes
        print("Payment successful!")
        self.payment_status = "Completed"


class Order:
    def _init_(self, user, item, quantity):
        self.user = user
        self.item = item
        self.quantity = quantity
        self.status = "Processing"
        self.payment = None

    def make_payment(self):
        total_amount = self.item.price * self.quantity
        total_amount = apply_discount(total_amount)
        delivery_cost = choose_delivery_option()
        total_amount += delivery_cost

        payment = Payment(self.user, total_amount)
        payment.process_payment()
        self.payment = payment

        print("Order placed successfully!")
        self.status = "Completed"


def apply_discount(total_amount):
    discount_code = input("Enter discount code (if any): ")
    discount_amount = 80
    discounted_total = max(0, total_amount - discount_amount)
    print(f"Discount applied: ${discount_amount:.2f}")
    return discounted_total

def choose_delivery_option():
    delivery_option = input("Choose delivery option (1. Standard, 2. Express): ")
    delivery_cost = 0

    if delivery_option == '1':
        delivery_cost = 39  # Standard delivery cost
    elif delivery_option == '2':
        delivery_cost = 69  # Express delivery cost
    else:
        print("Invalid delivery option. Using standard delivery.")

    return delivery_cost

# Dummy data for users, menu, and orders
users = [User("user1", "password1"), User("user2", "password2")]
menu = [
    FoodItem(1, 'Pizza', 399),
    FoodItem(2, 'Burger', 199),
    FoodItem(3, 'Pasta', 89),
    FoodItem(4, 'Salad', 49),
    FoodItem(5, 'Chicken Wings', 399),
    FoodItem(6, 'Sushi Roll', 1099),
    FoodItem(7, 'Steak', 1999),
]
orders = []

def authenticate_user():
    max_attempts = 3
    for attempt in range(max_attempts):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = next((u for u in users if u.username == username and u.password == password), None)

        if user:
            return user
        else:
            print(f"Invalid username or password. {max_attempts - attempt - 1} attempts remaining.")
    print("Maximum login attempts reached. Returning to the main menu.")
    return None

def display_menu():
    print("Menu:")
    for item in menu:
        print(f"{item.item_id}. {item.name} - Rs.{item.price}")

def place_order(user):
    display_menu()
    item_id = int(input("Enter the item ID you want to order: "))
    quantity = int(input("Enter the quantity: "))
    
    item = next((item for item in menu if item.item_id == item_id), None)
    
    if item:
        order = Order(user, item, quantity)
        orders.append(order)
        print(f"{quantity} {item.name}(s) added to your order.")
    else:
        print("Invalid item ID. Please try again.")

def display_order(user):
    user_orders = [order for order in orders if order.user == user]

    if not user_orders:
        print("You have no orders.")
        return

    total_amount = sum(order.item.price * order.quantity for order in user_orders)
    total_amount = apply_discount(total_amount)
    delivery_cost = choose_delivery_option()
    total_amount += delivery_cost

    print("Your Order:")
    for order in user_orders:
        print(f"{order.quantity} {order.item.name}(s) - Rs.{order.item.price * order.quantity:.2f}")

    print(f"Delivery Cost: Rs.{delivery_cost:.2f}")
    print(f"Total Amount: Rs.{total_amount:.2f}")

    payment_choice = input("Would you like to proceed with payment? (y/n): ")
    if payment_choice.lower() == 'y':
        for order in user_orders:
            order.make_payment()
    else:
        print("Order not completed. You can make a payment later.")

def display_order_history(user):
    user_orders = [order for order in orders if order.user == user]

    if not user_orders:
        print("You have no order history.")
        return
    
    print("Order History:")
    for order in user_orders:
        print(f"{order.quantity} {order.item.name}(s) - Rs.{order.item.price * order.quantity:.2f}")

def track_order(user):
    user_orders = [order for order in orders if order.user == user]
    if user_orders:
        for order in user_orders:
            print(f"Order ID: {id(order)}, Status: {order.status}")
    else:
        print("You have no orders.")

def main():
    print("Welcome to the Online Food Ordering System!")

    while True:
        print("\n1. Log In\n2. Register\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            user = authenticate_user()
            if user:
                print(f"Welcome, {user.username}!")
                while True:
                    print("\n1. Display Menu\n2. Place Order\n3. Display Current Order\n4. Order History\n5. Track Order\n6. Leave Review\n7. Make Payment\n8. Log Out")
                    user_choice = input("Enter your choice: ")

                    if user_choice == '1':
                        display_menu()
                    elif user_choice == '2':
                        place_order(user)
                    elif user_choice == '3':
                        display_order(user)
                    elif user_choice == '4':
                        display_order_history(user)
                    elif user_choice == '5':
                        track_order(user)
                    elif user_choice == '6':
                        item_id = int(input("Enter the item ID for which you want to leave a review: "))
                        item_to_review = next((item for item in menu if item.item_id == item_id), None)
                        if item_to_review:
                            item_to_review.leave_review(user)
                        else:
                            print("Invalid item ID. Please try again.")
                    elif user_choice == '7':
                        display_order(user)
                    elif user_choice == '8':
                        print(f"Goodbye, {user.username}!")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid username or password. Please try again.")

        elif choice == '2':
            username = input("Enter a new username: ")
            password = input("Enter a new password: ")
            new_user = User(username, password)
            users.append(new_user)
            print("Registration successful! Please log in.")

        elif choice == '3':
            print("Thank you for using the Online Food Ordering System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "_main_":
    main()