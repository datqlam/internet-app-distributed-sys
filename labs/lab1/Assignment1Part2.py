# Assignment 1: Part 2
# GROUP 43:
# Lalitha Devi Pulagam	105159977
# Nikhitha Inturi		110008508
# Quoc Dat Lam		    105190512

fit_items = ['treadmill', 'lifting bars', 'exercise bikes', 'weights', 'rigs', 'dumbbells', 'gym mats', 'steppers',
             'exercise balls', 'rowing machine', 'bands & tubing', 'home gym']

f = open('catalog.txt')
# read all contents of the file at once
# readlines() does not strip the newline character when splitting the contents into a list
contents = f.read()
file_as_list = contents.splitlines()

# item category dict
d1 = {}
# item quantity dict
d2 = {}
# assume there are no duplicated fit items in catalog.txt
# for each item in fit_items list, find its category and quantity in file_as_list
# build two dicts d1 and d2 for category and quantity respectively
for item in fit_items:
    if item in file_as_list:
        item_index = file_as_list.index(item)
        item_category = file_as_list[item_index + 1]
        item_quantity = file_as_list[item_index + 2]
        d1.update({item: item_category})
        d2.update({item: item_quantity})

print(d1)
print(d2)

while True:
    try:
        s = input("Please enter a fitness item:\n").lower()
        print(d1[s])
        print(d2[s])
    except KeyError:
        # if key not found in dicts, then KeyError is thrown
        # continue to ask users to key in correct items
        print("Invalid Key")
        continue
    except EOFError:
        # Ctrl + D is pressed
        print("Exit")
        break

    # Ask for another search
    opt = input("Another search?(yes/no)\n")
    if opt == 'yes':
        continue
    else:
        break
