###############################################################################
# File: uav_packet.py
# Author: Daniel Nybo
# Date: 4/14/2022
# Revision: 2.0
# Description: A class for creating a packet for the UAV to send to the control
# station and vice versa.
# This class also contains a method for creating a binary message from the packet
# and a method for creating a pseudo-random binary sequence (PN code) of a specified
# length using the ID of the UAV and the ID of the control station.
###############################################################################

import numpy as np
from prettytable import PrettyTable

class UAVPacket:
    '''A class for creating a packet for the UAV to send to the control station
    and vice versa.
    
    The packet is a 12 byte message with the following format:
    
    Parameters
    ----------
    UAV_ID: 8 bits
    CONTROL_ID: 8 bits
    UAV_RECIEVER_STATUS: 8 bits
    UAV_TRANSMITTER_STATUS: 8 bits
    CONTROL_RECIEVER_STATUS: 8 bits
    CONTROL_TRANSMITTER_STATUS: 8 bits
    CHANGE_X: 8 bits
    CHANGE_Y: 8 bits
    CHANGE_Z: 8 bits
    CHANGE_PITCH: 8 bits
    CHANGE_ROLL: 8 bits
    CHANGE_YAW: 8 bits
    
    Methods
    -------
    get_message()
        Convert the packet to a binary message.
    get_pn_code()
        Generate a pseudo-random binary sequence (PN code) of length 12 bytes using 
        the ID of the UAV and the ID of the control station.
    print_tx_frame()
        Print the packet.
    print_rx_frame()
        Print the packet.
    compare()
        Compare the packet to another packet.
    '''
    def __init__(self, UAV_ID = 1, CONTROL_ID = 1, UAV_RECIEVER_STATUS = 0, UAV_TRANSMITTER_STATUS = 0, CONTROL_RECIEVER_STATUS = 0, CONTROL_TRANSMITTER_STATUS = 0, CHANGE_X = 0, CHANGE_Y = 0, CHANGE_Z = 0, CHANGE_PITCH = 0, CHANGE_ROLL = 0, CHANGE_YAW = 0):
        '''Initialize the packet with default values of 0 for all fields except for the UAV_ID and CONTROL_ID fields, which are initialized to 1.'''
        self.UAV_ID = UAV_ID
        self.CONTROL_ID = CONTROL_ID
        self.UAV_RECIEVER_STATUS = UAV_RECIEVER_STATUS
        self.UAV_TRANSMITTER_STATUS = UAV_TRANSMITTER_STATUS
        self.CONTROL_RECIEVER_STATUS = CONTROL_RECIEVER_STATUS
        self.CONTROL_TRANSMITTER_STATUS = CONTROL_TRANSMITTER_STATUS
        self.CHANGE_X = CHANGE_X
        self.CHANGE_Y = CHANGE_Y
        self.CHANGE_Z = CHANGE_Z
        self.CHANGE_PITCH = CHANGE_PITCH
        self.CHANGE_ROLL = CHANGE_ROLL
        self.CHANGE_YAW = CHANGE_YAW

    def get_message(self):
        '''Convert the packet to a binary message.
        return: a binary message of length 12 bytes.'''
        UAV_ID = np.binary_repr(self.UAV_ID, width=8)
        CONTROL_ID = np.binary_repr(self.CONTROL_ID, width=8)
        UAV_RECIEVER_STATUS = np.binary_repr(self.UAV_RECIEVER_STATUS, width=8)
        UAV_TRANSMITTER_STATUS = np.binary_repr(self.UAV_TRANSMITTER_STATUS, width=8)
        CONTROL_RECIEVER_STATUS = np.binary_repr(self.CONTROL_RECIEVER_STATUS, width=8)
        CONTROL_TRANSMITTER_STATUS = np.binary_repr(self.CONTROL_TRANSMITTER_STATUS, width=8)

        CHANGE_X = np.binary_repr(self.CHANGE_X, width=8)
        CHANGE_Y = np.binary_repr(self.CHANGE_Y, width=8)
        CHANGE_Z = np.binary_repr(self.CHANGE_Z, width=8)

        CHANGE_PITCH = np.binary_repr(self.CHANGE_PITCH, width=8)
        CHANGE_ROLL = np.binary_repr(self.CHANGE_ROLL, width=8)
        CHANGE_YAW = np.binary_repr(self.CHANGE_YAW, width=8)
        message = UAV_ID + CONTROL_ID + UAV_RECIEVER_STATUS + UAV_TRANSMITTER_STATUS + CONTROL_RECIEVER_STATUS + CONTROL_TRANSMITTER_STATUS + CHANGE_X + CHANGE_Y + CHANGE_Z + CHANGE_PITCH + CHANGE_ROLL + CHANGE_YAW
        MESSAGE = [int(x) for x in message]
        return np.array(MESSAGE)
    
    def get_pn_code(self, mbits = 4):
        '''Create a m-bit pseudo-noise code using the UAV_ID and CONTROL_ID.
        return: a m-bit pseudo-noise code.'''
        # take the two ID's and create an m-bit code
        code = self.UAV_ID ^ self.CONTROL_ID * 200
        code = np.binary_repr(code, width=mbits)
        code = [int(x) for x in code[0:mbits]]
        return np.array(code)
    
    def print_tx_frame(self):
        '''Print the packet in a table format.
        return: a table with the packet fields and their values.'''
        print("UAV ID: ", self.UAV_ID)
        print("CONTROL ID: ", self.CONTROL_ID)
        print("UAV RECIEVER STATUS: ", self.UAV_RECIEVER_STATUS)
        print("UAV TRANSMITTER STATUS: ", self.UAV_TRANSMITTER_STATUS)
        print("CONTROL RECIEVER STATUS: ", self.CONTROL_RECIEVER_STATUS)
        print("CONTROL TRANSMITTER STATUS: ", self.CONTROL_TRANSMITTER_STATUS)
        print("CHANGE X: ", self.CHANGE_X)
        print("CHANGE Y: ", self.CHANGE_Y)
        print("CHANGE Z: ", self.CHANGE_Z)
        print("CHANGE PITCH: ", self.CHANGE_PITCH)
        print("CHANGE ROLL: ", self.CHANGE_ROLL)
        print("CHANGE YAW: ", self.CHANGE_YAW)

    def print_rx_frame(self,result):
        '''Print the packet in a table format.'''
        result = result.astype(int)
        result[result==-1] = 0
        # change the result from binary to decimal
        result = np.array([int(''.join(map(str, result[i:i+8])), 2) for i in range(0, len(result), 8)])
        # values are 2's complement, so convert to signed
        result = np.array([result[i] - 256 if result[i] > 127 else result[i] for i in range(len(result))])

        print("UAV ID: ", result[0])
        print("CONTROL ID: ", result[1])
        print("UAV RECIEVER STATUS: ", result[2])
        print("UAV TRANSMITTER STATUS: ", result[3])
        print("CONTROL RECIEVER STATUS: ", result[4])
        print("CONTROL TRANSMITTER STATUS: ", result[5])
        print("CHANGE X: ", result[6])
        print("CHANGE Y: ", result[7])
        print("CHANGE Z: ", result[8])
        print("CHANGE PITCH: ", result[9])
        print("CHANGE ROLL: ", result[10])
        print("CHANGE YAW: ", result[11])

    # create a function which makes a table and prints it comparing the received message to the sent message
    def compare(self, result, printTable=False):
        '''Compare the sent and received messages.
        Parameters:
            result: the received of the packet to compare to the sent message.
        return: bool
            return True if the sent and received messages are the same.'''
        result = result.astype(int)
        result[result==-1] = 0
        # change the result from binary to decimal
        result = np.array([int(''.join(map(str, result[i:i+8])), 2) for i in range(0, len(result), 8)])
        # values are 2's complement, so convert to signed
        result = np.array([result[i] - 256 if result[i] > 127 else result[i] for i in range(len(result))])
        if printTable:
            # create a table to compare the sent and received messages
            table = PrettyTable()
            table.field_names = ["","Sent", "Received"]
            # for each table row add the sent and received values
            table.add_row(["UAV ID", self.UAV_ID, result[0]])
            table.add_row(["CONTROL ID", self.CONTROL_ID, result[1]])
            table.add_row(["UAV RECIEVER STATUS", self.UAV_RECIEVER_STATUS, result[2]])
            table.add_row(["UAV TRANSMITTER STATUS", self.UAV_TRANSMITTER_STATUS, result[3]])
            table.add_row(["CONTROL RECIEVER STATUS", self.CONTROL_RECIEVER_STATUS, result[4]])
            table.add_row(["CONTROL TRANSMITTER STATUS", self.CONTROL_TRANSMITTER_STATUS, result[5]])
            table.add_row(["CHANGE X", self.CHANGE_X, result[6]])
            table.add_row(["CHANGE Y", self.CHANGE_Y, result[7]])
            table.add_row(["CHANGE Z", self.CHANGE_Z, result[8]])
            table.add_row(["CHANGE PITCH", self.CHANGE_PITCH, result[9]])
            table.add_row(["CHANGE ROLL", self.CHANGE_ROLL, result[10]])
            table.add_row(["CHANGE YAW", self.CHANGE_YAW, result[11]])
            print(table)

        if(self.UAV_ID == result[0] and self.CONTROL_ID == result[1] and self.UAV_RECIEVER_STATUS == result[2] and self.UAV_TRANSMITTER_STATUS == result[3] and self.CONTROL_RECIEVER_STATUS == result[4] and self.CONTROL_TRANSMITTER_STATUS == result[5] and self.CHANGE_X == result[6] and self.CHANGE_Y == result[7] and self.CHANGE_Z == result[8] and self.CHANGE_PITCH == result[9] and self.CHANGE_ROLL == result[10] and self.CHANGE_YAW == result[11]):
            return True
        else:
            return False
        
# class for a text frame
class TextPacket(UAVPacket):
    '''A class for a text frame. Inherits from the UAVPacket class.
    Attributes:
        TEXT (str): the text to be sent.
    '''
    def __init__(self, UAV_ID = 1, CONTROL_ID = 1, UAV_RECIEVER_STATUS = 0, UAV_TRANSMITTER_STATUS = 0, CONTROL_RECIEVER_STATUS = 0, CONTROL_TRANSMITTER_STATUS = 0, CHANGE_X = 0, CHANGE_Y = 0, CHANGE_Z = 0, CHANGE_PITCH = 0, CHANGE_ROLL = 0, CHANGE_YAW = 0, TEXT = ''):
        '''Constructor for the TextPacket class.'''
        super().__init__(UAV_ID, CONTROL_ID, UAV_RECIEVER_STATUS, UAV_TRANSMITTER_STATUS, CONTROL_RECIEVER_STATUS, CONTROL_TRANSMITTER_STATUS, CHANGE_X, CHANGE_Y, CHANGE_Z, CHANGE_PITCH, CHANGE_ROLL, CHANGE_YAW)
        self.TEXT = TEXT

    def get_message(self):
        '''Get the message to be sent.'''
        # get the message from the parent class
        message = super().get_message()
        # convert the text to ascii
        text = ''.join(format(ord(x), '08b') for x in self.TEXT)
        # now add the text to the message as array elements of 1 bit 
        message = np.append(message, np.array([int(x) for x in text]))

        return message

    def print_tx_frame(self):
        '''Print the message to be sent.'''
        super().print_tx_frame()
        print("TEXT: ", self.TEXT)

    def print_rx_frame(self, result):
        '''Print the received message.'''
        super().print_rx_frame(result)
        # get the result from the parent class and convert bytes 12- to text
        result = result.astype(int)
        result[result==-1] = 0
        # change the result from binary to decimal
        result = np.array([int(''.join(map(str, result[i:i+8])), 2) for i in range(0, len(result), 8)])
        # values are 2's complement, so convert to signed
        result = np.array([result[i] - 256 if result[i] > 127 else result[i] for i in range(len(result))])
        # convert the text to binary
        text = ''.join(format(i, '08b') for i in result[12:])
        # convert the text to ascii
        text = ''.join(chr(int(text[i:i+8], 2)) for i in range(0, len(text), 8))
        print("TEXT: ", text)

    def compare(self, result, printTable = False):
        '''Compare the sent and received messages.'''
        super().compare(result)
        # get the result from the parent class and convert bytes 12- to text
        result = result.astype(int)
        result[result==-1] = 0
        # change the result from binary to decimal
        result = np.array([int(''.join(map(str, result[i:i+8])), 2) for i in range(0, len(result), 8)])
        # values are 2's complement, so convert to signed
        result = np.array([result[i] - 256 if result[i] > 127 else result[i] for i in range(len(result))])
        
        if printTable:
            # convert the text to binary
            text = ''.join(format(i, '08b') for i in result[12:])
            # convert the text to ascii
            text = ''.join(chr(int(text[i:i+8], 2)) for i in range(0, len(text), 8))
            # create a table to compare the sent and received messages
            table = PrettyTable()
            table.field_names = ["","Sent", "Received"]
            # for each table row add the sent and received values
            table.add_row(["UAV ID", self.UAV_ID, result[0]])
            table.add_row(["CONTROL ID", self.CONTROL_ID, result[1]])
            table.add_row(["UAV RECIEVER STATUS", self.UAV_RECIEVER_STATUS, result[2]])
            table.add_row(["UAV TRANSMITTER STATUS", self.UAV_TRANSMITTER_STATUS, result[3]])
            table.add_row(["CONTROL RECIEVER STATUS", self.CONTROL_RECIEVER_STATUS, result[4]])
            table.add_row(["CONTROL TRANSMITTER STATUS", self.CONTROL_TRANSMITTER_STATUS, result[5]])
            table.add_row(["CHANGE X", self.CHANGE_X, result[6]])
            table.add_row(["CHANGE Y", self.CHANGE_Y, result[7]])
            table.add_row(["CHANGE Z", self.CHANGE_Z, result[8]])
            table.add_row(["CHANGE PITCH", self.CHANGE_PITCH, result[9]])
            table.add_row(["CHANGE ROLL", self.CHANGE_ROLL, result[10]])
            table.add_row(["CHANGE YAW", self.CHANGE_YAW, result[11]])
            table.add_row(["TEXT", self.TEXT, text])
            print(table)
        if(self.UAV_ID == result[0] and self.CONTROL_ID == result[1] and self.UAV_RECIEVER_STATUS == result[2] and self.UAV_TRANSMITTER_STATUS == result[3] and self.CONTROL_RECIEVER_STATUS == result[4] and self.CONTROL_TRANSMITTER_STATUS == result[5] and self.CHANGE_X == result[6] and self.CHANGE_Y == result[7] and self.CHANGE_Z == result[8] and self.CHANGE_PITCH == result[9] and self.CHANGE_ROLL == result[10] and self.CHANGE_YAW == result[11] and self.TEXT == text):
            return True
        else:
            return False





    