# Written by *** for COMP9021

# Defines a class Building that defines a few special methods,
# as well as the two methods:
# - go_to_floor_from_entry()
# - leave_floor_from_entry()
# and an atribute, number_created, to keep track of
# the number of Building objects that have been created.
#
# Also defines a function compare_occupancies() meant to take
# as arguments two Building objects.
#
# Building objects are created with statements of the form
# Building(height, entries) where height is a positive integer
# (possibly equal to 0) and entries is a nonempty string that
# denotes all access doors to the building, with at least
# one space within the string to separate entries.
# You can assume that height and entries are as expected.
#
# If building denotes a Building object, then
# building.go_to_floor_from_entry(floor, entry, nb_of_people)
# takes as argument an integer, a string, and an integer.
# An error of type BuildingError is raised,
# all with the same message, if:
# - floor is not between 0 and the building's height, or
# - entry is not one of the building's entries, or
# - nb_of_people is not strictly positive.
# If the lift at that entry has to go down,
# then by how many floors it has to go down is printed out.
#
# If building denotes a Building object, then
# building.leave_floor_from_entry(floor, entry, nb_of_people)
# takes as argument an integer, a string, and an integer.
# An error of type BuildingError is raised if:
# - floor is not between 0 and the building's height, or
# - entry is not one of the building's entries, or
# - nb_of_people is not strictly positive, or
# - there are not at least nb_of_people on that floor.
# The same error message is used for the first 3 issues,
# and another error message is used for the last issue.
# If the lift at that entry has to go up or down, then
# by how many floors it has to go up or down is printed out.
#
# For the number of floors to go up or down, use
# "1 floor..." or "n floors..." for n > 1.


# DEFINE AN ERROR CLASS HERE
# import sys
# import traceback

class BuildingError(Exception):
    # def __init__(self, *args):
        # sys.excepthook = custom_excepthook

    # def __str__(self):
    #     return "That makes no sense!"
    pass

# def custom_excepthook(exc_type, exc_value, exc_traceback):
#         module_name = exc_type.__module__
#         if module_name and module_name != "builtins":
#             full_exception_name = f"{module_name}.{exc_type.__name__}"
#         else:
#             full_exception_name = exc_type.__name__
            
#         print("Traceback (most recent call last):")
#         print("...")
#         print(f"{full_exception_name}: {exc_value}")

# sys.excepthook = custom_excepthook

class Building:
    number_created=0
    def __init__(self,height,entries) -> None:
        # print(height)
        # print('init:',height,entries)
        self.height=height
        self.entries=entries.split(' ')
        self.populations={}
        for i in range(height):
            self.populations[i]={}
        Building.number_created+=1
        self.currentFloor={}
        
    def __repr__(self) -> str:
        return f"Building({self.height}, '{' '.join(self.entries)}')"

    def __str__(self) -> str:
        return f"Building with {self.height+1} floor{'s' if self.height>0 else ''} accessible from entries: {', '.join(self.entries)}"
    
    def sum(self):
        sump=0
        for _,v1 in self.populations.items():
            for _,v2 in v1.items():
                sump+=v2
        return sump

    def go_to_floor_from_entry(self,floor, entry, nb_of_people):
        # print('go to floor:',floor,entry,nb_of_people)
        if(floor<0 or  floor>=self.height or entry not in self.entries or nb_of_people<=0):
            raise BuildingError("That makes no sense!")
        if(entry in self.currentFloor and self.currentFloor[entry]!=0):
            diff=self.currentFloor[entry]
            print(f"Wait, lift has to go down {diff} floor{'s' if diff>1 else ''}...")
        if(entry not in self.populations[floor]):
            self.populations[floor][entry]=nb_of_people
        else:
            self.populations[floor][entry]+=nb_of_people
        self.currentFloor[entry]=floor

    def leave_floor_from_entry(self,floor, entry, nb_of_people):
        # print('leave floor:',floor,entry,nb_of_people)
        if(floor<0 or floor>=self.height or entry not in self.entries or nb_of_people<=0):
            raise BuildingError("That makes no sense!")
        elif(entry not in self.populations[floor] or self.populations[floor][entry]<nb_of_people):
            raise BuildingError("There aren't that many people on that floor!")
        if(entry in self.currentFloor and self.currentFloor[entry]!=floor):
            diff=floor-self.currentFloor[entry]
            print(f"Wait, lift has to go {'down' if diff<0 else 'up'} {abs(diff)} floor{'s' if abs(diff)>1 else ''}...")
        self.populations[floor][entry]-=nb_of_people
        self.currentFloor[entry]=0
        

    # pass
    # REPLACE PASS WITH YOUR CODE

    
def compare_occupancies(building_1, building_2):
    # print('compare')
    sum1=building_1.sum()
    sum2=building_2.sum()
    if(sum1==sum2):
        print("There is the same number of occupants in both buildings.")
    elif(sum1>sum2):
        print("There are more occupants in the first building.")
    else:
        print("There are more occupants in the second building.")
    # pass
    # REPLACE PASS WITH YOUR CODE
        
if __name__=='__main__':
    # a=Building(10,'A B C D')
    # b=Building(31,'1')
    # a.go_to_floor_from_entry(0,'B',4)
    # b.go_to_floor_from_entry(17,'1',4)
    # b.leave_floor_from_entry(17,'1',3)
    # a.leave_floor_from_entry(0,'B',1)
    # a.leave_floor_from_entry(0,'B',1)
    # a.leave_floor_from_entry(0,'B',1)
    a=Building(6,'A B Z')
    a.go_to_floor_from_entry(3,'B',1)
    a.go_to_floor_from_entry(3,'B',1)
    a.go_to_floor_from_entry(3,'B',1)
    a.go_to_floor_from_entry(3,'B',2)
    a.leave_floor_from_entry(3,'B',2)
    a.leave_floor_from_entry(3,'B',2)
    a.go_to_floor_from_entry(4,'A',10)
    a.go_to_floor_from_entry(5,'A',10)
    a.go_to_floor_from_entry(2,'A',10)
    a.leave_floor_from_entry(4,'A',2)
    a.go_to_floor_from_entry(1,'A',10)
    a.leave_floor_from_entry(5,'A',2)
    a.go_to_floor_from_entry(5,'A',10)
    a.leave_floor_from_entry(5,'B',2)


    
    # the_horizons = Building(10, 'A B C D')
    # print(repr(the_horizons))