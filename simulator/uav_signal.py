###############################################################################
# File: uav_signal.py
# Author: Daniel Nybo
# Date: 4/14/2022
# Revision: 2.0
# Description: This file contains the UAVSignal class. The purpose of this class
# is to encode and modulate a BPSK Binary Phase-shift Keying signal given a
# message and a PN code for DSSS encoding. The class also demodulates the 
# signal and decodes the message. The class enables the simulation of the
# signal transmission and reception between a UAV and a ground station given 
# noise conditions and the presence of other signals on the channel. It also
# provides visualization of the signals and the messages.
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


class UAVSignal:
    '''UAVSignal class encodes and modulates a BPSK Binary Phase-shift 
        Keying signal given a message and a PN code for DSSS encoding.
        The class also demodulates the signal and decodes the message.
        The class can be used to simulate the signal transmission and
        reception between a UAV and a ground station.
        
        Parameters
        ----------
        message : ndarray
            The message to be encoded and modulated. The message is a list
            of 0s and 1s.
        pn_code : ndarray
            The PN pseudo-random code to be used for DSSS encoding. The PN code 
            is a list of 0s and 1s.
        Fs : float
            The sampling frequency of the signal. The default is 2.4e9.
        fc : float
            The carrier frequency of the signal.
        fp : int
            number of bits in the PN code for DSSS encoding.  
        bit_t : float
            period for a symbol in the message. The default is .01.


        Attributes(other than parameters)
        ----------
        original_message : ndarray
            The original message before encoding and modulation.
        BPSK : ndarray
            The BPSK modulated signal.
        DSSS : ndarray
            The DSSS encoded signal.
        rx : ndarray
            The received signal after demodulation.
        demod : ndarray
            The demodulated signal.
        result : ndarray
            The decoded message.

        Methods 
        -------
        set_pn_code(pn_code)
            Sets the PN code for DSSS encoding.
        encode()
            Encodes the message using DSSS encoding.
        modulate()
            Modulates the DSSS encoded signal.
        demodulate()
            Demodulates the received signal.
        decode()
            Decodes the demodulated signal.
        plot()
            Plots the original message, the encoded message, the modulated signal,
            the demodulated signal, and the decoded message.
        plot_constellation()
            Plots the constellation diagram of the modulated signal.
        '''

    def __init__(self, message=[0, 1, 0, 1], pn_code=[1,0,0,1], Fs=2.4e9, fc=100, fp=4, bit_t=.01):
        '''Initializes the UAVSignal class.'''
        self.message = message
        self.pn_code = self.set_pn_code(pn_code)
        self.original_message = message
        self.message[self.message == 0] = -1 # convert 0 to -1 for DSSS encoding
        self.message = np.tile(self.message, (fp,1))  # scale and reshape the message for DSSS encoding
        self.message = self.message.T.reshape(1, self.message.size)[0]
        self.pn_code[self.pn_code == 0] = -1
        self.Fs = Fs
        self.fc = fc
        self.fp = fp
        self.bit_t = bit_t
        self.t = np.arange(0, (bit_t-1/Fs), 1/1000)
        self.s0 = -1*np.sin(2 * np.pi * fc * self.t)
        self.s1 = np.sin(2 * np.pi * fc * self.t)
        self.carrier = np.array([])
        self.BPSK = np.array([])
        self.DSSS = self.message * self.pn_code
        self.rx = np.array([])
        self.demod = np.array([])
        self.result = np.array([])
        self.result_wrong = np.array([])
        self.rx2 = np.array([])
        self.demod2 = np.array([])
        self.pn_code_wrong = np.random.randint(0, 2, size=len(self.pn_code))
        self.pn_code_wrong[self.pn_code_wrong == 0] = -1

    def set_pn_code(self, pn_code=None):
        '''Sets the PN code for DSSS encoding.
            pn_code : ndarray
                The PN pseudo-random code to be used for DSSS encoding. The PN code
                is a list of 0s and 1s.
            Returns
            -------
            codearray : ndarray'''
        codearray = np.array([])
        for i in range(len(self.message)):
            codearray = np.concatenate((codearray, pn_code))
        self.pn_code = codearray
        return codearray
    
    def modulate(self, SNR = None, addsignal = None, plot=False):
        '''Modulates the DSSS encoded signal.
            SNR : float
                Optional Parameter for adding noise to signal in simulation environment. 
                The default is None.
            addsignal : ndarray
                Optional addition of another signal of the same width for simulating 
                CDMA. The default is None.
            plot : bool
                Optional parameter for plotting the modulated signal. The default is False.

            Returns
            -------
            BPSK : ndarray
                The BPSK modulated signal.'''
        
        self.BPSK = np.array([])
        for i in range(len(self.DSSS)):
            if self.DSSS[i] == 1:
                self.BPSK = np.concatenate((self.BPSK, self.s1))
            elif self.DSSS[i] == -1:
                self.BPSK = np.concatenate((self.BPSK, self.s0))
            self.carrier = np.concatenate((self.carrier, self.s1))
        #add noise to signal given SNR
        if SNR is not None:
            noise = np.random.normal(0, 1, len(self.BPSK))
            noise = noise / np.linalg.norm(noise) * np.linalg.norm(self.BPSK) / (10**(SNR/20))
            self.BPSK = self.BPSK + noise
        
        #add a signal to the signal
        if addsignal is not None:
            self.BPSK = self.BPSK + addsignal

        # plot the BPSK signal
        if (plot):
            plt.figure(figsize=(8, 6))
            plt.subplot(2, 1, 1)
            plt.plot(np.arange(0, (self.bit_t-1/self.Fs), 1/3000), self.BPSK[:3*len(self.t)], label='Modulated signal')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude (V)')
            plt.title('Modulated signal')
            plt.legend()
            plt.grid()
            plt.subplot(2, 1, 2)
            plt.subplots_adjust(hspace=0.5)
            f, Pxx_den = signal.welch(self.BPSK, self.Fs, nperseg=1024)
            plt.semilogy(f, Pxx_den)
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('PSD (V**2/Hz)')
            plt.title('Power spectral density of the modulated signal')
            plt.grid()
        return self.BPSK

    def demodulate(self,plot=False):
        '''Demodulates the BPSK modulated signal.
            Parameters
            ----------
            plot : bool
                Optional parameter for plotting the demodulated signal. The default is False.
            
            Returns
            -------
            result : ndarray
                The demodulated signal.'''
        self.rx = np.array([])
        self.demod = np.array([])
        self.result = np.array([])
        # despread the signal by bringing code back out of the psuedo-random sequence
        for i in range(len(self.pn_code)):
            if self.pn_code[i] == 1:
                self.rx = np.concatenate((self.rx, self.BPSK[(i*len(self.t)):((i+1)*len(self.t))]))
            else:
                self.rx = np.concatenate((self.rx, -1 * self.BPSK[(i*len(self.t)):((i+1)*len(self.t))]))
    
        # plot the received signal
        if(plot):
            plt.figure(figsize=(8, 6))
            plt.subplot(2, 1, 1)
            plt.plot(np.arange(0, (self.bit_t-1/self.Fs), 1/10000), self.BPSK[20*len(self.t):30*len(self.t)], label='Received signal')
            plt.plot(np.arange(0, (self.bit_t-1/self.Fs), 1/10000), self.rx[20*len(self.t):30*len(self.t)], label='Demodulated signal')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude (V)')
            plt.title('Received and demodulated signal')
            plt.legend()
            plt.grid()
            plt.subplot(2, 1, 2)
            plt.subplots_adjust(hspace=0.5)
            f, Pxx_den = signal.welch(self.rx, self.Fs, nperseg=1024)
            plt.semilogy(f, Pxx_den)
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('PSD (V**2/Hz)')
            plt.title('Power spectral density of the received and demodulated signal')
            plt.grid()
        
        # decode
        for i in range(int(len(self.message)/self.fp)):
            x = len(self.t) * self.fp
            cx = np.sum(self.carrier[(i*x):(i+1)*x] * self.rx[(i*x):(i+1)*x])
            if cx > 0:
                self.result = np.concatenate((self.result, [1]))
            else:
                self.result = np.concatenate((self.result, [-1]))
        return self.result
    
    def demodulate_wrong(self):
        '''Demodulates the BPSK modulated signal with a wrong code for comparison.
            Returns
            -------
            result_wrong : ndarray'''
        self.rx2 = np.array([])
        self.demod2 = np.array([])
        self.result_wrong = np.array([])
        for i in range(len(self.pn_code_wrong)):
            if self.pn_code_wrong[i] == 1:
                self.rx2 = np.concatenate((self.rx2, self.BPSK[(i*len(self.t)):((i+1)*len(self.t))]))
            else:
                self.rx2 = np.concatenate((self.rx2, -1 * self.BPSK[(i*len(self.t)):((i+1)*len(self.t))]))
        self.demod2 = self.rx2
        for i in range(int(len(self.message)/self.fp)):
            x = len(self.t) * self.fp
            cx = np.sum(self.carrier[(i*x):(i+1)*x] * self.demod2[(i*x):(i+1)*x])
            if cx > 0:
                self.result_wrong = np.concatenate((self.result_wrong, [1]))
            else:
                self.result_wrong = np.concatenate((self.result_wrong, [-1]))
        return self.result_wrong
    
    def plot_message(self):
        '''Plots the original message, the demodulated message and the demodulated message with a wrong code.'''
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

    def plot_constellation(self):
        '''Plots the constellation diagram of the modulated signal.'''
        plt.figure(figsize=(8, 6))
        plt.scatter(self.BPSK.real, self.BPSK.imag, s=1)
        plt.xlabel('In-phase')
        plt.ylabel('Quadrature')
        plt.title('Constellation diagram of the modulated signal')
        plt.grid()



