from random import seed
from random import randint
 
ips = list()

number_of_ip_addresses = int(input("Enter the number of IP addresses you want to generate: "))
output = input("Name the output file(without extension): ")

counter = 0
while counter < number_of_ip_addresses:
    number_of_class_A_ips = randint(0,255)
    while number_of_class_A_ips > number_of_ip_addresses:
        number_of_class_A_ips = randint(0,255)
    first_part = randint(0,255)
    print('A: ' + str(number_of_class_A_ips) + '-' + str(first_part))
    for x in range(number_of_class_A_ips):

        number_of_class_B_ips = randint(0,255)
        while number_of_class_B_ips > number_of_ip_addresses+number_of_class_A_ips:
            number_of_class_A_ips = randint(0,255)

        second_part = randint(0,255)
        print('B: ' + str(number_of_class_B_ips) + '-' + str(second_part))
        for y in range(number_of_class_B_ips):
            third_part = randint(0,255)
            forth_part = randint(0,255)
            ip = str(first_part) + '.' + str(second_part) + '.' + str(third_part) + '.' + str(forth_part)
            ips.append(ip)
            counter = counter + 1

with open(output  + '.txt', 'w') as f:
    for items in ips:
        f.write("%s\n" % items)
