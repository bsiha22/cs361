import zmq
import json

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def server(filename):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:6666")

    while True:
        data = load_data(filename)
        message = socket.recv_string()
        messages = message.split(',')
        response = None

        if messages[0] == "name":
            sortlist = sorted(data[messages[1]], key=lambda item: item['name'])
            data[messages[1]] = sortlist
            save_data(filename, data)
            response = (f'{messages[1]} was sorted by name.')

        elif messages[0] == "price":
            sortlist = sorted(data[messages[1]], key=lambda item: item['price'])
            data[messages[1]] = sortlist
            save_data(filename, data)
            response = (f'{messages[1]} was sorted by price.')
        
        if response is None:
            response = 'There was an error sorting'
        
        print(response)
        socket.send_string(response)


if __name__ == "__main__":
    server('listdata.json')


        
