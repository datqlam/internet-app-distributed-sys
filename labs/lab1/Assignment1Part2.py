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
        print("Invalid Key")
        continue
    except EOFError:
        print("Exit")
        break

    opt = input("Another search?(yes/no)\n")
    if opt == 'yes':
        continue
    else:
        break
