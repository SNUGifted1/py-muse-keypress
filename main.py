import argparse
import math
import keymodule

from pythonosc import dispatcher
from pythonosc import osc_server

click = 0


def eeg_handler1(unused_addr, args, ch1):
    print("Blink: ", ch1)
    keymodule.PressKey(VK_SPACE)
    keymodule.ReleaseKey(VK_SPACE)
    
def eeg_handler2(unused_addr, args, ch1):
    print("Jaw Clench: ", ch1)
    global click
    if(click==0):
        click=1
        keymodule.ReleaseKey(VK_SPACE)
    else:
        click=0
        keymodule.PressKey(VK_SPACE)
           
if __name__ == "__main__":
    
    click=0
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5001, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/debug", print)
    dispatcher.map("/muse/elements/blink", eeg_handler1, "Blink")
    dispatcher.map("/muse/elements/jaw_clench", eeg_handler2, "Jaw_clench")
    
    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
