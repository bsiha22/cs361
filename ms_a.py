import zmq
import json

# Load data from JSON file
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Save data to JSON file
def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# ZeroMQ server
def server(file_path):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        data = load_data(file_path)
        response = None
        request = socket.recv_string()
        request_parts = request.split(',')
        if request_parts[0] == 'keys':
            response_list = []
            for item in data:
                response_list.append(item["name"])
            response = ','.join(response_list)
        elif request_parts[0] == 'get':
            key = request_parts[1]
            for item in data:
                if key == item["name"]:
                    response = json.dumps(item)
                else:
                    continue
            if response is None:
                print(response)
                response = 'Key not found'
        elif request_parts[0] == 'rename':
            old_key = request_parts[2]
            new_key = request_parts[3]
            for item in data[request_parts[1]]:
                if "name" in item and item["name"] == old_key:
                    item["name"] = new_key
                    save_data(file_path, data)
                    response = 'Key renamed'
            if response is None:
                response = 'Key not found'
        else:
            response = 'Invalid request'

        print(response)
        socket.send_string(response)

# Main program
if __name__ == '__main__':
    file_path = 'listdata.json'
    server(file_path)