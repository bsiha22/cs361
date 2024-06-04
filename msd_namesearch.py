import json
import zmq

def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def namesearch(filename):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:3333")

    while True:

        message = socket.recv_string()
        data = load_data(filename)
        name = message.strip()
        found = []

        for lists, items in data.items():
            for item in items:
                if item['name'].lower() == name.lower():
                    found.append((lists, item))
                    break

        if found:
            info = [f"{name} was found in the following lists:"]
            for lists, item in found:
                info.append(f"\nList: {lists}")
                info.append(f"  Price: {item['price']}")
                info.append(f"  Store: {item['store']}")
                info.append(f"  Restrictions: {item['limits']}")
            response = "\n".join(info)
        
        else:
            response = f"{name} wasn't found in any of your lists."

        print("Response was sent.")
        socket.send_string(response)


if __name__ == "__main__":
    namesearch('listdata.json')