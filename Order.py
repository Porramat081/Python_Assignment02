from datetime import datetime
from Guest import Guest

class Order:
    current_date = datetime.now()
    time_stamp = current_date.strftime("%d/%m/%Y %H:%M")

    def __init__(self,guest:Guest,product_list=[],time_stamp=time_stamp,total_price=0,reward=0):
        self.guest = guest
        self.product_list = product_list
        self.time_stamp = time_stamp
        self.total_price = total_price
        self.reward = reward

    def set_total_price(self,total_price):
        self.total_price = total_price
    
    def set_reward(self,reward):
        self.reward = reward

    @staticmethod
    def ask_date(type="in" , compare_date=""):
        while True:
            try:
                question = "When will the guest is expected to check {} (d/m/yyyy):\n".format(type)
                input_date = input(question).strip()
                list_date = input_date.split("/")
                if len(list_date) != 3:
                    raise Exception('Date invalid , please entering in format d/m/yyyy')
                d,m,y = list_date[0].strip() , list_date[1].strip()  , list_date[2].strip() 
                if not d.isnumeric() or not m.isnumeric() or not y.isnumeric():
                    raise Exception("Date invalid , please entering numeric data in format d/m/yyyy")
                formatted_date = datetime(int(y),int(m),int(d))
                if type == 'in' and (formatted_date - datetime.now()).days < -1 :
                    raise Exception("Check-in date must not be earlier booking date")
                elif compare_date and type == 'out':
                    list_date = compare_date.split("/")
                    fd,fm,fy = list_date[0].strip() , list_date[1].strip()  , list_date[2].strip() 
                    formatted_compare = datetime(int(fy),int(fm),int(fd))
                    length_stay = (formatted_date - formatted_compare).days 
                    if length_stay > 7:
                        raise Exception("Length of stay must not exceed than 7 days")
                    elif length_stay <= 0:
                        raise Exception("Check-out date must be after check-in date at least 1 day")
                    return f'{d}/{m}/{y}' , length_stay
                return f'{d}/{m}/{y}'
            except Exception as e:
                print("\n",e,"\n")
    
    def display_recript(self,number_guest,check_in , check_out , use_reward):
        total_price,discount,final_price,earn_reward,used_reward = self.compute_cost(use_reward)
        sup_str , sup_total = self.format_sup_list(self.product_list[0][1])
        receipt = f'{'='*69}\n{"Debuggers Hut Serviced Apartments - Booking Receipt":^70}\n{'='*69}\
            \n{'Guest name:':<28}{self.guest.name}\
            \n{'Number of guests:':<28}{number_guest}\
            \n{'Apartment name:':<28}{self.product_list[0][0].name}\
            \n{'Apartment rate:$':<28}{self.product_list[0][0].price} (AUD)\
            \n{'Check-in date:':<28}{check_in}\
            \n{'Check-out date:':<28}{check_out}\
            \n{'Length of stay:':<28}{self.product_list[0][1]} (nights)\
            \n{'Booking date:':28}{datetime.now().strftime("%d/%m/%Y")}\
            \n{'Sub-total:$':<28}{float(self.product_list[0][0].price )* int(self.product_list[0][1])} (AUD)\
            \n{'-'*69}\
            \n{'Supplementary items'}\
            \n{sup_str}\
            \n{'Sub-total:$':<28}{sup_total} (AUD)\
            \n{'-'*69}\
            \n{'Total cost:$':<28}{total_price} (AUD)\
            \n{'Reward points to redeem:':<28}{used_reward} (points)\
            \n{'Discount based on points:$':<28}{discount} (AUD)\
            \n{'Final total cost:$':<28}{final_price} (AUD)\
            \n{'Earned rewards:':<28}{earn_reward} (points)\
            \n\nThank you for your booking!\nWe hope you will have an enjoyable stay.\n{'='*69}'
        print(receipt)
        return final_price , earn_reward

    def format_sup_list(self,length):
        sup_list = self.product_list[1:]
        total_sup = 0
        init_str = f'{'ID':^10}{'Name':^28}{'Quantity':^10}{'Unit Price$':^15}{'Cost$':^8}\n'
        if len(sup_list) == 0:
            return 'None',0
        else:
            for i in sup_list:
                sup = i[0]
                qty = i[1]
                total = float(sup.price) * int(qty)
                if sup.id == "SI6":
                    qty = f'{qty/length:.0f} x {str(length)} nights'
                total_sup += total
                init_str += f'{sup.id:^10}{sup.name:^28}{qty:^10}{sup.price:^15}{total:^8}\n'
        return init_str,total_sup

    def compute_cost(self,use_reward):
        total_price = 0
        discount = 0
        for i in self.product_list:
            total_price += (float(i[0].price) * int(i[1]))
        guest_reward = self.guest.get_reward(total_cost=None)
        used_point = guest_reward 
        if guest_reward >= 100 and use_reward:
            discount = self.guest.redeem_rate * (guest_reward / 100)
        if guest_reward * self.guest.redeem_rate / 100 > total_price:
            used_point = total_price * self.guest.redeem_rate / 100
        final_price = total_price-discount
        self.guest.update_reward(add_reward=used_point , down=True)
        earn_reward = self.guest.get_reward(final_price)
        self.guest.update_reward(earn_reward)
        return total_price,discount,final_price,earn_reward,used_point
    
    def display_info(self):
        self.guest.display_info()
        for sup in self.product_list:
            sup[0].display_info()
    
    def write_file(self):
        init_string = f'{self.guest.name}, {self.product_list[0][1]} x {self.product_list[0][0].id}, {self.total_price}, {self.reward}, {self.time_stamp}'
        product_string = ''
        if len(self.product_list[1:0]) > 0:
            for product in self.product_list[1:]:
                new_string = f'{product[1]} x {product[0].id},'
                product_string += new_string
        if product_string != '':
            init_string = f'{self.guest.name}, {self.product_list[0][1]} x {self.product_list[0][0].id}, {product_string} {self.total_price}, {self.reward}, {self.time_stamp}'
        return init_string
