import zmq

def recs():

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:4444")

    while True:
        message = socket.recv_string()
        response = None

        if message == 'fruits':
            response = "Commonly bought fruits are: Apples, Avocados, Bananas, Grapes, Oranges, and Strawberries."

        if message == 'vegetables':
            response = "Commonly bought vegetables are: Carrots, Kale, Lettuce, Mushrooms, Potatos, and Tomatoes."
        
        if message == 'household':
            response = "Common household items are: Hand Soap, Lotion, Paper Towels, Tissues, Toilet Paper and Water."

        if message == 'smoothie':
            response = "Common smoothie addins: Bananas, Frozen Berries, Milk, Peanut Butter, Protein Powder, and Yogurt."

