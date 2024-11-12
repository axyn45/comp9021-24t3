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

class Building:
    number_created=0
    def __init__(self,height,entries) -> None:
        # print(height)
        print('init:',height,entries)
        self.height=height
        self.entries=entries.split(' ')
        self.populations={}
        for i in range(height):
            self.populations[i]=0
        Building.number_created+=1

    def __repr__(self) -> str:
        return f"Building({self.height}, '{' '.join(self.entries)}')"

    def __str__(self) -> str:
        return f"Building with {self.height+1} floor{'s' if self.height>0 else ''} accessible from entries: {', '.join(self.entries)}"

    class BuildingError(Exception):

        pass
    def go_to_floor_from_entry(self,floor, entry, nb_of_people):
        if(floor<0 or  floor>=self.height or entry not in self.entries or nb_of_people<=0):
            raise self.BuildingError("That makes no sense!").with_traceback('...')
        print('go to floor:',floor,entry,nb_of_people)
    
    def leave_floor_from_entry(self,floor, entry, nb_of_people):
        if(floor<0 or floor>=self.height or entry not in self.entries or nb_of_people<=0 or self.populations[floor]<nb_of_people):
            raise self.BuildingError("That makes no sense!").with_traceback('...')
        print('leave floor:',floor,entry,nb_of_people)

    pass
    # REPLACE PASS WITH YOUR CODE

    
def compare_occupancies(building_1, building_2):
    pass
    # REPLACE PASS WITH YOUR CODE
        
# a=Building(10,'A B C D')
# print(repr(a))
# b=Building(2,'F')
# print(Building.number_created)