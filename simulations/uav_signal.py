import numpy as np
import matplotlib.pyplot as plt

# create a class which generates a signal given a message and a PN code
class UAVSignal:
    def __init__(self, message, pn_code, Fs, fc, fp, bit_t):
        self.message = message
        self.original_message = message
        self.message[self.message == 0] = -1 # convert 0 to -1 for DSSS encoding
        self.message = np.tile(self.message, (fp,1))  # scale and reshape the messages to be the same length
        self.message = self.message.T.reshape(1, self.message.size)[0]
        self.pn_code = pn_code
        self.pn_code[self.pn_code == 0] = -1
        self.Fs = Fs
        self.fc = fc
        self.fp = fp
        self.bit_t = bit_t
        self.t = np.arange(0, (bit_t-1/Fs), 1/1000)
        self.s0 = np.sin(2 * np.pi * fc * self.t)
        self.s1 = -1 * np.sin(2 * np.pi * fc * self.t)
        self.carrier = np.array([])
        self.BPSK = np.array([])
        self.DSSS = self.message * self.pn_code
        self.rx = np.array([])
        self.demod = np.array([])
        self.result = np.array([])
        self.result_wrong = np.array([])
        self.rx2 = np.array([])
        self.demod2 = np.array([])
        self.pn_code_wrong = np.random.randint(0, 2, size=len(self.message)*self.fp)
        self.pn_code_wrong[self.pn_code_wrong == 0] = -1

        
    def modulate(self):
        for i in range(len(self.DSSS)):
            if self.DSSS[i] == 1:
                self.BPSK = np.concatenate((self.BPSK, self.s1))
            elif self.DSSS[i] == -1:
                self.BPSK = np.concatenate((self.BPSK, self.s0))
            self.carrier = np.concatenate((self.carrier, self.s1))
 
    def demodulate(self):
        for i in range(len(self.pn_code)):
            if self.pn_code[i] == 1:
                self.rx = np.concatenate((self.rx, self.BPSK[(i*len(self.t)):((i+1)*len(self.t))]))
            else:
                self.rx = np.concatenate((self.rx, -1 * self.BPSK[(i*len(self.t)):((i+1)*len(self.t))]))
        
        self.demod = self.rx * self.carrier

        for i in range(int(len(self.message)/self.fp)):
            x = len(self.t) * self.fp
            cx = np.sum(self.carrier[(i*x):(i+1)*x] * self.demod[(i*x):(i+1)*x])
            if cx > 0:
                self.result = np.concatenate((self.result, [1]))
            else:
                self.result = np.concatenate((self.result, [-1]))
    
    def demodulate_with(self, pn_code):
        return 0
    
    def demodulate_wrong(self):
        for i in range(len(self.pn_code_wrong)):
            if self.pn_code_wrong[i] == 1:
                self.rx2 = np.concatenate((self.rx2, self.BPSK[(i*len(self.t)):((i+1)*len(self.t))]))
            else:
                self.rx2 = np.concatenate((self.rx2, -1 * self.BPSK[(i*len(self.t)):((i+1)*len(self.t))]))
        
        self.demod2 = self.rx2 * self.carrier
        
        for i in range(int(len(self.message)/self.fp)):
            x = len(self.t) * self.fp
            cx = np.sum(self.carrier[(i*x):(i+1)*x] * self.demod2[(i*x):(i+1)*x])
            if cx > 0:
                self.result_wrong = np.concatenate((self.result_wrong, [1]))
            else:
                self.result_wrong = np.concatenate((self.result_wrong, [-1]))
    
        
    def plot(self):
        plt.figure(figsize=(8, 6))
        if len(self.result_wrong) > 0:
            plt.subplot(3, 1, 1)
        else:
            plt.subplot(2, 1, 1)
        plt.plot(range(len(self.original_message)), self.original_message, '-o', label='Original message')
        plt.xlabel('Bit index')
        plt.ylabel('Bit value')
        plt.title('DSSS modulation and demodulation')
        plt.legend()
        if len(self.result_wrong) > 0:
            plt.subplot(3, 1, 2)
        else:
            plt.subplot(2, 1, 2)
        plt.plot(range(len(self.result)), self.result, '-o', label='Demodulated message')
        plt.xlabel('Bit index')
        plt.ylabel('Bit value')
        plt.legend()
        if len(self.result_wrong) > 0:
            plt.subplot(3, 1, 3)
            plt.plot(range(len(self.result_wrong)), self.result_wrong, '-o', label='Demodulated message with wrong PN code')
            plt.xlabel('Bit index')
            plt.ylabel('Bit value')
            plt.legend()
        # plt.show()

# this function takes two independent signals on the same frequency and length 
# and returns a combined signal to be transmitted  
@staticmethod
def combine_signals(signal1, signal2):
    return signal1 + signal2

# this function demodulates a BPSK DSSS signal given a PN code
# and returns the demodulated signal
# the function assumes that the PN code is the same as the one used to modulate the signal
 

# this function adds noise to a signal given an SNR
@staticmethod
def add_noise(signal, SNR):
    signal_power = np.sum(np.abs(signal)**2) / len(signal)
    noise_power = signal_power / (10**(SNR/10))
    noise = np.random.normal(0, np.sqrt(noise_power), len(signal))
    return signal + noise

# this function takes a signal and returns the plot of its FFT
@staticmethod
def plotfft(signal, title='FFT'):
    plt.figure()
    plt.plot(np.abs(np.fft.fft(signal)))
    plt.title(title)
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')

# Plots the PSD of a signal
@staticmethod
def plotpsd(signal, title='PSD'):
    plt.figure()
    plt.psd(signal, Fs=1)
    plt.title(title)
    plt.xlabel('Frequency')
    plt.ylabel('PSD')

# plots the constellation diagram of a BPSK signal
@staticmethod
def plot_constellation(signal, title='Constellation'):
    plt.figure()
    plt.plot(signal.real, signal.imag, 'o')
    plt.title(title)
    plt.xlabel('Real')
    plt.ylabel('Imaginary')

# this function takes a signal and returns the BER between the original message and the demodulated message
@staticmethod
def calculate_BER(original_message, demodulated_message):
    return np.sum(np.abs(original_message - demodulated_message)) / len(original_message)



