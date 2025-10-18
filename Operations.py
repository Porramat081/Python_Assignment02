from Error import CarParkException, ExtrabedException, InvalidNumber, TypeException
from Records import Records
from Guest import Guest
from Order import Order
from Product import ApartmentUnit, Bundle,SupplementaryItem


class Operations:
    def __init__(self , records : Records):
        self.records = records
    
    def ask_guest_name(self,check_order=False):
        while True:
            try:        
                name = input("Enter the name of the main guest [e.g. Porramat]:\n").strip()
                if not name.isalpha():
                    raise TypeException("name","alphabet")
                else:
                    exist_guest = self.records.find_guest(name)

                    if not exist_guest:
                        if check_order:
                            return None
                        new_guest = Guest(len(self.records.guest_list)+1 , name , reward=0)
                        self.records.guest_list.append(new_guest)
                        return new_guest
                    return exist_guest
            except Exception as e:
                print(e)

    def ask_apartment_id(self):
        while True:
            try:
                apt_id = input("Enter apartment unit ID or bundle ID to book:\n").strip()
                exist_apt = self.records.find_product(apt_id,sup=False)
                sup_list = []
                if not exist_apt:
                    print("this apartment id does not exist, please try again.")
                else:
                    if isinstance(exist_apt,Bundle):
                        sup_list = exist_apt.get_sup_list()
                        exist_apt.display_info()
                        return (exist_apt.apt , sup_list , exist_apt)
                    else:
                        exist_apt.display_info()
                        return (exist_apt,sup_list,None)
            except Exception as e:
                print(e)

    def ask_supplement_id(self,exist_extra_bed=0):
        while True:
            try:
                sup_id = input("Enter supplement id : \n").strip()
                exist_sup = self.records.find_product(sup_id , sup=True)
                if not exist_sup:
                    raise Exception("This supplement does not exist, please try again.")
                elif exist_sup.id == "SI6" and exist_extra_bed >= 2:
                    raise ExtrabedException("max" , exist_bed=exist_extra_bed)                    
                else:
                    return exist_sup
            except Exception as e:
                print(e)

    def ask_supplement_qty(self,product=None,stay_length=None,is_extrabed=False,exist_extra_bed=0):
        while True:
            try:
                sup_qty = int(input("Enter supplement qty : \n").strip())
                if sup_qty <= 0:
                    raise InvalidNumber('product quantity','>0')
                if is_extrabed or product.id == "SI6":
                    if sup_qty + exist_extra_bed > 2:
                        raise ExtrabedException(option="max" , exist_bed=exist_extra_bed)
                elif product.id == "SI1":
                    if sup_qty < stay_length:
                        raise CarParkException(str(stay_length))
                return sup_qty
            except ValueError:
                print("Invalid input data type , please enter only integer data.")
            except Exception as e:
                print(e)

    def ask_supplement(self,stay_length,sup_list,exist_extra_bed=0):
        s_list= []
        for sup_item in sup_list:
            s_item = self.records.find_product(sup_item[0].strip(),sup=True)
            s_list.append({0:s_item,1:sup_item[1]})
        supplement_list = [] + s_list
        while True:
            try:
                question = "Do you want to add supplement? (y/n)\n" if len(supplement_list) == 0 else \
                "Do you want to add another supplement? (y/n)\n"
                input_option = input(question).strip()
                if input_option.lower() not in ("y","n") :
                    raise Exception("please enter only 'y' or 'n'")
                if input_option.lower() == "y":
                    selected_sup = self.ask_supplement_id(exist_extra_bed)
                    selected_qty = self.ask_supplement_qty(selected_sup,stay_length,exist_extra_bed=exist_extra_bed)
                    is_exist_selected_sup = False
                    for sup in supplement_list:
                        if sup[0].id == selected_sup.id:
                            is_exist_selected_sup = True
                            if selected_sup.id == "SI6":
                                sup[1] += (int(selected_qty) + int(exist_extra_bed))* int(stay_length)
                            else:
                                sup[1] += int(selected_qty)
                    if not is_exist_selected_sup:
                        if selected_sup.id == "SI6":
                            supplement_list.append(({0:selected_sup,1:selected_qty*int(stay_length)}))
                        else:
                            supplement_list.append(({0:selected_sup,1:selected_qty}))
                elif input_option.lower() == "n":
                    return supplement_list
            except Exception as e:
                print("\n",e,"\n")
    
    def check_capacity(self,capacity,number_guest):
        is_exceed = False
        extra_bed_qty = 0
        if capacity < int(number_guest):
            print("Please consider ordering an extra bed.")
            extra_bed_qty = self.ask_supplement_qty(is_extrabed=True)
            if (extra_bed_qty * 2) + capacity <  int(number_guest):
                is_exceed = True 
            else:
                is_exceed = False
                extra_bed_item = self.records.find_product(query="SI6",sup=True)
                print("The cost for the supplementary item will be ${:.2f} per night".format(float(extra_bed_item.price) * extra_bed_qty))
        return is_exceed , extra_bed_qty

    def make_booking(self):
        print("\nmake booking\n")
        guest_obj = self.ask_guest_name()
        number_guest = Guest.ask_number_guest()
        selected_apt,sup_list,selected_bundle = self.ask_apartment_id()
        is_exceed , extra_bed_qty = self.check_capacity(int(selected_apt.capacity),number_guest)
        if is_exceed:
            print("Booking cannot proceed , number of guests exceed than room capacity")
            return
        check_in = Order.ask_date(type='in')
        (check_out , stay_length) = Order.ask_date(type='out' , compare_date=check_in)
        selected_sup = self.ask_supplement(stay_length , sup_list ,exist_extra_bed = extra_bed_qty)
        is_use_reward = guest_obj.ask_use_reward()
        product_list = [(selected_apt,int(stay_length))] + selected_sup
        new_order = Order(guest=guest_obj,product_list=product_list)
        if selected_bundle:
            new_order = Order(guest=guest_obj,product_list=product_list,bundle=selected_bundle)
        total_price , earn_reward =new_order.display_recript(number_guest=number_guest,check_in=check_in,check_out=check_out,use_reward=is_use_reward)
        new_order.set_total_price(total_price=total_price)
        new_order.set_reward(earn_reward)
        self.records.order_list.append(new_order)

    def add_update_apt(self):
        while True:
            try:
                print("Add/Update apartment unit")
                mod_apt = input("enter modifying apartment in format (apartment_id rate capacity) : \n").strip()
                if len(mod_apt.split(" ")) != 3:
                    print("invalid format , apartmentID rate capacity")
                else:
                    input_id , input_rate , input_capacity = mod_apt.split(" ")
                    input_id , input_rate , input_capacity = input_id.strip() , input_rate.strip() , input_capacity.strip()
                    if not input_id.startswith("U"):
                        raise Exception("ApartmentID must contain the leading capital U")
                    elif not ApartmentUnit.check_apt_name(input_id):
                        raise Exception("ApartmentID is invalid , must contain U + Unit number + alphabet")
                    elif not input_rate.isnumeric() and not isinstance(float(input_rate), float):
                        raise TypeException("Rate","integer",'float')
                    elif not input_capacity.isdigit():
                        raise TypeException("Capacity","integer")
                    elif float(input_rate) <= 0:
                        raise InvalidNumber("Rate",">0")
                    elif int(input_capacity) <= 0:
                        raise InvalidNumber("Capacity", ">0")
                    else:
                        # pass all validate
                        is_exist = self.records.find_product(input_id)
                        if not is_exist:
                            (unit_number , unit_name) = ApartmentUnit.check_apt_name(input_id,get_value=True)
                            gen_name = f'Unit {unit_number} {unit_name} Building'
                            new_apt = ApartmentUnit(input_id,gen_name,input_rate,input_capacity)
                            self.records.product_list.append(new_apt)
                            print("Add new apartment successfully")
                        else:
                            is_exist.price = float(input_rate)
                            is_exist.capacity = int(input_capacity)
                            print("Update existing apartment successfully")
                        break
            except ValueError:
                print("\nRate must be integer or float number\n")
            except Exception as e:
                print(e,"\n")

    def add_update_supplement(self):
        while True:
            try:
                input_update = input("enter updated supplementary list (item_name1<str> item_price1<num> , ...): \n").strip()
                input_update_list = input_update.split(",") if not input_update.endswith(",") else input_update[:-1].split(",")

                if len(input_update_list) >=1 :
                    for j in input_update_list:
                        update_item = j.strip().split(" ")
                        if len(update_item) < 2 or update_item == "":
                            raise Exception("invalid format -> item_name<str> item_price<num> , ...")
                        else:
                            if  update_item[0].strip().isnumeric():
                                raise Exception("supplement item name must be alphabet")
                            elif not update_item[1].strip().isnumeric() and not isinstance(float(update_item[1].strip()), float): # isinstance for checking type [7]
                                raise Exception("item price must be number")
                            elif float(update_item[1].strip()) <= 0:
                                raise Exception("item price must be positive number")
                            else:
                                product_name = update_item[0].strip()
                                product_price = float(update_item[1].strip())

                                is_exist = self.records.find_product(product_name)

                                if is_exist:
                                    is_exist.price = product_price
                                else:
                                    new_id = "SI" + str(self.records.list_products(type="sup",get_len=True) +1)
                                    new_member =  SupplementaryItem(id=new_id , name=update_item[0],price=update_item[1])
                                    self.records.product_list.append(new_member)
                    print("Add/Update Supplement Product successfully")
                    break
                else:
                    raise Exception("invalid format -> item_id item_price , ...")
            except ValueError:
                print("please enter item price with numeric data\n")
            except Exception as e:
                print(e , ", please try again","\n")

    def add_update_bundle(self):
        while True:
            try:
                input_update = input("enter adding/modifying apartment in format (bundle_name aparment_id sup1 sup2 ... rate) : \n")
                update_split = input_update.split(" ")
            except Exception as e:
                print(e,", please try again")

    def update_reward_rate(self):
        print("\nAdjust the reward rate of all guests\n")
        while True:
            try:
                input_rate = float(input("Enter new reward rate (parcentage) : \n").strip())
                self.records.update_guest(input_rate , att='reward_rate')
                print("update reward rate successfully")
                break
            except ValueError:
                print("New rate must be number / float data type")
            except Exception as e:
                print(e)

    def update_redeem_rate(self):
        print("\nAdjust the redeem rate of all guests\n")
        while True:
            try:
                input_rate = float(input("Enter new redeem rate : \n").strip())
                self.records.update_guest(input_rate , att='redeem_rate')
                print("update redeem rate successfully")
                break
            except ValueError:
                print("New rate must be number / float data type")
            except Exception as e:
                print(e)

    def display_exist_guest(self):
        print("\ndisplay exist guest\n")
        self.records.list_guests()
    
    def display_exist_apartment(self):
        print("\ndisplay exist apartment\n")
        self.records.list_products(type='apt')
    
    def display_exist_supplement(self):
        print("\ndisplay exist supplement\n")
        self.records.list_products(type='sup')
    
    def display_exist_product(self):
        print("\ndisplay exist product\n")
        self.records.list_products()
    
    def display_exist_order(self):
        print("\ndisplay exist order\n")
        for order in self.records.order_list:
            order.display_info()
    
    def display_guest_order(self):
        print("\nDisplay a guest order history\n")
        while True:
            try:
                exist_guest = self.ask_guest_name(check_order=True)
                if not exist_guest:
                    raise Exception("This guest does not exist , please try again")
                self.records.list_guest_order(exist_guest)
                break
            except Exception as e:
                print(e)
        
    def generate_stat(self):
        print("\nGenerate key statistics\n")
        with open("stats.txt", "w") as f:
            stat_text = self.records.generate_stat()
            f.write("Woops! I have deleted the content!")

    def save_record(self):
        print("\nsave all record\n")
        self.records.save_record()  