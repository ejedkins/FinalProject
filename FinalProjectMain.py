#Elijah Jedkins Student id: 1786452
import csv
import datetime


class Manufacturer:
    # class manufacturer constructor
    def __init__(self, item_id, name, item_type, condition):
        self.item_id = item_id
        self.name = name
        self.item_type = item_type
        self.condition = condition

    def __str__(self):
        # return type string for the class
        return str(self.item_id) + "," + self.name + "," + self.item_type + "," + self.condition

    def __eq__(self, other):
        # uniquify all instances
        if isinstance(other, Manufacturer):
            return other.item_id == self.item_id and other.name == self.name \
                   and other.type == self.item_type and other.condition == self.condition


class Price:
    # class price constructor
    def __init__(self, item_id, price, items):
        self.item_id = item_id
        self.price = price
        self.name = None
        self.item_type = None
        self.condition = None
        self.match_data(items)

    # create a function to match pre-loaded data
    def match_data(self, items):
        for i in items:
            if i.item_id == self.item_id:
                self.name = i.name
                self.item_type = i.item_type
                self.condition = i.condition

    def __str__(self):
        return str(self.item_id) + "," + self.name + "," + self.item_type + "," + self.condition\
               + "," + str(self.price)


class ServiceDates:
    # ServiceDates constructor
    def __init__(self, item_id, date, items):
        self.item_id = item_id
        self.date = date
        self.name = None
        self.item_type = None
        self.condition = None
        self.price = None
        self.match_data(items)

    # create a function to match the pre-loaded data
    def match_data(self, items):
        for i in items:
            if i.item_id == self.item_id:
                self.name = i.name
                self.item_type = i.item_type
                self.condition = i.condition
                self.price = i.price

    # define class objects as strings
    def __repr__(self):
        if self.condition:
            return str((self.item_id, self.name, self.item_type, self.price, self.date,
                        self.condition))
        else:
            return str((self.item_id, self.name, self.item_type, self.price, self.date))


def read_manufacturer_data_file(filename):
    # Function to read manufacturer data
    entries = []
    data = []
    file = open(filename, "r")
    for line in file.readlines():
        data.append(line.strip().split(","))
    file.close()
    for i in data:
        try:
            entries.append(Manufacturer(str(i[0]).strip(), str(i[1]).strip(),
                                        str(i[2]).strip(), str(i[3]).strip()))
        except:
            entries.append(Manufacturer(str(i[0]).strip(), str(i[1]).strip(),
                                        str(i[2]).strip(), None))
    return entries


def read_price_data_file(filename, manufacturer_data):
     # Function to read prices of the items
    entries = []
    data = []
    file = open(filename, "r")
    for line in file.readlines():
        data.append(line.strip().split(","))
    file.close()
    for i in data:
        entries.append(Price(str(i[0]).strip(), str(i[1]).strip(), manufacturer_data))
    return entries


def read_service_dates_data_file(filename, manufacturer_price_data):
   #  Function to read service dates of the items
    entries = []
    data = []
    file = open(filename, "r")
    for line in file.readlines():
        data.append(line.strip().split(","))
    file.close()
    for i in data:
        entries.append(ServiceDates(str(i[0]).strip(), str(i[1]).strip(),
                                    manufacturer_price_data))
    return entries


def create_full_inventory_file(data, filename):
    # Function to create report file for all inventory
    file = open(filename, "w")
    for i in data:
        try:
            file.write(i.item_id + ", " + i.name + ", " + i.item_type + ", " +
                       i.price + ", " + i.date + ", " + i.condition + "\n")
        except:
            file.write(i.item_id + ", " + i.name + ", " + i.item_type + ", " +
                       i.price + ", " + i.date + "\n")
    file.close()


def create_each_inventory_file(data):
    # Function to create report file for each inventory
    inventory = dict()
    for i in data:
        if i.item_type in inventory:
            inventory[i.item_type].append(i)
        else:
            inventory[i.item_type] = [i]
    for key in inventory.keys():
        filename = str(key).capitalize() + "Inventory.csv"
        file = open(filename, "w")
        for i in inventory[key]:
            try:
                file.write(i.item_id + ", " + i.name + ", " + i.price + ", " +
                           i.date + ", " + i.condition + "\n")
            except:
                file.write(i.item_id + ", " + i.name + ", " + i.price + ", " +
                           i.date + "\n")
        file.close()


def create_past_service_date_inventory_file(data, filename):
    # Function to create report of inventories
    #whose service date is due
    file = open(filename, "w")
    for i in data:
        today = datetime.date.today().strftime("%y/%m/%d")
        temp = str(i.date).split("/")
        check = datetime.date(int(temp[2]), int(temp[0]), int(temp[1])).strftime("%y/%m/%d")
        if check < today:
            try:
                file.write(i.item_id + ", " + i.name + ", " + i.item_type + ", " + i.price +
                           ", " + i.date + ", " + i.condition + "\n")
            except:
                file.write(i.item_id + ", " + i.name + ", " + i.item_type + ", " + i.price +
                           ", " + i.date + "\n")
    file.close()


def create_damaged_inventory_file(data, filename):
    # Function to create report file of damaged inventory
    file = open(filename, "w")
    for i in data:
        if i.condition:
            file.write(i.item_id + ", " + i.name + ", " + i.item_type + ", " + i.price + ", " +
                       i.date + "\n")
    file.close()


def user_query():
    # function to get user input for the search parameters
    # returns a list of search parameters
    try:
        entry = input("Please enter your item search here with space separated "
                      "manufacturer and item type or q to quit: \n")
        if entry is "":
            raise ValueError
        else:
            return entry.split()
    except ValueError:
        print("Error! Empty input value")
        return None

if __name__ == '__main__':

    manufacturer_data = read_manufacturer_data_file("ManufacturerList.csv")
    price_data = read_price_data_file("PriceList.csv", manufacturer_data)
    service_dates_data = read_service_dates_data_file("ServiceDatesList.csv", price_data)
    create_full_inventory_file(sorted(service_dates_data,
                                      key=lambda x: x.name), "FullInventory.csv")
    create_each_inventory_file(sorted(service_dates_data, key=lambda x: x.item_id))
    create_past_service_date_inventory_file(sorted(service_dates_data,
                                                   key=lambda x: x.date,
                                                   reverse=False), "PastServiceDateInventory.csv")
    create_damaged_inventory_file(sorted(service_dates_data, key=lambda x: x.price, reverse=True),
                                  "DamagedInventory.csv")
    # start a while loop for indefinite recursion
    # till the user quits the query
    while True:
        query = user_query()    # call the function to get user input
        while query is None:    # loop the function till valid input
            query = user_query()
        if query[0] in ["q", "Q", "quit", "Quit"]:  # check if user wants to quit
            break
        else:       # if user doesn't wants to quit, continue further
            target_item_type = []   # create empty list for item type
            target_manufacturer = []    # create empty list for manufacturer name
            for i in query:     # recursion through all the search keywords
                if i.lower() in [str(x.name).lower() for x in service_dates_data]:
                    # if manufacturer name is found
                    # append to list of manufacturers
                    target_manufacturer.append(i.capitalize())
                if i.lower() in [str(x.item_type).lower() for x in service_dates_data]:
                    # if item type is found
                    # append to list of item type
                    target_item_type.append(i.lower())
            if len(target_manufacturer) > 1 or len(target_item_type) > 1:
                print("Invalid item search! Multiple search parameters found."
                      "Please try again one at a time!")
            elif len(target_manufacturer) == 0 and len(target_item_type) == 0:
                print("No search parameter found! Please try again!")
            elif len(target_manufacturer) == 1 and len(target_item_type) == 0:
                print("Item type is not specified in the search parameter! Please try again!")
            elif len(target_manufacturer) == 0 and len(target_item_type) == 1:
                # if only item type is passed in search parameters
                # print error message
                print("Manufacturer for the item type is missing! Please try again!")
            elif len(target_manufacturer) == 1 and len(target_item_type) == 1:
                # continue if valid search parameters are found
                # declare present date
                today = datetime.date.today().strftime("%y/%m/%d")
                target_item = False     # create a flag for target item
                for j in sorted(service_dates_data, key=lambda x: x.price, reverse=True):
                    temp = str(j.date).split("/")
                    check = datetime.date(int(temp[2]), int(temp[0]),
                                          int(temp[1])).strftime("%y/%m/%d")
                    if j.name == target_manufacturer[0] and j.item_type == target_item_type[0]:
                        # target item is set to true
                        # if manufacturer and item type are matched
                        target_item = True
                        try:
                            suggest_price = float(j.price)      # collect the price of target item
                            matched_id = j.item_id              # collect item id of target item
                        except:
                            pass
                        if check > today and not j.condition:
                            # print the item only if service date condition
                            # and item damage condition are passed
                            print("Your item is: {}\t{}\t{}\t{}".format(j.item_id, j.name,
                                                                        j.item_type, j.price))
                            break
                else:
                    # print the message if item not found
                    print("No item found in the inventory! Please try again!")
                if target_item:
                    # if target item flag is true
                    # loop through all data with similar item type
                    for k in sorted(service_dates_data, key=lambda x: x.price, reverse=True):
                        temp = str(k.date).split("/")
                        check = datetime.date(int(temp[2]), int(temp[0]), int(temp[1])).strftime("%y/%m/%d")
                        if k.item_type == target_item_type[0] and k.item_id != matched_id and check > today and not k.condition:
                            # get all items except for the item matched earlier as target item
                            try:
                                related_price = float(k.price)
                                if related_price in range(int(suggest_price-100), int(suggest_price+100)):
                                    # print the item details if price
                                    # is in range of +100 to -100 to that of target item
                                    print("You may, consider: {}\t{}\t{}\t{}".format(k.item_id, k.name, k.item_type, k.price))
                            except:
                                pass
