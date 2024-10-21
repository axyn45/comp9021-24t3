# Written by *** for COMP9021
#
# Uses the file cardio_train.csv downloaded from
# https://www.kaggle.com/sulianova/cardiovascular-disease-dataset
#
# Implements a function analyse(gender, age)
# where gender is one of 'F' (for female) or 'M' (for male),
# and where age is any integer for which we have data in the file
# (nothing needs to be done if that is not the case).
#
# We assume that all years have 365 days;
# in particular, someone who is 365 days old is 0 year old,
# and someone who is 366 days old is 1 year old.
#
# We ignore records for which at least one of these conditions holds:
# - height < 150 or height > 200
# - weight < 50 or weight > 150
# - ap_hi < 80 or ap_hi > 200
# - ap_lo < 70 or ap_lo > 140
#
# For each of both classes "cardio problem" and "no cardio problem"
# (as given by the cardio attribute), we create 5 bins/categories for
# height, weight, ap_hi, ap_lo, of equal width,
# that span between smallest value and largest value
# for the attribute in the category.
# For instance, suppose that gender is 'F' and age is 48.
# - Suppose that for the category "cardio problem",
#   the shortest woman aged 48 is 150cm tall, and
#   the tallest woman aged 48 is 200cm tall.
#   Then each of the 5 categories for the class "cardio problem"
#   and for the attribute "height" spans 10cm.
# - Suppose that for the class "no cardio problem",
#   the shortest woman aged 48 is 158cm tall, and
#   the tallest woman aged 48 is 193cm tall.
#   Then each of the 5 categories for the class "no cardio problem"
#   and for the attribute "height" spans 7cm.
# To avoid boundary issues, add 0.1 to the maximum value
# (so with the previous example, the maximum heights would be
# considered to be 200.1 and 193.1, respectively).
# This applies to each of the 4 attributes height, weight,
# ap_hi and ap_lo.
#
# For each attribute and for each of its possible values,
# we compute the ratio of
# - the frequency of people under consideration with a "cardio problem"
#   having that value for that attribute, with
# - the frequency of people under consideration with "no cardio problem"
#   having that value for that attribute.
# Continuing the previous example:
# - Suppose that there are 100 woman aged 48
#   who have a "cardio problem" and 20 of those are at most 160cm tall.
# - Suppose that there are 150 woman aged 48
#   who have "no cardio problem" and 50 of those are at most 165cm tall.
# Then the ratio for the value "category 1" of the attribute "height"
# is 0.2 / 0.3...3...
#
# We keep only ratios that are strictly greater than 1 and order them
# from largest to smallest.
# A ratio might be infinite (see second sample test).
# In case two ratios are exactly the same, their order is determined
# by the order of the corresponding attributes in the csv file
# (first is height, last is being active or not), and in case the
# attributes are the same, their order is determined by the rank of
# the category (first is 1, last is 5; for booleans, False comes
# before True).
#
# We format ratios with 2 digits after the decimal point.
# After a ratio, the output is one of:
# - Height in category [1-5] (1 lowest, 5 highest)
# - Weight in category [1-5] (1 lowest, 5 highest)
# - Systolic blood pressure in category [1-5] (1 lowest, 5 highest)
# - Diastolic blood pressure in category [1-5] (1 lowest, 5 highest)
# - Cholesterol in category [1-3] (1 lowest, 3 highest)
# - Glucose in category [1-3] (1 lowest, 3 highest)
# - Smoking/Not smoking
# - Drinking/Not drinking
# - Not being active/Being active
#
# You are NOT allowed to use pandas. If you do, then your submission
# will NOT be assessed and you will score 0 to the quiz.

import csv
from collections import defaultdict


def analyse(gender, age):
    # MACROS
    ID=0
    AGE=1
    GENDER=2
    HEIGHT=3
    WEIGHT=4
    APHI=5
    APLO=6
    CHOLESTEROL=7
    GLUC=8
    SMOKE=9
    ALCO=10
    ACTIVE=11
    CARDIO=12
    def checkAge(age,days):
        if((days-1)//365==age):return True
        else:
            return False
    def checkGender(ref,value):
        if(ref=='F' and value==1):
            return True
        elif(ref=='M' and value==2):
            return True
        else: return False
    def checkHeight(height):
        if(height<150 or height>200):return False
        else: return True
    def checkWeight(weight):
        if(weight<50 or weight>150):return False
        else: return True
    def checkAPHI(aphi):
        if(aphi<80 or aphi>200):return False
        else: return True
    def checkAPLO(aplo):
        if(aplo<70 or aplo>140):return False
        else: return True
    def aggregate(feature,shape):
        interval=[0,0]
        if(shape[0]==5):
            interval[0]=cardioBoundries[feature][1]-cardioBoundries[feature][0]/5.0
            interval[1]=noncardioBoundries[feature][1]-noncardioBoundries[feature][0]/5.0
        if(shape[0]<=3):
            interval[0]=interval[1]=1

        pass

    lut={HEIGHT:(5,'Height'),WEIGHT:(5,'Weight'),APHI:(5,'Systolic blood pressure'),APLO:(5,'Diastolic blood pressure'),CHOLESTEROL:(3,'Cholesterol'),GLUC:(3,'Glucose'),SMOKE:(2,'Smoking','Not smoking'),ALCO:(2,'Dringking','Not drinking'),ACTIVE:(2,'Being active','Not being active')}
    cardioBoundries={HEIGHT:[199,150],WEIGHT:[149,50],APHI:[199,80],APLO:[139,70]}
    noncardioBoundries={HEIGHT:[199,150],WEIGHT:[149,50],APHI:[199,80],APLO:[139,70]}
    filename='quiz5/cardio_train.csv'
    fields=[]
    cardio=[]
    noncardio=[]
    result={}
    with open(filename,'r') as csvfile:
        csvreader=csv.reader(csvfile,delimiter=';')
        fields=next(csvreader)
        for row in csvreader:
            for i in range(len(row)):
                if(i==4):row[i]=float(row[i])
                else:row[i]=int(row[i])
            # if(checkAge(age,row[AGE])):
            #     print()
            if(checkAge(age,row[AGE]) and checkGender(gender,row[GENDER]) and checkHeight(row[HEIGHT]) and checkWeight(row[WEIGHT]) and checkAPHI(row[APHI]) and checkAPLO(row[APLO])):
                if(row[CARDIO]==1):boundries=cardioBoundries
                else:boundries=noncardioBoundries
                if(row[WEIGHT]<boundries[WEIGHT][0]):boundries[WEIGHT][0]=row[WEIGHT]
                if(row[WEIGHT]>boundries[WEIGHT][1]):boundries[WEIGHT][1]=row[WEIGHT]
                if(row[HEIGHT]<boundries[HEIGHT][0]):boundries[HEIGHT][0]=row[HEIGHT]
                if(row[HEIGHT]>boundries[HEIGHT][1]):boundries[HEIGHT][1]=row[HEIGHT]
                if(row[APHI]<boundries[APHI][0]):boundries[APHI][0]=row[APHI]
                if(row[APHI]>boundries[APHI][1]):boundries[APHI][1]=row[APHI]
                if(row[APLO]<boundries[APLO][0]):boundries[APLO][0]=row[APLO]
                if(row[APLO]>boundries[APLO][1]):boundries[APLO][1]=row[APLO]
                if(row[CARDIO]==1):cardio.append(row)
                else:noncardio.append(row)
            

    print(fields)
    print(len(cardio), len(noncardio))
    print(cardioBoundries)
    print(noncardioBoundries)



    # pass
    # REPLACE PASS ABOVE WITH YOUR CODE
analyse('F',43)