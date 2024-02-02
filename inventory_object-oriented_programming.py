
#========Importing libraries==========
import tabulate 
from colorama import Style 

#========The beginning of the class==========
'''Create a Shoe class for a Shoe object'''
class Shoe:
    '''Declare the constructor method with five parameters,
    and pointers to properties of each shoe object.'''
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    '''Define a method to get the shoe list for each shoe object'''
    def get_shoe_list(self):
        return [self.country, self.code, self.product,  self.cost, self.quantity]
   
    '''Define a method to get the cost of the shoe.'''
    def get_cost(self):
        return self.cost

    '''Define a method to get the quantity of the shoes.'''
    def get_quantity(self):
        return self.quantity

    '''Define a string representation of the shoe object when printed.'''
    def __str__(self):
        return f'Country:\t{self.country}\nCode:\t\t{self.code}\nProduct:\t{self.product}\nCost:\t\t{self.cost}\nQuantity:\t{self.quantity}'


#=============Shoe list===========
'''Define a list to store shoe objects'''
shoe_list = []


#==========Functions outside the class==============
'''Create a function to print bold messages efficiently using colorama'''
def print_with_colorama(bold_message, message, style = Style.BRIGHT, style_reset = Style.RESET_ALL):
    print(style + f'\n{bold_message}: ' + style_reset + f'{message}\n')

'''Create a error handling function for numeric inputs using while loop'''
def get_numeric_input(prompt, data_type = float):
    while True:
        try:
            value = data_type(input(prompt))
            return value
        except ValueError:
            print_with_colorama('ValueError', f'Please enter a valid {data_type.__name__.lower()} value.')

def read_shoes_data():
    '''Use try except for error handling when opening
    the inventory.txt file, else print error message.'''
    try:
        with open('inventory.txt', 'r') as inventory_file:
            '''Use readline() to skip the first line and then use a
            for loop to strip and split each line to extract shoe data'''
            inventory_file.readline()
            for shoe_line in inventory_file:
                shoes_data = shoe_line.strip('\n').split(',')
                country = shoes_data[0]
                code = shoes_data[1]
                product = shoes_data[2]
                cost = shoes_data[3]
                quantity = shoes_data[4]

                '''Call Shoe class to create shoe object using extracted 
                data as parameters then append shoe_list with object'''
                shoe_object = Shoe(country, code, product, float(cost), int(quantity))
                shoe_list.append(shoe_object)

            '''Print message that shoes data has been read.'''
            print_with_colorama('ReadShoesDataSuccessful', 'you have read shoes data :)')

    except FileNotFoundError:
        print_with_colorama('ReadShoesData_FileNotError', 'inventory.txt file does not exist :(')
    except IndexError:
        print_with_colorama('ReadShoesData_IndexError','index error in code :(')

def capture_shoes():
    '''Print message that capture a shoe has been selected'''
    print_with_colorama('CaptureAShoeSelected', 'you have selected to capture a shoe, details:')
    
    '''Prompt user to enter shoe country, code, and product to capture'''
    shoe_country = str(input('Enter country of the shoe: '))
    shoe_code = input('\nEnter the shoe code: ')
    shoe_product = input('\nEnter the shoe product: ')

    '''Use get_numeric_input function to enter cost and quantity'''
    shoe_cost = get_numeric_input('\nEnter the shoe cost: ')
    shoe_quantity = get_numeric_input('\nEnter the shoe quantity: ', data_type = int)
    
    '''Append the shoe list using the information entered by user.'''
    shoe_list.append(Shoe(shoe_country, shoe_code, shoe_product, shoe_cost, shoe_quantity))

    '''Write on inventory.txt file to update shoe information'''
    with open ('inventory.txt', 'w') as inventory_file:
        inventory_file.write('Country,Code,Product,Cost,Quantity\n')
        for line in shoe_list:
            country, code, product, cost, quantity = line.country, line.code, line.product, line.cost, line.quantity
            inventory_file.write(f'{country},{code},{product},{cost},{quantity}\n')

    '''Print a message for successful shoe capture and appending list'''
    print_with_colorama('CaptureAShoeSuccessful', f'{shoe_product} captured and appended on last row:')

    view_all()  # Call function to view all

def view_all():
    '''Print message that view all shoes has been selected'''
    print_with_colorama('ViewAllShoesSelected', 'viewing all shoes, details:')

    '''Create a shoe list in 2d using comprehension method
    and use the tabulate module to print the shoe list'''
    shoe_list_2d = [shoe.get_shoe_list() for shoe in shoe_list]
    print(tabulate.tabulate(shoe_list_2d, headers= ['Country', 'Code', 'Product', 'Cost', 'Quantity']))
    
    '''Print message that viewing all shoes data has been completed'''
    print_with_colorama('ViewAllShoesSuccessful', 'you have viewed all shoes data :)')

def re_stock():
    '''Create variable for index of shoe object with lowest quantity'''
    index_shoe_lowest_qty = 0

    '''Find the index of shoe object with lowest quantity using
    enumerate and check if assumed index has lowest quantity'''
    for i, shoe_obj in enumerate(shoe_list):
        if shoe_obj.get_quantity() < shoe_list[index_shoe_lowest_qty].get_quantity():
            index_shoe_lowest_qty = i

    '''Print the information of the shoe with the lowest quantity'''
    print_with_colorama('ReStockLowestQuantitySelected', f'{shoe_list[index_shoe_lowest_qty].product} has the lowest quantity, shoe details:')
    print('--------------------------------------')
    print(shoe_list[index_shoe_lowest_qty])
    print('--------------------------------------\n')

    ''' Request user to answer if they want to re-stock the shoe'''
    re_stock_request = str(input(f'Would you like to re-stock {shoe_list[index_shoe_lowest_qty].product}? (yes/no): ').lower())

    '''If user would like to re-stock, then use while True
    and try except to input the quantity to be restocked'''
    if re_stock_request == 'yes':
        while True:
            try:
                re_stock_quantity = int(input('\nEnter the quantity to be re-stocked (e.g 100): '))
                break
            except ValueError:
                print('\nYou have entered an invalid quantity :( Try again!')
        
        '''Add the quantity to be re-stocked to the current quantity
        and print the shoe information with re-stocked quantity'''
        shoe_list[index_shoe_lowest_qty].quantity += re_stock_quantity
        print_with_colorama('ReStockSuccessful', f' quantity of {shoe_list[index_shoe_lowest_qty].product} after re-stocking is {shoe_list[index_shoe_lowest_qty].get_quantity()}, details:')
        print('--------------------------------------')
        print(shoe_list[index_shoe_lowest_qty])
        print('--------------------------------------\n')

        '''Write on inventory.txt file to update shoe information'''
        with open('inventory.txt', 'a') as inventory_file:
            inventory_file.write('Country,Code,Product,Cost,Quantity\n')
            for shoe_line in range(len(shoe_list)):
                inventory_file.write(f'{shoe_list[shoe_line].country},{shoe_list[shoe_line].code},{shoe_list[shoe_line].product},{shoe_list[shoe_line].cost},{shoe_list[shoe_line].quantity}\n')

        '''Print a message for successful shoe capture and appending list'''
        print_with_colorama('ReStockUpdatedTable', 'the updated table of all shoes data after re-stocking:')

        view_all()  # Call function to view all

        '''Print re-stocking and file update were completed'''
        print_with_colorama('ReStock&FileWritingSuccessful:', f're-stocking and updating inventory.txt file completed :)')

def seach_shoe():

    view_all()  # Call function to view all

    '''Request user to input the shoe code to print shoe information'''
    shoe_code = input('Enter shoe code (from table above) to print shoe information: ')

    '''Use for loop to search and if shoe code finds a match 
    then assign to a variable then print'''
    for shoe_info in range(len(shoe_list)):
        if shoe_code == shoe_list[shoe_info].code:
            searched_shoe = shoe_list[shoe_info]

    '''Print message that search a shoe has been selected and details'''
    print_with_colorama('SearchShoeSelected', f'you have selected to view {searched_shoe.code} shoe, details:')
    print('--------------------------------------')
    print(searched_shoe)
    print('--------------------------------------')
    print_with_colorama('SearchShoeSuccessful', f'you have viewed {searched_shoe.code} shoe details :)')

def value_per_item():
    '''Print that value per item for all shoes has been selected'''
    print_with_colorama('ValuePerItemSelected', 'value per item for all shoes is on the last column, details:')
    
    '''Create a empty value list to be appended with objects with a column
    of value per item. Use a for loop and methods to calculate value.'''
    value_list = []
    for shoe_line in range(len(shoe_list)):
        shoe_value = float(shoe_list[shoe_line].get_cost()  * shoe_list[shoe_line].get_quantity())
        shoe_info_list = shoe_list[shoe_line].get_shoe_list()
        shoe_info_list.append(shoe_value)
        value_list.append(shoe_info_list)

    '''Print that calculation for value is completed and 
    print value table using tabulate module.'''
    print(tabulate.tabulate(value_list, headers= ['Country', 'Code', 'Product', 'Cost', 'Quantity', 'Value']))

    '''Print that value per item for all shoes has been completed'''
    print_with_colorama('ValuePerItemSuccessful', 'you have printed the value per item for all shoes :)')

def highest_qty():
    '''Create variable for index of shoe object with highest quantity'''
    index_shoe_highest_qty = 0

    '''Find the index of shoe object with highest quantity using
    enumerate and check if assumed index has highest quantity'''
    for i, shoe_obj in enumerate(shoe_list):
        if shoe_obj.get_quantity() > shoe_list[index_shoe_highest_qty].get_quantity():
            index_shoe_highest_qty = i

    '''Print the information of the shoe with the highest quantity'''
    print_with_colorama('HighestQuantitySaleSelected', f'{shoe_list[index_shoe_highest_qty].product} has the highest quantity and on sale, shoe details:')
    print('--------------------------------------')
    print(shoe_list[index_shoe_highest_qty])
    print('--------------------------------------')
    print_with_colorama('HighestQuantitySaleSuccessful','you have printed the shoe on sale with the highest quantity :)')


#==========Main Menu=============
'''Call function to read shoes data'''
read_shoes_data()

'''Create a menu to prompt user to execute functions using a while loop'''
while True:
    menu = input('''Select one of the following options:
    cs - capture a shoe
    vs - view all shoes
    re - re-stock of lowest quantity 
    ss - search a shoe
    vp - value per item for all shoes
    hs - highest quantity shoe sale
    ex - exit
    : ''').lower()

    if menu == 'cs' :

        capture_shoes() # Call function to capture a shoe

    elif menu == 'vs':
        
        view_all()  # Call function to view all

    elif menu == 're':

        re_stock()  # Call function to re-stock shoe with lowest quantity

    elif menu == 'ss':

        seach_shoe()    # Call function to search shoe

    elif menu == 'vp':

        value_per_item()    # Call function to calculate and print value per item

    elif menu == 'hs':

        highest_qty()   # Call function to find and print shoe with highest quantity

    elif menu == 'ex':
        print_with_colorama('Goodbye!!!', 'You have to re-run the program to login. :)')
        exit()  
