# S4144787 : Porramat Thaepngoen
# Assignment 2 : part 2 (100%) - pre-version implementation

import os.path as op
from Operations import Operations
from Records import Records

class Main:
    def run():
        if not op.exists("guests.csv"):
            print("Not found guests.csv")
        elif not op.exists("products.csv"):
            print("Not found products.csv")
        elif not op.exists("orders.csv"):
            print("Not found orders.csv")
        else:
            record = Records()
            record.read_guests()
            record.read_products()
            record.read_orders()

            operation = Operations(record)

            while True:
                try:
                    list_option = f'''
{"Welcome to Debugger's Hut Serviced Aparments!".center(58," ")}
==========================================================
Please choose from the following options:
1) Make a booking
2) Add/Update information of an apartment unit
3) Add/Update information of multiple supplementary items
4) Add/Update information of bundle
5) Display existing all guests
6) Display a guest order history
7) Display existing all products
8) Display existing all aparment units
9) Display existing all supplementary items
10) Display existing all orders
11) Adjust the reward rate of all guests
12) Adjust the redeem rate of all guests
0) Exit the program
==========================================================
'''
                    print(list_option)
                    input_option = int(input('Enter option : ').strip())
                    
                    if input_option == 1:
                        operation.make_booking()
                    elif input_option == 2:
                        operation.add_update_apt()
                    elif input_option == 3:
                        operation.add_update_supplement()
                    elif input_option == 4:
                        operation.add_update_bundle()
                    elif input_option == 5:
                        operation.display_exist_guest() 
                    elif input_option == 6:
                        operation.display_guest_order()
                    elif input_option == 7:
                        operation.display_exist_product()
                    elif input_option == 8:
                        operation.display_exist_apartment()
                    elif input_option == 9:
                        operation.display_exist_supplement()
                    elif input_option == 10:
                        operation.display_exist_order()
                    elif input_option == 11:
                        operation.update_reward_rate()
                    elif input_option == 12:
                        operation.update_redeem_rate()
                    elif input_option == 0:
                        operation.save_record()
                        print("Exit the program , bye!!")
                        break
                    else:
                        raise Exception("please , enter only 0 - 12")
                except ValueError:
                    print("please , enter only number 0 - 12")
                except Exception as e:
                    print("\n",e,"\n")
    
if __name__ == "__main__":
    Main.run()