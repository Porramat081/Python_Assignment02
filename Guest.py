from Error import TypeException , OptionException , InvalidNumber

class Guest:
    __reward_rate = 100 # 100%
    __redeem_rate = 1

    @staticmethod
    def get_reward_rate():
        return Guest.__reward_rate
    
    @staticmethod
    def get_redeem_rate():
        return Guest.__redeem_rate
    
    @staticmethod
    def set_reward_rate(new_rate):
       Guest.__reward_rate = new_rate
    
    @staticmethod
    def set_redeem_rate(new_rate):
       Guest.__redeem_rate = new_rate

    @staticmethod
    def ask_number_guest():
        while True: 
            try:
                num_people = int(input("How many people will stay?:\n").strip())
                if type(num_people) is not int:
                    raise TypeException("number of guest","integer")
                else:
                    if num_people > 0:
                        return num_people
                    else:
                        raise InvalidNumber("number of guest",">0")
            except ValueError:
                print("\nInvalid input data type , please enter only integer data.\n")
            except Exception as e:
                print(e)
    
    def __init__(self,id:int,name:str,reward=0,reward_rate=0,redeem_rate=0):
        if type(id) != int:
            raise TypeException("id","integer")
        self.__id = id
        if not name.isalpha():
            raise TypeException("name","aplphabet")
        self.__name = name
        if  type(reward) not in (int,float):
            raise TypeException("reward","number or float")
        self.__reward = reward
        if reward_rate > 0:
            self.__reward_rate = reward_rate
        else:
            self.__reward_rate = Guest.get_reward_rate()
        if redeem_rate > 0:
            self.__redeem_rate = redeem_rate
        else:
            self.__redeem_rate = Guest.get_redeem_rate()

    @property
    def id(self):
        return self.__id    

    @property
    def name(self):
        return self.__name
    
    @property
    def reward(self):
        return self.__reward
    
    @property
    def reward_rate(self):
        return self.__reward_rate
    
    @property
    def redeem_rate(self):
        return self.__redeem_rate
    
    @reward.setter
    def reward(self, new_reward):
        if type(new_reward) not in (int,float):
            raise TypeException("reward","number or float")
        self.__reward = new_reward

    @reward_rate.setter
    def reward_rate(self, new_rate):
        if type(new_rate) not in (int,float):
            raise TypeException("reward rate","number or float")
        self.__reward_rate = new_rate

    @redeem_rate.setter
    def redeem_rate(self, new_rate):
        if type(new_rate) not in (int,float):
            raise TypeException("redeem rate","number or float")
        self.__redeem_rate = new_rate

    def get_reward(self,total_cost=None):
        if total_cost == None:
            return self.reward
        if type(total_cost) not in (int,float):
            raise TypeException("total cost","number or float")
        reward = (self.reward_rate/100 )* total_cost
        return round(reward)
    
    def update_reward(self,add_reward:float,down=False):
        if type(add_reward) not in (int,float):
            raise TypeException("add reward","number or float")
        else:
            if down:
                self.reward -= add_reward
            else:
                self.reward += add_reward

    def ask_use_reward(self):
        while True:
            try:
                if self.reward < 100:
                    return False
                input_option = input("Do you want to use your reward for discount? (y/n) : \n").strip()
                if input_option.lower() not in ("y","n"):
                    raise OptionException("y","n")
                return input_option.lower() == 'y'
            except Exception as e:
                print("\n",e,"\n")

    def display_info(self):
        print(f'{self.id} {self.name} has {self.reward} point {self.redeem_rate} {self.reward_rate}')
    
    def write_file(self):
        return f'{self.id},{self.name},{self.reward_rate},{self.reward},{self.redeem_rate}'

