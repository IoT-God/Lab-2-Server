import socket
import picar_4wd as fc
import json

HOST = "10.0.0.7" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
power_val = 50
distance = 0
direction = "forward"

def pack_data():
    json_data = {
        "cpu_temp": fc.cpu_temperature(),
        "power": fc.power_read(),
        "distance": distance,
        "direction": direction
    }
    return json_data
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        client, clientInfo = s.accept()
        print("server recv from: ", clientInfo)
        while 1:
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                data = data.strip()
                print("server recv data: ", data)
            else:
                continue
            
            if data == b"87":
                # w
                fc.forward(power_val)
                direction = "forward"
                distance += 1
            elif data == b"83":
                # s
                fc.backward(power_val)
                direction = "backward"
                distance += 1
            elif data == b"65":
                # a
                fc.turn_left(power_val)
                direction = "left"
            elif data == b"68":
                # d
                fc.turn_right(power_val)
                direction = "right"
            elif data == b"0":
                fc.stop()

            data = pack_data()
            client.send(json.dumps(data).encode("utf-8"))
            print(data)
    except Exception as e:
        print("Error: ", e)
        client.close()
    except:
        print("Closing socket")
        client.close()
        s.close()    