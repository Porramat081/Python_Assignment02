from Error import TypeException


class Product:
    '''class Product - For managing product information'''
    # constructor - set attribute value for instance
    def __init__(self , id:int ,name:str,price:float):
        self.__id = id
        self.__name = name
        self.__price = price
    
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price
    
    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @price.setter
    def price(self, new_price):
        self.__price = new_price

    def display_info(self):
        '''display general product information'''
        rate = f'{float(self.__price):.2f} AUD'
        return f'{self.__id:<20}{self.__name:<30}{rate:<12}'

class ApartmentUnit(Product):
    '''class AparmentUnit - For managing aparment unit information (inherit from class Product)'''
    # constructor - set attribute value for instance
    def __init__(self, id, name, price,capacity):
        super().__init__(id, name, price)
        self.__capacity = capacity

    @property
    def capacity(self):
        return self.__capacity
    
    @capacity.setter
    def capacity(self, new_capacity):
        self.__capacity = new_capacity  

    @staticmethod
    def check_apt_name(apt_name:str , get_value=False):
        '''Validating Function for checking second part of apartment name format'''
        apt_name = apt_name[1:]
        if not apt_name[0].isnumeric():
            return False
        checked_index = 0
        for i in apt_name:
            if i.isnumeric():
                checked_index += 1
            else:
                break
        rest = apt_name[checked_index :]
        if not rest.isalpha():
            return False
        if get_value:
            return (apt_name[0:checked_index],rest)
        return True
    
    def display_info(self):
        '''display aparment information (overriding method)'''
        rate = f'{float(self.price):.2f} AUD'
        return f'{self.id:<18} {self.name:<29} {rate:<14} {self.capacity:<7}'

    def write_file(self):
        '''generate string for writing in csv'''
        return f'{self.id}, {self.name}, {self.price}, {self.capacity}'


class SupplementaryItem(Product):
    '''class SupplementaryItem - For managing supplement item information (inherit from class Product)'''
    # constructor - set attribute value for instance
    def __init__(self, id, name, price):
        super().__init__(id, name, price)
    def write_file(self):
        '''generate string for writing in csv'''
        return f'{self.id}, {self.name}, {self.price}'
    

class Bundle(Product):
    '''class Bundle - For managing bundle information (inherit from class Product)'''
    # constructor - set attribute value for instance
    def __init__(self, id, name, apt , sup_list:list[str] ,price):
        super().__init__(id, name, price)
        self.apt = apt
        self.sup_list = sup_list

    def set_apt(self,new_apt):
        self.apt = new_apt

    def set_sup_list(self , new_suplist):
        self.sup_list = new_suplist

    def get_sup_list(self):
        '''return supplement list in bundle'''
        sup_list_export = []
        for sup in self.sup_list:
            exist_product = False
            for sup_export in sup_list_export:
                if sup_export[0] == sup.strip():
                    exist_product = True
                    sup_export[1] += 1
            if not exist_product:
                sup_list_export.append({0:sup.strip(),1:1})
        return sup_list_export
                    
    def display_info(self):
        '''display bundle information (overriding method)'''
        dict_sup = {}
        for i in self.sup_list:
            if i.strip() not in dict_sup:
                dict_sup[i.strip()] = 1
            else:
                dict_sup[i.strip()] += 1
        list_sup_str = ""
        for k,v in dict_sup.items():
            add_str = str(v) + " x " + k
            list_sup_str += (add_str + ",")
        component_str = f'{self.apt.id},{list_sup_str}'
        format_price = f'{self.price} AUD'
        return f'{self.id:<12}{self.name:<35}{component_str:<39}{format_price:<10}'

    def write_file(self):
        '''generate string for writing in csv'''
        if len(self.sup_list) > 0:
            sup_list_str = ""
            for sup in self.sup_list:
                sup_list_str += sup.strip() +", "
            return f'{self.id}, {self.name}, {self.apt.id}, {sup_list_str}{self.price}'
        return f'{self.id}, {self.name}, {self.apt.id}, {self.price}'
