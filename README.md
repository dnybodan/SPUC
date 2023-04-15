# SPUC
Simulated Protocol for Unmaned aerial vehicle Communications. 
A physical and networking protocol simulator targeted at UAV communications. 

This simulator provides classes and methods and example scripts for running a basic Unmaned Aerial Vehicle protocol 
using BPSK Binary Phase-Shift Keying as well as DSSS Direct Sequence Spread Spectrum. It mixes pseudo random
noise or PN codes with networking strategies for CDMA in order to provide reliable communication in potentially
noisy and congested frequency bands. The simulator provides noise modeling and channel capacity estimation.

This simulator also provides classes for a basic UAV packet structure including integer and string field entries,
binary message construction. It also provides binary message reconstruction and comparison methods for identifying
proper data transmission.

Further Work: 

There is also a class called UAVFrame which is intended to wrap UAVPacket objects with networking 
information; provide packet encryption and decryption; create and verify checksum...etc It is built but not
currently implimented in test scripts but can definitely be utilized for further research and development.


Additionally, this protocol can and should be implimented on SDRs for furthur testing, especially if it is 
modified for UAV usage.

