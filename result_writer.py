def write_to_file(message, sender_ip, receiver_ip, block):
    """Write the output into a result.txt file"""
    with open("result.txt", "a") as f:
        f.write(f"Processed Message: {message}\n")
        f.write(f"Sender IP: {sender_ip}, Receiver IP: {receiver_ip}\n")
        f.write(f"Blockchain Entry: {block}\n\n")
    print("Result written to result.txt.")
