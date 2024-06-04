# Hareen Dilruksha Nanayakkara
# 4034502
# HD Level

from datetime import datetime


class Customer:
    def __init__(self, customerID, customerName, reward):
        self.customerID = customerID
        self.customerName = customerName
        self.reward = reward

        def get_reward():
            pass

        def get_discount():
            pass

        def update_reward():
            pass

        def display_info():
            pass


class BasicCustomer(Customer):
    default_reward_rate = 1.0

    def __init__(self, customerID, customerName, reward, reward_rate):
        super().__init__(customerID, customerName, reward)
        if reward_rate is None:
            self.reward_rate = BasicCustomer.default_reward_rate
        else:
            self.reward_rate = reward_rate

    def get_reward(self, total_cost):
        self.reward = round(total_cost * float(self.reward_rate))
        return self.reward

    def update_reward(self, value):
        self.reward = (self.reward + value)

    def display_reward(self):
        print("Reward Points: ", self.reward)

    def set_reward_rate(self, new_reward_rate):
        self.reward_rate = new_reward_rate


class VIPCustomer(BasicCustomer):
    default_discount_rate = 0.08

    def __init__(self, customerID, customerName, reward, reward_rate, discount_rate):
        super().__init__(customerID, customerName, reward, reward_rate)
        if reward_rate is None:
            self.reward_rate = self.default_reward_rate
        else:
            self.reward_rate = reward_rate

        if discount_rate is None:
            self.discount_rate = VIPCustomer.default_discount_rate
        else:
            self.discount_rate = discount_rate

    def get_discount(self, total_cost):
        discount = total_cost * float(self.discount_rate)
        return round(float(discount))

    def get_reward(self, total_cost):
        reward = total_cost - (total_cost * float(self.discount_rate)) * float(self.reward_rate)
        return round(float(reward))

    def display_info(self):
        pass

    def set_discount_rate(self, new_discount_rate):
        self.discount_rate = new_discount_rate


class Product:
    def __init__(self, productID, product_name, product_price):
        self.productID = productID
        self.product_name = product_name
        self.product_price = product_price

    def display_info(self):
        print("product id: ", self.productID)
        print("product name: ", self.product_name)
        print("product price: ", self.product_price)
        print("prescription requirement: ")


class Order:
    def __init__(self, customer, product, quantity):
        self.customer = customer
        self.product = product
        self.quantity = quantity

    def compute_cost(self):
        return


class Records:
    def __init__(self):
        self.customers = {}
        self.products = {}
        self.orders = {}

    def get_customer_list(self):
        return self.customers

    def get_products_list(self):
        return self.products

    # reads orders data file and store it in a dictionary
    def read_orders(self, file_name):
        try:
            with open(file_name, 'r') as file:
                rows = file.readlines()
        except FileNotFoundError:
            return 404

        if rows is None:
            return 404
        else:
            for row in rows:
                column = row.strip().split(", ")
                rowLength = len(column)
                identifier = column[0]
                orderItems = {}
                orderArray = []
                quantity = []

                for i in range(1, rowLength - 3):
                    if "P" in column[i] or "B" in column[i] or column[i].isalpha():
                        orderArray.append(column[i])
                    elif column[i].isdigit():
                        quantity.append(column[i])

                total = column[rowLength - 3]
                rewards = column[rowLength - 2]
                dateTime = column[rowLength - 1]

                for i in range(len(orderArray)):
                    orderItems[orderArray[i]] = quantity[i]

                self.orders[identifier] = {"items": orderItems, "total": total,
                                           "rewards": rewards, "dateTime": str(dateTime)}

            return self.orders

    # reads customers data file and store it in a dictionary
    def read_customers(self, file_name):
        try:
            with open(file_name, 'r') as file:
                rows = file.readlines()
        except FileNotFoundError:
            return 404

        if rows is None:
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

    # reads products data file and store it in a dictionary
    def read_products(self, file_name):
        try:
            with open(file_name, 'r') as file:
                rows = file.readlines()
        except FileNotFoundError:
            return 404

        if rows is None:
            return 404
        else:
            for row in rows:
                column = row.strip().split(", ")
                productID = column[0]
                productName = column[1]
                productPrice = column[2]
                prescription = column[3]

                if "B" in productID:
                    bundleItems = []
                    rowLengthForIndex = len(column)
                    for i in range(2, rowLengthForIndex):
                        bundleItems.append(column[i])

                    self.products[productID] = {"name": productName, "bundle items": bundleItems}
                else:
                    self.products[productID] = {"name": productName, "price": productPrice,
                                                "prescription": prescription}

            return self.products

    # takes a value which can be an ID or a name which helps to search and retrieve data and return the customer object
    def find_customer(self, value):
        if "V" in value or "B" in value:
            customer = self.customers.get(value)
            if "V" in customer["customerID"]:
                NewCustomer = VIPCustomer(customer["customerID"], customer["name"], customer["rewards"],
                                          customer["reward rate"], customer["discount rate"])
            else:
                NewCustomer = BasicCustomer(customer["customerID"], customer["name"], customer["rewards"],
                                            customer["reward rate"])

            return NewCustomer
        else:
            for customer_ID, info in self.customers.items():
                if info["name"] == value:
                    customerID = customer_ID
                    name = value
                    rewardRate = info["reward rate"]
                    rewards = info["rewards"]

                    if "V" in customerID:
                        discountRate = info["discount rate"]
                        NewCustomer = VIPCustomer(customerID, name, rewards, rewardRate, discountRate)
                    else:
                        NewCustomer = BasicCustomer(customerID, name, rewards, rewardRate)

                    return NewCustomer

    # takes a value which can be an ID or a name which helps to search and retrieve data and return product data
    def find_product(self, value):
        if len(value) >= 3:
            for product_ID, info in self.products.items():
                if info["name"] == value:
                    print(f'{value.ljust(20)} {str(info["price"]).rjust(10)}')
        else:
            product = self.products.get(value)
            print(f'{product["name"].ljust(20)} {str(product["price"]).rjust(10)}')

    # list of customers which read from the file
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

    # list of products which read from the file
    def list_products(self):
        print('\n################################')
        print('\t\t\tProducts')
        print('################################')

        for product_ID, details in self.products.items():
            if "B" in product_ID:
                name = details["name"]
                items = ", ".join(details["bundle items"])
                print(f'{name.ljust(20)} Bundle items: {items}')
            else:
                name = details["name"]
                price = details["price"]
                print(f'{name.ljust(20)} {str(price).rjust(10)}')

        print('\n')


customersDict = {}
productDict = {}
ordersDict = {}


# this is the place order function which takes product name/ID, username/ID and quantity as inputs, store them and
# pass to another function
def display(record):
    global tempID, customer
    name = 'null'
    prescriptionList = []
    bundleListInOrder = []
    bundleList = []
    VIPList = []
    BasicList = []
    maxKey = 0
    maxIdNumber = 0

    for key in customersDict.keys():
        if key.startswith('B') and key[1:].isdigit():
            number = int(key[1:])
            if number > maxIdNumber:
                maxIdNumber = number
                maxKey = key

    for productID, details in productDict.items():
        if "B" in productID:
            bundleList.append(details["name"])

    print(bundleList)

    for customerID, details in customersDict.items():
        if "V" in customerID:
            VIPList.append(details["name"])
        else:
            BasicList.append(details["name"])

    # saving the products that need a prescription in a list
    for productID in productDict:
        if "P" in productID:
            dataDict = productDict[productID]
            presRequirement = dataDict["prescription"]

            if presRequirement == 'y':
                prescriptionList.append(dataDict["name"])
        else:
            continue

    # username validation
    tempName = input('\nEnter the name of the customer or the ID of the customer [e.g. Huong/V3]:')
    if "V" in tempName or "B" in tempName:
        detailsDicTemp = customersDict.get(tempName)
        if detailsDicTemp is None:
            print("\nUser not found ..")
            return
        else:
            name = detailsDicTemp.get("name")
    else:
        while 1:
            if tempName.isalpha():
                name = tempName
                break
            else:
                print('Please enter a valid name.')
                tempName = input('Enter the name of the customer [e.g. Huong]:')
                continue

    # creating customer objects depending on their status VIP/Basic
    if name in VIPList:
        VCustomer = record.find_customer(name)
        customer = VCustomer
    elif name in BasicList:
        BasCustomer = record.find_customer(name)
        customer = BasCustomer
    else:  # if user not found creating a new user
        print("\ncreating new user ..\n")
        customersDict[f"B{maxIdNumber}"] = {"name": name, "reward rate": 1, "discount rate": 0, "rewards": 0}
        customer = BasicCustomer(f"B{maxIdNumber}", name, 0, 1)

    while True:
        tempProducts = input('Enter the product [enter a valid product only, e.g. vitaminC, coldTablet]: ')
        tempProductList = [product.strip() for product in tempProducts.split(",")]

        Valid = True
        productNameList = []
        productIDList = []
        productNameOnlyList = []

        for productID, details in productDict.items():
            productIDList.append(productID)
            productNameList.append(details["name"])

        # product name/ID validation
        for tempProduct in tempProductList:
            if "B" in tempProduct or "P" in tempProduct:
                if tempProduct not in productIDList:
                    print(f'The product {tempProduct} is not valid. Please enter a valid product list.')
                    Valid = False
                    break
            else:
                if tempProduct not in productNameList:
                    print(f'The product {tempProduct} is not valid. Please enter a valid product list.')
                    Valid = False
                    break

        if Valid:
            for tempProduct in tempProductList:
                if "B" in tempProduct or "P" in tempProduct:
                    productNameOnlyList.append(productDict[tempProduct]["name"])
                else:
                    productNameOnlyList.append(tempProduct)

            productList = productNameOnlyList
            break

    while True:
        quantities = input('Enter the quantities [enter positive integers only, e.g. 1, 2, 3, 4]:')
        tempQuantityList = [quantity.strip() for quantity in quantities.split(",")]

        Valid = True

        # quantity validation
        for tempQuantity in tempQuantityList:
            quantity = int(tempQuantity)
            if quantity < 0 or quantity == 0:
                print('Enter a valid quantity [quantities cannot be negative or 0]')
                Valid = False
                break
        if Valid:
            quantityList = tempQuantityList
            break

    for pName in productList:
        for bundleItem in bundleList:
            if pName == bundleItem:
                bundleListInOrder.append(pName)

    # prescription requirement
    for product in productList[:]:
        if product in prescriptionList:
            while True:
                tempAnswer = input(f"The product {product} requires a doctor's prescription, do you have one? (y/n): ")
                if tempAnswer.lower() == 'n':
                    # Remove the product and its quantity
                    index = productList.index(product)
                    quantityList.pop(index)
                    productList.remove(product)
                    break
                elif tempAnswer.lower() == 'y':
                    break  # Break the while loop if the user has a prescription
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
                    break

    inputFunc(productList, name, quantityList, customer)


# takes customer name/ID as input and displays their order history
def searchCustomerOrder():
    identifierInput = ""

    identifierInput = input('Enter the name of the customer or the ID of the customer [e.g. Huong/V3]: ')

    if identifierInput not in ordersDict:
        print(f"No order history found for {identifierInput}.")
        return

    print(f'This is the ordr history of {identifierInput}\n')
    print("{:<10} {:<30} {:<15} {:<15}".format("Order", "Products", "Total Cost", "Earned Rewards"))

    customer_orders = ordersDict[identifierInput]
    items = customer_orders['items']
    total_cost = customer_orders['total']
    earned_rewards = customer_orders['rewards']
    product_list = ', '.join([f"{quantity} x {product}" for product, quantity in items.items()])

    print("{:<10} {:<30} {:<15} {:<15}".format("Order 1", product_list, total_cost, earned_rewards))


# takes customer name/ID, new discount rate as inputs and updates them
def adjustDiscountRateVip():
    name = ""
    DiscountRate = 0.0

    tempName = input('\nEnter the name of the customer or the ID of the customer [e.g. Huong/V3]:')
    if "V" in tempName or "B" in tempName:
        detailsDicTemp = customersDict[tempName]
        name = detailsDicTemp.get("name")
    else:
        while 1:
            if tempName.isalpha():
                name = tempName
                break
            else:
                print('Please enter a valid name or a ID.')
                tempName = input('Enter the name of the customer [e.g. Huong]:')
                continue

    # discount rate validation
    def validateRate():
        while True:
            try:
                tempDiscountRate = input('Enter the new discount rate for VIP customer [1 = 100%]: ')
                discountRate = float(tempDiscountRate)

                if discountRate <= 0:
                    raise ValueError("Discount rate must be a positive number greater than 0.")

                return discountRate

            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    DiscountRate = validateRate()

    for customerID, details in customersDict.items():
        if details["name"] == name:
            details["discount rate"] = DiscountRate


# this displays all the order history of customers
def displayOrders():
    print('########################################################################################')
    print('\t\t\t\t\t\t\t\t\tCustomers')
    print('########################################################################################')

    print("{:<15} {:<20} {:<15} {:<15} {:<10}".format("Customer ID", "Items", "Total", "Rewards", "DateTime\n"))

    for identifier, info in ordersDict.items():
        items = ', '.join([f"{k}: {v}" for k, v in info.get("items", {}).items()])
        total = info["total"]
        rewards = info["rewards"]
        dateTime = info["dateTime"]

        print("{:<15} {:<20} {:<15} {:<15} {:<10}".format(str(identifier), items, total, rewards, dateTime))

    print('\n########################################################################################')


# selection menu for the functions
def menu():
    record = Records()

    # custom file names if available if not available uses default file names
    cusFile = input("Enter the customers file name: ")
    if not cusFile.strip():
        cusFile = "customers.txt"
    prodFile = input("Enter the products file name: ")
    if not prodFile.strip():
        prodFile = "products.txt"
    ordFile = input("Enter the orders file name: ")
    if not ordFile.strip():
        ordFile = "orders.txt"

    # if any file reading error occur
    if (record.read_customers(cusFile)) == 404 or (record.read_products(prodFile)) == 404 or (
            record.read_orders(ordFile)) == 404:
        print("\nFiles not found !!")
    else:
        print("\nDefault values read...\n")
        global productDict
        global customersDict
        global ordersDict
        productDict = record.read_products("products.txt")
        customersDict = record.read_customers("customers.txt")
        ordersDict = record.read_orders("orders.txt")

        while True:
            # features
            print('\nWelcome to the R.M.I.T pharmacy!\n')
            print('###################################################################')
            print('You can choose from the following options:')
            print('1. Make a purchase')
            print('2. Add/update information of products')
            print('3. Display existing customers')
            print('4. Display existing products')
            print('5. Adjust the discount rate of a VIP customer')
            print('6. Display all orders')
            print('7. Search customer orders')
            print('0. Exit the program')
            print('###################################################################')
            option = input('Choose one option: ')

            if option.strip() == "":
                print('\nInvalid selection.')
                return

            option = int(option)

            if option == 0:
                # these will save all the new data to relevant file when exiting the program
                save_products_to_file(prodFile)
                save_customers_to_file(cusFile)
                save_orders_to_file(ordFile)
                break  # Exit the loop and the program
            elif option == 1:
                display(record)
            elif option == 2:
                manageProducts()
            elif option == 3:
                record.list_customers()
            elif option == 4:
                record.list_products()
            elif option == 5:
                adjustDiscountRateVip()
            elif option == 6:
                displayOrders()
            elif option == 7:
                searchCustomerOrder()
            else:
                print('\nInvalid selection.')


# save new updates and new products added to the file
def save_products_to_file(file_name):
    with open(file_name, 'w') as file:
        for product_id, details in productDict.items():
            if "price" in details:
                name = details['name']
                price = details['price']
                prescription = details['prescription']
                line = f"{product_id}, {name}, {price}, {prescription}\n"
            else:
                name = details['name']
                bundle_items = ", ".join(details['bundle items'])
                line = f"{product_id}, {name}, {bundle_items}\n"
            file.write(line)


# save new order added to the file
def save_orders_to_file(file_name):
    with open(file_name, 'w') as file:
        for customer, details in ordersDict.items():
            items_str = ', '.join([f"{item}, {quantity}" for item, quantity in details['items'].items()])
            total = details['total']
            rewards = details['rewards']
            date_time = details['dateTime']
            line = f"{customer}, {items_str}, {total}, {rewards}, {date_time}\n"
            file.write(line)


# save new updates and new customers added to the file
def save_customers_to_file(file_name):
    with open(file_name, 'w') as file:
        for customer_id, details in customersDict.items():
            name = details['name']
            reward_rate = details['reward rate']
            discount_rate = details['discount rate']
            rewards = details['rewards']
            if discount_rate == 0:
                line = f"{customer_id}, {name}, {reward_rate}, {rewards}\n"
            else:
                line = f"{customer_id}, {name}, {reward_rate}, {discount_rate}, {rewards}\n"
            file.write(line)


# update or add new products
def manageProducts():
    global productTemp, priceTemp, prescriptionTemp
    # print(productDict)
    maxIdNumber = 0

    for key in productDict.keys():
        if key.startswith('P') and key[1:].isdigit():
            number = int(key[1:])
            if number > maxIdNumber:
                maxIdNumber = number

    # price validation (has to be float convertible)
    def validate_price(priceValidate):
        try:
            return float(priceValidate)
        except ValueError:
            raise ValueError(f"Invalid price: {priceValidate}")

    # prescription validation (has to be only 'y' or 'n')
    def validate_prescription(prescriptionValidate):
        if prescriptionValidate.lower() in ['y', 'n']:
            return prescriptionValidate.lower()
        else:
            raise ValueError(f"Invalid prescription flag: {prescriptionValidate}")

    while True:
        productsInput = input(
            "Enter the products, prices, and the doctor's prescription requirements [e.g., toothpaste 5.2 n, "
            "shampoo 8.2 n]: ")
        productsDataList = [item.strip() for item in productsInput.split(',')]

        try:
            for productData in productsDataList:
                productTemp, priceTemp, prescriptionTemp = [item.strip() for item in productData.split(' ')]

                product = str(productTemp)
                price = validate_price(priceTemp)
                prescription = validate_prescription(prescriptionTemp)

                productUpdated = False
                for productID, details in productDict.items():
                    if details["name"] == product:
                        productDict[productID] = {"name": product, "price": price, "prescription": prescription}
                        productUpdated = True
                        break

                if not productUpdated:
                    maxIdNumber += 1
                    productDict[f"P{maxIdNumber}"] = {"name": product, "price": price, "prescription": prescription}

            # Break the loop if input is successfully processed
            break
        except ValueError as e:
            print(e)

    # print(productDict)


# total calculation for normal products
def calcTotal(product, quantity):
    for productID, details in productDict.items():
        if details["name"] == product:
            price = float(details["price"])
            total = price * quantity
            return round(total, 2)


# total calculation for bundle products
def bundleTotalCalc(bundle):
    total = 0
    subTotal = 0

    for name, data in bundle.items():
        products = data["items"]

        for product in products:
            for productID, details in productDict.items():
                if "P" in productID:
                    if product == productID:
                        total += float(details["price"])
                    else:
                        continue

        subTotal = total * data["quantity"]

    return float(subTotal - ((subTotal / 100) * 80))


# this function takes data from the display function to generate the invoice
def inputFunc(productList, name, quantityList, customer):
    current_datetime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    normTotal = 0
    productStoreNewDict = {}
    bundleListTemp = {}
    normalProductList = {}
    bundleList = {}

    # combining quantityList and productList arrays all together
    product_quantity_dict = {productList[i]: quantityList[i] for i in range(len(productList))}

    # list of bundle products
    for productID, details in productDict.items():
        for productName in productList:
            if details["name"] == productName and "B" in productID:
                bundleListTemp[details["name"]] = {"items": details["bundle items"]}

    bundleList = bundleListTemp

    print('----------------------------------')
    print('\t\t\tReceipt')
    print('----------------------------------')
    print(f'Name:\t\t\t\t{name}\n')

    for i in range(len(productList)):
        product = str(productList[i])
        quantity = int(quantityList[i])

        if not bundleListTemp:
            normalProductList[product] = {"quantity": quantity}
        else:
            for name, items in bundleListTemp.items():
                if product == name:
                    bundleList[product]["quantity"] = quantity
                else:
                    normalProductList[product] = {"quantity": quantity}

        print(f'Product:\t\t\t{product}')
        print(f'Quantity:\t\t\t{quantity}')
        print("----------------------------------")

    # total for normal products
    for normProductName, details in normalProductList.items():
        normTotal += calcTotal(normProductName, details["quantity"])

    # total for bundle products
    bundleTotal = bundleTotalCalc(bundleList)

    # final subtotal
    subTotalFloat = float(normTotal + bundleTotal)

    # displaying the invoice depending on the user type
    if isinstance(customer, VIPCustomer):
        vipCustomerDiscount = customer.get_discount(subTotalFloat)
        vipCustomerRewards = customer.get_reward(subTotalFloat)
        print('----------------------------------')
        print(f'Original cost:\t\t\t{subTotalFloat} (AUD)')
        print(f'Discount:\t\t\t\t{vipCustomerDiscount}')
        print(f'Total cost:\t\t\t\t{subTotalFloat - vipCustomerDiscount} (AUD)')
        print(f'Earned rewards:\t\t\t{vipCustomerRewards}')
        ordersDict[name] = {"items": product_quantity_dict, "total": subTotalFloat - vipCustomerDiscount,
                            "rewards": vipCustomerRewards, "dateTime": current_datetime}
    else:
        basicCustomerRewards = customer.get_reward(subTotalFloat)
        print('----------------------------------')
        formattedSubTotal = f"{subTotalFloat:.2f}"
        print(f'Total cost:\t\t\t{formattedSubTotal} (AUD)')
        print(f'Earned reward:\t\t{basicCustomerRewards}\n')
        ordersDict[name] = {"items": product_quantity_dict, "total": formattedSubTotal, "rewards": basicCustomerRewards,
                            "dateTime": current_datetime}


menu()
