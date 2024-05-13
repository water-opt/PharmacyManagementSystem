class Customer():
    def __init__(self, customerID, customerName, reward):
        self.customerID = customerID
        self.customerName = customerName
        self.reward = reward

        def get_reward(self):
            pass

        def get_discount(self):
            pass

        def update_reward(self):
            pass

        def display_info(self):
            pass


class BasicCustomer(Customer):
    default_reward_rate = 1.0

    def __init__(self, customerID, customerName, reward, reward_rate):
        super().__init__(customerID, customerName, reward)
        if reward_rate is None:
            self.reward_rate = BasicCustomer.default_reward_rate
        else:
            self.rewardRate = reward_rate

    def get_reward(self, total_cost):
        self.reward = round(total_cost * self.reward_rate)
        return round(total_cost * self.reward_rate)

    def update_reward(self, value):
        self.reward = (self.reward + value)

    def display_reward(self):
        print("Reward Points: ", self.reward)

    def set_reward_rate(self, new_reward_rate):
        self.reward_rate = new_reward_rate


class VIPCustomer(BasicCustomer):
    default_discount_rate = 0.08

    def __init__(self, customerID, customerName, reward, reward_rate, discount_rate):
        super().__init__(customerID, customerName, reward)
        if reward_rate is None:
            self.reward_rate = self.default_reward_rate
        else:
            self.reward_rate = reward_rate

        if discount_rate is None:
            self.discount_rate = VIPCustomer.default_discount_rate
        else:
            self.discount_rate = discount_rate

    def get_discount(self, total_cost):
        return total_cost - (total_cost * self.discount_rate)

    def get_reward(self, total_cost):
        return (total_cost - (total_cost * self.discount_rate)) * self.reward_rate

    def display_info(self):
        pass

    def set_discount_rate(self, new_discount_rate):
        self.discount_rate = new_discount_rate


class Product():
    def __init__(self, productID, product_name, product_price):
        self.productID = productID
        self.product_name = product_name
        self.product_price = product_price

    def display_info(self):
        print()


class Order():
    def __init__(self, customer, product, quantity):
        self.customer = customer
        self.product = product
        self.quantity = quantity

    def compute_cost(self):
        return


class Records():
    def __init__(self):
        self.customers = {}
        self.products = {}

    def get_customer_list(self):
        return self.customers

    def get_products_list(self):
        return self.products

    def read_customers(self, file_name):
        with open(file_name, 'r') as file:
            rows = file.readlines()

            if rows == None:
                return 404
            else:
                for row in rows:
                    column = row.strip().split(", ")
                    customerID = column[0]
                    customerName = column[1]
                    rewardRate = column[2]
                    if "V" in customerID:
                        discountRate = column[3]
                        rewards = column[4]
                    else:
                        discountRate = 0
                        rewards = column[3]

                    self.customers[customerID] = {"name": customerName, "reward rate": rewardRate,
                                                  "discount rate": discountRate, "rewards": rewards}

                return self.customers

    def read_products(self, file_name):
        with open(file_name, 'r') as file:
            rows = file.readlines()

            if rows == None:
                return 404
            else:
                for row in rows:
                    column = row.strip().split(", ")
                    productID = column[0]
                    productName = column[1]
                    productPrice = column[2]
                    prescription = column[3]

                    self.products[productID] = {"name": productName, "price": productPrice, "prescription": []}

                    if prescription == "y":
                        self.products[productID]["prescription"].append(productName)

                return self.products

    def find_customer(self, value):
        if "V" or "B" in value:
            customer = self.customers.get(value)
            print(
                "{:<15} {:<20} {:<15} {:<15} {:<10}".format(str(value), customer["name"], str(customer["reward rate"]),
                                                            str(customer["discount rate"]), str(customer["rewards"])))
        else:
            for customer_ID, info in self.customers.items():
                customerID = customer_ID
                name = info["name"]
                rewardRate = info["reward rate"]
                discountRate = info["discount rate"]
                rewards = info["rewards"]

                print("{:<15} {:<20} {:<15} {:<15} {:<10}".format(str(customerID), name, str(rewardRate),
                                                                  str(discountRate), str(rewards)))

    def find_product(self, value):
        if len(value) >= 3:
            for product_ID, info in self.products.items():
                print(f'{info["name"].ljust(20)} {str(info["price"]).rjust(10)}')
        else:
            product = self.products.get(value)
            print(f'{product["name"].ljust(20)} {str(product["price"]).rjust(10)}')

    def list_customers(self):
        print('\n#############################################################')
        print('\t\t\tCustomers')
        print('###############################################################')

        for customer_ID, info in self.customers.items():
            customerID = customer_ID
            name = info["name"]
            rewardRate = info["reward rate"]
            discountRate = info["discount rate"]
            rewards = info["rewards"]

            print("{:<15} {:<20} {:<15} {:<15} {:<10}".format(str(customerID), name, str(rewardRate), str(discountRate),
                                                              str(rewards)))

        print('\n')

    def list_products(self):
        print('\n################################')
        print('\t\t\tProducts')
        print('################################')

        for product_ID, details in self.products.items():
            name = details["name"]
            price = details["price"]
            print(f'{name.ljust(20)} {str(price).rjust(10)}')

        print('\n')


customersDict = {}
productDict = {}


#data input
def display():
    product = 'null'
    quantity = 0
    name = 'null'
    prescriptionList = []

    # saving the products that need a prescription in a list
    for productID, details in productDict.items():
        # prescriptionList = details["prescription"]
        prescriptionList.extend(details["prescription"])

    # username validation
    tempName = input('\nEnter the name of the customer [e.g. Huong]:')
    while 1:
        if tempName.isalpha():
            name = tempName
            break
        else:
            print('Please enter a valid name.')
            tempName = input('Enter the name of the customer [e.g. Huong]:')
            continue

    # check whether the name exists in the dictionary
    for customerID, details in customersDict.items():
        if name not in details["name"]:
            details["name"] = 0

    while True:
        tempProducts = input('Enter the product [enter a valid product only, e.g. vitaminC, coldTablet]: ')
        tempProductList = [product.strip() for product in tempProducts.split(",")]

        Valid = True
        productNameList = []

        for productID, details in productDict.items():
            productNameList.append(details["name"])

        for tempProduct in tempProductList:
            if tempProduct not in productNameList:
                print(f'The product {tempProduct} is not valid. Please enter a valid product list.')
                Valid = False
                break

        if Valid:
            productList = tempProductList
            break

    while True:
        quantities = input('Énter the quantities [enter positive integers only, e.g. 1, 2, 3, 4]:')
        tempQuantityList = [quantity.strip() for quantity in quantities.split(",")]

        Valid = True

        for tempQuantity in tempQuantityList:
            quantity = int(tempQuantity)
            if quantity < 0 or quantity == 0:
                print('Enter a valid quantity [quantities cannot be negative or 0]')
                Valid = False
                break
        if Valid:
            quantityList = tempQuantityList
            break

    for product in productList:
        if product in prescriptionList:
            while True:
                # answer check
                tempAnswer = input(f"The product {product} requires a doctor' prescription, do you have one? (y/n): ")
                if tempAnswer == 'n':
                    quantityList.pop(productList.index(product))
                    productList.remove(product)
                    break
                elif tempAnswer == 'y':
                    break
                else:
                    print('Invalid input. Please enter either "y" or "n".')

    # inputFunc(productList, name, quantityList)


selectionDict = {
    1: display,
    # 2:manageProducts,
    # 5:orderHistory
}


# selection menu for the functions
def menu():
    record = Records()

    if (record.read_customers("customers.txt")) == 404 or (record.read_products("products.txt")) == 404:
        print("Files not found !!")
    else:
        global productDict
        global customersDict
        productDict = record.read_products("products.txt")
        customersDict = record.read_customers("customers.txt")

        print(productDict)
        print(customersDict)

        while True:
            # features
            print('\nWelcome to the RMIT pharmacy!\n')
            print('###################################################################')
            print('You can choose from the following options:')
            print('1. Make a purchase')
            # print('2. Add/update information of products')
            print('3. Display existing customers')
            print('4. Display existing products')
            # print('5. Display a customer order history')
            print('0. Exit the program')
            print('###################################################################')
            option = input('Choose one option: ')

            option = int(option)

            if option == 0:
                break  # Exit the loop and the program
            elif option == 3:
                record.list_customers()
            elif option == 4:
                record.list_products()
            elif option in selectionDict:
                selectionDict[option]()
            else:
                print('Invalid selection.')


# # order history
# orderDict = {
#     "Tom": {
#         "orders": [
#             {
#                 "products": {"vitaminC": 1},
#                 "total": 12.0,
#                 "earnedRewards": 12
#             },
#             {
#                 "products": {"fragrance": 1, "vitaminE": 2},
#                 "total": 54.0,
#                 "earnedRewards": 54
#             },
#             {
#                 "products": {"coldTablet": 3, "vitaminC": 1},
#                 "total": 31.2,
#                 "earnedRewards": 31
#             }
#         ]
#     }
# }
#
# # initial customers
# customersDict = {
#     "Kate": 120,
#     "Tom": 32,
# }
#

#
# # product add/ update
# def manageProducts():
#     while True:
#         productsInput = input(
#             "Enter the products, prices, and the doctor's prescription requirements [e.g., toothpaste 5.2 n, shampoo 8.2 n]: ")
#         productsDataList = [item.strip() for item in productsInput.split(',')]
#
#         # prices validity
#         pricesIsValid = True
#
#         for productData in productsDataList:
#             product, price, prescription = [item.strip() for item in productData.split(' ')]
#
#             # price validation [price > 0]
#             try:
#                 price = float(price)
#                 if price <= 0:
#                     pricesIsValid = False
#                     break
#             except ValueError:
#                 pricesIsValid = False
#                 break
#
#             # prescription requirement validation ['y' or 'n']
#             if prescription.lower() not in ['y', 'n']:
#                 pricesIsValid = False
#                 break
#
#         prescriptionList = productDict["prescription"]
#
#         if pricesIsValid:
#             for productData in productsDataList:
#                 product, price, prescription = [item.strip() for item in productData.split(' ')]
#
#                 if product in productDict:
#                     productDict[product] = price
#                     if prescription.lower() == 'y':
#                         prescriptionList.append(product)
#                 else:
#                     productDict[product] = price
#                     if prescription.lower() == 'y':
#                         prescriptionList.append(product)
#
#             productDict["prescription"] = prescriptionList
#             print("\nInformation updated.\n")
#             break
#         else:
#             print(
#                 "\nInvalid input. Valid inputs. [prices should be greater than o and prescription requirement should be 'n' or 'y']")
#             continue

#
# def orderHistory():
#     # user name input
#     name = input("Enter the name of the user: ")
#     print(f'\nThis is the order history of {name}')
#
#     # checking the name given as an input
#     if name in orderDict:
#         orders = orderDict[name]["orders"]
#
#         # formatting the history
#         print('\t\t\tProducts\t\t\t\t\t\tTotal Cost\t\t\t\tEarned Rewards')
#         for i, orderDetails in enumerate(orders, start=1):
#             productsDisplay = ", ".join([f"{quantity} x {product}" for product, quantity in orderDetails["products"].items()])
#             print(f"Order {i:<5} {productsDisplay:<31} Total Cost: {orderDetails['total']:<11} Earned Rewards: {orderDetails['earnedRewards']}")
#             # print(f"Order {i} {productsDisplay}, Total Cost: {orderDetails['total']}, Earned Rewards: {orderDetails['earnedRewards']}")
#     else:
#         print(f"No order history exists for user - {name}")
#
# selection navigation


# #total calculation
# def calcTotal(product, quantity):
#     total = productDict[product] * int(quantity)
#     return total
#
# #save new rewards amount calculation
# def saveRewards(customer, total):
#     customersDict[customer] = customersDict[customer] + total
#
# #calculations callings
# def inputFunc(productList, name, quantityList):
#     subTotal = 0
#     totalRewards = 0
#     productStoreNewDict = {}
#     #display
#     print('--------------------------------')
#     print('\t\t\tReceipt')
#     print('--------------------------------')
#
#     for i in range(len(productList)):
#         product = str(productList[i])
#         quantity = int(quantityList[i])
#
#         #store products and quantity dictionary temporary for storing
#         productStoreNewDict[product] = quantity
#
#         # calling rewards and total calculation functions
#         total = calcTotal(product, quantity)
#
#         subTotal += total
#
#         #display
#         print(f'Name:\t\t\t\t{name}')
#         print(f'Product:\t\t\t{product}')
#         print(f'Unit Price:\t\t\t{productDict[product]} (AUD)')
#         print(f'Quantity:\t\t\t{quantity}')
#
#     if customersDict[name] >= 100:
#         cashToBeDeducted = float(rewardToCash(name))
#         finalAmount = subTotal - cashToBeDeducted
#     else:
#         finalAmount = subTotal
#
#     totalRewards = round(subTotal)
#     saveRewards(name, totalRewards)
#
#     print('--------------------------------')
#     print(f'Total cost:\t\t\t{finalAmount} (AUD)')
#     print(f'Earned reward:\t\t{totalRewards}\n')
#
#     order = {
#         "products": productStoreNewDict,
#         "total": float(finalAmount),
#         "earnedRewards": int(totalRewards)
#     }
#
#     if name in orderDict:
#         orderDict[name]["orders"].append(order)
#     else:
#         orderDict[name] = {"orders": [order]}
#
# # reward points to cash
# def rewardToCash(name):
#     rewards = customersDict[name]
#     if rewards >= 100:
#         rewardCash = int(rewards/100)*10
#         customersDict[name] = rewards - (round(rewards/100))*100
#     else:
#         rewardCash = rewards
#
#     return rewardCash
#
#calling display function
menu()
