###############################################################################
# File: uav_frame.py
# Author: Daniel Nybo
# Date: 4/14/2022
# Revision: 1.0
# Description: This file contains the UAVFrame class, which is used to create
#              a frame for the UAV protocol. The frame is a binary message
#              that is sent over the air. The frame is created by the UAV
#              protocol and is used to send data between UAVs and controllers.
#              This is meant to operate as an encryption layer for the UAV
#              protocol, but is not yet implemented as of revision 1.0.
###############################################################################

import numpy as np


class UAVFrame:
    def __init__(self, frame_length, frame_packet,  frame_priority, 
                 frame_source, frame_destination):
        self.frame_length = frame_length
        self.frame_priority = frame_priority
        self.frame_source = frame_source
        self.frame_destination = frame_destination
        self.frame_start = 0x7E
        self.frame_end = 0x7E
        self.frame_packet = frame_packet
        self.frame_packet_encrypted = 0
        self.frame_checksum = self.create_checksum()
        self.frame_message = self.create_message()
    
    # create a method for creating a checksum
    def create_checksum(self):
        self.frame_checksum = self.frame_length + self.frame_packet + \
            self.frame_priority + self.frame_source + self.frame_destination
        return self.frame_checksum
    
    def encrypt(self):
        # encrypt frame_packet with a basic hash/unhash algorithm
        # for now, just XOR with 0x55555555555
        self.frame_packet_encrypted = self.frame_packet ^ 0x55555555555
        return self.frame_packet_encrypted
    
    def decrypt(self, frame_packet_encrypted=None):
        # decrypt frame_packet with a basic hash/unhash algorithm
        # for now, just XOR with 0x55555555555
        self.frame_packet = self.frame_packet_encrypted ^ 0x55555555555
        return self.frame_packet
    
    # create a method for creating a binary message of the frame
    def create_message(self):
        # convert each frame element to binary and concatenate
        self.frame_message = np.concatenate((np.binary_repr(self.frame_start, width=8),
                                                np.binary_repr(self.frame_length, width=8),
                                                self.frame_packet_encrypted,
                                                np.binary_repr(self.frame_priority, width=8),
                                                np.binary_repr(self.frame_source, width=8),
                                                np.binary_repr(self.frame_destination, width=8),
                                                np.binary_repr(self.frame_checksum, width=8),
                                                np.binary_repr(self.frame_end, width=8)))
        return self.frame_message
    

    

    


    
    

        


