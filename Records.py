from Error import ExtrabedException
from Guest import Guest
from Product import ApartmentUnit , SupplementaryItem , Bundle
from Order import Order

class Records:
    '''class Record - For managing record information'''
    # constructor - init attribute 3 lists : guest_list , product_list , order_list
    def __init__(self):
        self.guest_list = []
        self.product_list = []
        self.order_list = []

    def read_guests(self):
        '''read guest data in guests.csv and append those data to guest_list'''
        file = open("guests.csv","r",encoding='utf-8-sig')
        read_line = file.readline()
        while read_line:
            split_line = read_line.split(",")
            guest_id = int(split_line[0])
            guest_name = split_line[1]
            guest_reward = float(split_line[3])
            guest_reward_rate = float(split_line[2])
            guest_redeem_rate = float(split_line[4])
            guest = Guest(guest_id,guest_name,guest_reward,guest_reward_rate,guest_redeem_rate)
            self.guest_list.append(guest)     
            read_line = file.readline()
        file.close()
 
    def read_products(self):
        '''read product data in products.csv and append those data to product_list'''
        file = open("products.csv","r",encoding='utf-8')
        read_line = file.readline()
        while read_line:
            split_line = read_line.split(",")
            if split_line[0].strip().startswith("U"):
                apartment = ApartmentUnit(split_line[0].strip(),split_line[1].strip(),split_line[2].strip(),split_line[3][:-1].strip())
                self.product_list.append(apartment)
            elif split_line[0].startswith("SI"):
                supplement = SupplementaryItem(split_line[0].strip(),split_line[1].strip(),split_line[2][:-1].strip())
                self.product_list.append(supplement)
            elif split_line[0].startswith("B"):
                apt = self.find_product(split_line[2].strip())
                bundle = Bundle(split_line[0].strip(),split_line[1].strip(),apt,split_line[3:-1],split_line[-1].strip())
                self.product_list.append(bundle)
            read_line = file.readline()
        file.close()    

    def read_orders(self):
        '''read order data in orders.csv and append those data to order_list'''
        file = open("orders.csv","r",encoding="utf-8")
        read_line = file.readline()
        while read_line:
            split_line = read_line.split(",")
            guest_name = split_line[0].strip()
            apt_split = (split_line[1].strip()).split("x")
            apt_night = apt_split[0].strip()
            apt_name = apt_split[1].strip()
            apt = self.find_product(apt_name)
            price = split_line[-3].strip()
            reward = split_line[-2].strip()
            time_stamp = split_line[-1].strip()
            product_list = split_line[2:-3]
            apt_tuple = (apt,apt_night)
            product_tuple_list = [apt_tuple]

            for product in product_list:
                product_split = product.split("x")
                product_obj = self.find_product(product_split[1].strip(),sup=True)
                product_tuple = (product_obj,product_split[0].strip())
                product_tuple_list.append(product_tuple)

            guest = self.find_guest(guest_name)
            if guest:
                order = Order(guest,product_tuple_list,total_price=price,reward=reward,time_stamp=time_stamp)
                self.order_list.append(order)
            read_line = file.readline()
        file.close()   
                   

    def find_guest(self,query):
        '''find a guest in guest_list by search query (id or name)'''
        validate_guest = lambda guest : str(guest.id) == query or guest.name == query
        result = list(filter(validate_guest,self.guest_list))
        if len(result) != 0:
            return result[0]
        return None
    
    def find_product(self,query,sup=False):   
        '''find a product in product_list by search query (id or name)'''   
        validate_product = lambda product : (str(product.id) == query or product.name == query) and (isinstance(product,ApartmentUnit) or isinstance(product,Bundle))
        if sup:
            validate_product = lambda product : (str(product.id) == query or product.name == query) and isinstance(product,SupplementaryItem)
        result = list(filter(validate_product,self.product_list))
        if len(result) != 0:
            return result[0]
        return None
    
    def list_guests(self):
        '''display guest information in guest_list'''
        for guest in self.guest_list:
            guest.display_info()
    
    def update_products(self,productObj,length):
        '''update new product object to product_list'''
        current_product_id = productObj[0].id
        current_product_qty = productObj[1]
        filter_exist = lambda product : str(product.id) == current_product_id
        exist_product = list(filter(filter_exist,self.product_list))
        if len(exist_product)>0:
            if current_product_id == "SI6":
                if exist_product[0][1] + current_product_qty > 2:
                    raise ExtrabedException("max")
                else:
                    exist_product[0][1] = (exist_product[0][1]/length) + current_product_qty
                    exist_product[0][1] *= length
            else:
                exist_product[0][1] += current_product_qty
        else:
            self.list_products.append(productObj)

    def list_products(self , type="all" , get_len=False):
        '''display product information in product_list'''
        if type == 'apt':        
            for product in self.product_list:
                if isinstance(product,ApartmentUnit):
                    product.display_info()
        elif type == 'sup':
            len_sup = 0
            for product in self.product_list:
                if isinstance(product,SupplementaryItem):
                    if get_len:
                        len_sup += 1
                    else:
                        product.display_info()
            if get_len:
                return len_sup
        else:
            for product in self.product_list:
                product.display_info()

    def save_record(self):
        '''write data in guest_list , order_list , product_list to corresponding csv files'''
        with open("guests.csv", "w") as file1,open("orders.csv" , "w") as file2,open("products.csv", "w") as file3:
            for guest in self.guest_list:
                write_string = guest.write_file() + "\n"
                file1.write(write_string)
            
            for order in self.order_list:
                write_string = order.write_file() + "\n"
                file2.write(write_string)

            for product in self.product_list:
                write_string = product.write_file() + "\n"
                file3.write(write_string)
    
    def update_guest(self,new_rate,att='reward_rate'):
        '''update guest reward rate or redeem rate'''
        if att == 'reward_rate':
            Guest.set_reward_rate(new_rate)
            for guest in self.guest_list:
                guest.reward_rate = new_rate
        elif att == 'redeem_rate':
            Guest.set_redeem_rate(new_rate)
            for guest in self.guest_list:
                guest.redeem_rate = new_rate

    
    def list_guest_order(self,guest):
        '''display guest history order list'''
        init_str = f'{'This is the booking and order history for '+guest.name:^70}\n'
        init_str += f'{'Order ID':<10}{'Products Ordered':^38}{'Total Cost':<12}{'Earned Rewaeds':<10}\n'
        index = 1
        for order in self.order_list:
            if order.guest.name == guest.name:
               init_str += f'{'Order' + str(index):<10}'
               init_str += f'{order.display_order()}\n'
               index += 1
        print(init_str)
