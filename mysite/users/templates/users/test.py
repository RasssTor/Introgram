person_count = input("Число работников")
web_server = int(input("Web_server - "))
db_server = int(input("bd_server"))
ip_tel = int(input("count ip tel - "))
camera = int(input("camera"))
result = person_count*(web_server*4096 + web_server*6144+db_server*2048 + db_server*4096)/60 + 0.08*ip_tel+8192*camera
print(result)



input()