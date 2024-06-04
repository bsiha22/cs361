import zmq

def recs():

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:4444")

    while True:
        message = socket.recv_string()
        response = None

        if message == '1':
            response = "Commonly bought fruits: Apples, Avocados, Bananas, Grapes, Oranges, and Strawberries."

        elif message == '2':
            response = "Commonly bought vegetables: Carrots, Kale, Lettuce, Mushrooms, Potatos, and Tomatoes."
        
        elif message == '4':
            response = "Common household items: Hand Soap, Lotion, Paper Towels, Tissues, Toilet Paper and Trash Bags"

        elif message == '5':
            response = "Common smoothie addins: Bananas, Frozen Berries, Milk, Peanut Butter, Protein Powder, and Yogurt."

        elif message == '3':
            response = "Popular Sweets: Brownies, Cakes, Cookies, Donuts, Ice Cream, and Pies."

        if response is None:
            response = 'Invalid entry.'

        print(response)
        socket.send_string(response)


if __name__ == "__main__":
    recs()

