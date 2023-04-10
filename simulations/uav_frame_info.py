import numpy as np

# create a class which holds all these data fields 
# and updates the current message
class UAVFrame:
    def __init__(self, UAV_ID, CONTROL_ID, UAV_RECIEVER_STATUS, UAV_TRANSMITTER_STATUS, CONTROL_RECIEVER_STATUS, CONTROL_TRANSMITTER_STATUS, CHANGE_X, CHANGE_Y, CHANGE_Z, CHANGE_PITCH, CHANGE_ROLL, CHANGE_YAW):
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

    def update(self, UAV_ID, CONTROL_ID, UAV_RECIEVER_STATUS, UAV_TRANSMITTER_STATUS, CONTROL_RECIEVER_STATUS, CONTROL_TRANSMITTER_STATUS, CHANGE_X, CHANGE_Y, CHANGE_Z, CHANGE_PITCH, CHANGE_ROLL, CHANGE_YAW):
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
    
    def print_tx_frame(self):
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




    