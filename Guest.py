from Error import TypeException , OptionException , InvalidNumber

class Guest:
    '''class Guest - For managing guest information'''
    __reward_rate = 100 # 100%
    __redeem_rate = 1

    @staticmethod
    def get_reward_rate():
        ''' get static variable reward rate from class Guest '''
        return Guest.__reward_rate
    
    @staticmethod
    def get_redeem_rate():
        '''get static variable redeem rate from class Guest'''
        return Guest.__redeem_rate
    
    @staticmethod
    def set_reward_rate(new_rate):
       '''set new value to static variable reward rate'''
       Guest.__reward_rate = new_rate
    
    @staticmethod
    def set_redeem_rate(new_rate):
       '''set new value to static variable redeem rate'''
       Guest.__redeem_rate = new_rate

    @staticmethod
    def ask_number_guest():
        '''get number of guest input from user'''
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
    
    # constructor - set attribute value for instance
    def __init__(self,id:int,name:str,reward=0,reward_rate=0,redeem_rate=0):
        # check - data type before assign value
        if type(id) != int:
            raise TypeException("id","integer")
        if not name.isalpha():
            raise TypeException("name","aplphabet")
        if  type(reward) not in (int,float):
            raise TypeException("reward","number or float")
        self.__name = name
        self.__id = id
        self.__reward = reward
        # check - if already have own reward rate when read original data from csv
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
        '''calculate reward - used to calculate guest rewards'''
        if total_cost == None:
            return self.reward
        if type(total_cost) not in (int,float):
            raise TypeException("total cost","number or float")
        reward = (self.reward_rate/100 )* total_cost
        return round(reward)
    
    def update_reward(self,add_reward:float,down=False):
        '''update reward - used to add or reduce guest rewards'''
        if type(add_reward) not in (int,float):
            raise TypeException("add reward","number or float")
        else:
            if down:
                self.reward -= add_reward
            else:
                self.reward += add_reward

    def ask_use_reward(self):
        '''ask user for using the reward point'''
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
        '''display guest instance information'''
        reward = f'{self.reward:.2f}'
        reward_rate = f'{self.reward_rate:.2f}'
        redeem_rate = f'{self.redeem_rate:.2f}'
        return f'{self.id:<10}{self.name:<20}{reward:<15}{reward_rate:<15}{redeem_rate:<15}'
    
    def write_file(self):
        '''generate string for writing in csv'''
        return f'{self.id},{self.name},{self.reward_rate},{self.reward},{self.redeem_rate}'

