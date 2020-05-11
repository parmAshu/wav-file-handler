import builtins
import audioop
import struct
import sys
from chunk import Chunk
from collections import namedtuple

WAVE_FORMAT_PCM = 0x0001

class Wave_write:
    #class constructor
    def __init__(self):
        self.wavdata=b''
        self._nchannels = 0
        self._sampwidth = 0
        self._framerate = 0
        self._nframes = 0
    
    #function to set channel number
    def setnchannels(self, nchannels):
        self._nchannels = nchannels

    #function to set sample width
    def setsampwidth(self, sampwidth):
        self._sampwidth = sampwidth

    #function to set framerate
    def setframerate(self, framerate):
        self._framerate = int(round(framerate))

    #function to write the audio bytes into a byte string
    def writeframes(self, data):

        self._write_header(len(data))

        nframes = len(data) // (self._sampwidth * self._nchannels)
        
        #if the system is big endian then, reverse the order of recorded sample bytes as the wav files are always little endian
        if self._sampwidth != 1 and sys.byteorder == 'big':
            data = audioop.byteswap(data, self._sampwidth)

        self.wavdata=self.wavdata+data
        
        return self.wavdata

    #function to write the data into a byte string
    def _write_header(self, initlength):

        self.wavdata=self.wavdata+b'RIFF'
        
        self._nframes = initlength // (self._nchannels * self._sampwidth)
        self._datalength = self._nframes * self._nchannels * self._sampwidth
        
        self.wavdata=self.wavdata+struct.pack('<L4s4sLHHLLHH4s',36 + self._datalength, b'WAVE', b'fmt ', 16,WAVE_FORMAT_PCM, self._nchannels, self._framerate,self._nchannels * self._framerate * self._sampwidth,self._nchannels * self._sampwidth,self._sampwidth * 8, b'data')

        self.wavdata=self.wavdata+struct.pack('<L', self._datalength)

