"""vending_machine.py - simulate a coin operated vending machine

Louis B
2019-10-08 -- Starter file for Project 1

This is a demonstration of a simple state machine.

The vending machine waits for coins to be deposited and the user
to make a selection. When the user makes the selection, the machine
dispenses the item but only if the coin total is greater than or
equal to the price of the item. Then the machine provides change if
needed.
"""

import time
import msvcrt # built-in module to read keyboard in Windows

products={'A':[50,'chocolate'],'B':[90,'juice'],'C':[200,'biscuit'],'D':[150,'shake'],'E':[120,'chips']}
money={'1':5,'2':10,'3':25,'4':100,'5':200}


# System constants
TESTING = True

# Support functions

def log(s):
    """Print the argument if testing/tracing is enabled."""
    if TESTING:
        print(s)

def get_event():
    """Non-blocking keyboard reader.
    Returns uppercase letter or digit, or "" empty string if no key pressed.
    """
    x = msvcrt.kbhit()
    #print(x)  # for debugging only
    if x: 
        ret = (msvcrt.getch().decode("utf-8")).upper()
        log("Event " + ret)
    else: 
        ret = ""
    return ret


###
# State machine
###
class VendingMachine(object):
    """Control a virtual vending machine."""
    def __init__(self):
        self.state = None  # current state
        self.states = {}  # dictionary of states
        self.event = ""  # no event detected

    def add_state(self, state):
        self.states[state.name] = state

    def go_to_state(self, state_name):
        if self.state:
            log('Exiting %s' % (self.state.name))
            self.state.exit(self)
        self.state = self.states[state_name]
        log('Entering %s' % (self.state.name))
        self.state.enter(self)

    def update(self):
        if self.state:
            self.state.update(self)


###
# States
###
class State(object):
    """Abstract parent state class."""
    def __init__(self):
        pass

    @property
    def name(self):
        return ''

    def enter(self, machine):
        pass

    def exit(self, machine):
        pass

    def update(self, machine):
        pass


###
# Define the State sub-classes here
###
class WaitingState(State):
    def __init__(self):
        State.__init__(self)
        
    @property
    def name(self):
        return 'waiting'
    
    def enter(self,machine):
        State.enter(self,machine)
        
    def update(self,machine):
        if machine.event in money:
            
            machine.go_to_state('amount')
           
    def exit(self,machine):
        State.exit(self,machine)


class AmountState(State):
    def __init__(self):
        State.__init__(self)
        
    @property
    def name(self):
        return 'amount'
    
    def enter(self,machine):
        if machine.event in money:
            print("amount: ",money[machine.event])
            machine.amt=money[machine.event]
        
    def update(self,machine):
        if machine.event in products:
            machine.go_to_state('product')
        elif machine.event in money:
            machine.amt+=money[machine.event]
            print("amount: ",money[machine.event])
        
            
    def exit(self,machine):
        print("total money: ",machine.amt)
        State.exit(self,machine)

        
class ProductState(State):
    def __init__(self):
        State.__init__(self)
        
    @property
    def name(self):
        return 'product'
    
    def enter(self,machine):
        machine.price=products[machine.event][0]
        machine.item=products[machine.event][1]
        
        
    def update(self,machine):
        if machine.amt>=machine.price:
            machine.go_to_state("assign")
        else:
            machine.event=''
            machine.go_to_state("amount")
      
        
    def exit(self,machine):
        State.exit(self,machine)

class AssignState(State):
    def __init__(self):
        State.__init__(self)
    @property
    def name(self):
        return 'assign'
    def enter(self,machine):
        pass
        
        print("dispensing ",machine.item)
    def update(self,machine):
        machine.change=machine.amt-machine.price
        
        if machine.change>0:
            machine.go_to_state('returning')
        else:
            machine.go_to_state('waiting')
            
    def exit(self,machine):
        print('closing valve')
        
        
class ReturnState(State):
    def __init__(self):
        pass
    @property
    def name(self):
        return 'returning'
    def enter(self,machine):
        print("change due: ",machine.change)
        
        
    def update(self,machine):
        while machine.change>=200:
            print('return 200')
            machine.change-=200
        while machine.change>=100:
            print('return 100')
            machine.change-=100
        while machine.change>=25:
            print('return 25')
            machine.change-=25
        while machine.change>=10:
            print("return 10")
            machine.change-=10
        while machine.change>=5:
            print('return 5')
            machine.change-=5
        if machine.change==0:
            machine.go_to_state('waiting')
            
            
    def exit(self,machine):
        pass
        
        
    
    
    
###
# Main program starts here
###
if __name__ == "__main__":
    # new machine object
    vending = VendingMachine()

    # Add the states
    vending.add_state(WaitingState())
    vending.add_state(AmountState())
    vending.add_state(ProductState())
    vending.add_state(AssignState())
    vending.add_state(ReturnState())
    # vending.add_state(zzzState())  
    # add all the states

    # Reset state is "waiting for first coin"
    vending.go_to_state('waiting')

    # begin continuous processing of events
    while True:
        try:
            vending.event = get_event()
        except KeyboardInterrupt:
            print("shutting down")
            break
        vending.update()

