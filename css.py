print('started server')

map = "bosta"
while True:
    inp = input("Enter input: ")

    if inp == "close":
        break
    elif inp == "ping":
        print("pong")
    elif "changelevel" == inp.split(" ")[0] and len(inp.split(' ')) == 2:
        print(f"changed map from {map} to {inp.split(' ')[1]}")
        map = inp.split(' ')[1]
    else:
        print("bad command")
