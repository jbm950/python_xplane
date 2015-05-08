#-------------------------------------------------------------------------------
# Name:        python_xplane_interface.py
# Purpose:     This module will allow easy communication between python code
#              and the xplane software.
#
# Author:      James
#
# Created:     03/01/2015
# Copyright:   (c) James 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import socket, time, struct

class Xplane_connection:
    def __init__(self,xplane_ip_addr,xplane_port,recieve_port):
        """This will take care of all interactions that you will need between
        python and simulink.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Inputs:
            xplane_ip_addr - This is a string of the ip address of the computer
                that xplane is being run on.

            xplane_port - This is the port that xplane is listening to for
                recieving data.

            recieve_port - This is the port that your code will listen to for
                data from xplane.

            (Make sure the ports match what xplane has set in its net
             connections menu)
        """

        # Set up the sockets for sending and recieving data from xplane
        # x for xplane h for host
        self.xUDP_IP = xplane_ip_addr
        self.xUDP_PORT = xplane_port
        self.xsock = socket.socket(socket.AF_INET, # Internet
                                   socket.SOCK_DGRAM) # UDP

        self.hUDP_IP = socket.gethostbyname(socket.gethostname())
        self.hUDP_PORT = recieve_port
        self.hsock = socket.socket(socket.AF_INET, # Internet
                              socket.SOCK_DGRAM) # UDP
        self.hsock.bind((self.hUDP_IP, self.hUDP_PORT))

    def recieve(self):
        """ This method will pass the data that was sent from xplane.
        format (data,first_item)"""

        # Recieve data from xplane and return both the raw data and the unpacked
        # first item
        data = self.hsock.recv(1024)
        first_item = struct.unpack_from('<f',data,9)[0]

        return (data,first_item)

    def send(self,message):
        """This method will send data to xplane.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Inputs:
            message - This is the byte string of data to be sent to xplane. It
                will start with an integer defining which type of data you are
                sending followed by the floating point data.
        """

        # Initialize the tag identifing the message as data and append it to the
        # front of the byte string message.
        data_tag = b'DATA@'
        message = data_tag + message

        # Send the data to the computer running xplane
        self.xsock.sendto(message, (self.xUDP_IP, self.xUDP_PORT))

    def level_flight(self):
        """Not Currently Working. If paused it will the euler angles will go to zero
           but as soon as it is unpaused it will return to initial position"""

        # Initialize the message setting the euler angles to zero and send to
        # xplane
        message = b'DATA@\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.xsock.sendto(message, (self.xUDP_IP, self.xUDP_PORT))

# Self Test Code
#   NOTE: The ip address and ports need to be changed to match your current
#   setup.

if __name__ == '__main__':

    # Initialize the connection
    xp_inter = Xplane_connection('128.206.20.1',49000,49001)

    # Test Sending a Message
    throt_command = struct.pack('ifxxxxxxxxxxxxxxxxxxxxxxxxxxxx',25,0.5)
    print(throt_command)
    xp_inter.send(throt_command)

##    # Test level flight command (Not working)
##    start = time.time()
##    while start + 10 > time.time():
##        xp_inter.level_flight()

    # Test Recieving a Message
    print(xp_inter.recieve())


