from graphics import *
import serial
import pyaudio
import wave
from  time import sleep
from threading import Thread


#define stream chunk
CHUNK_SIZE = 1024

p = pyaudio.PyAudio()
wav_filename = 'beep-02.wav';
wf=None



def play(framemod=1,chunk_size=CHUNK_SIZE) :
    # thread = Thread(target=playWave, args=(framemod,chunk_size,))
    # thread.start()
    playWave(framemod,chunk_size)

def playWave( framemod=1, chunk_size=CHUNK_SIZE):
    '''
    Play (on the attached system sound device) the WAV file
    named wav_filename.
    '''
    global p;
    global wf

    wf.rewind();

    divisor=0;

    if framemod<0:
        divisor = 1 / (framemod*-1);
    else:
        divisor=framemod


    # Open stream.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate()/framemod,
                    output=True)

    data = wf.readframes(chunk_size/framemod)
    i=0
    while len(data) > 0 and i<20*framemod: #
        i=i+1
        stream.write(data)
        data = wf.readframes(chunk_size/framemod)

    # Stop stream.
    stream.stop_stream()
    stream.close()


def main():
    # win = GraphWin("My Circle", 100, 100)
    # c = Circle(Point(50, 50), 10)
    # c.draw(win)

    global wf

    try:
        print('Trying to play file ' + wav_filename)
        wf = wave.open(wav_filename, 'rb')
    except IOError as ioe:
        sys.stderr.write('IOError on file ' + wav_filename + '\n' + \
                         str(ioe) + '. Skipping.\n')
        return
    except EOFError as eofe:
        sys.stderr.write('EOFError on file ' + wav_filename + '\n' + \
                         str(eofe) + '. Skipping.\n')
        return

    try:
       ser = serial.Serial('/dev/ttyUSB0',timeout=None,baudrate=9600,rtscts=False,dsrdtr=False);
    except serial.SerialException :
        try:
            ser = serial.Serial('/dev/ttyUSB1', timeout=None, baudrate=9600, rtscts=False, dsrdtr=False);
        except serial.SerialException:
            try:
                ser = serial.Serial('/dev/ttyUSB2', timeout=None, baudrate=9600, rtscts=False, dsrdtr=False);
            except serial.SerialException:
                try:
                    ser = serial.Serial('/dev/ttyUSB3', timeout=None, baudrate=9600, rtscts=False, dsrdtr=False);
                except serial.SerialException:
                    try:
                        ser = serial.Serial('/dev/ttyUSB5', timeout=None, baudrate=9600, rtscts=False, dsrdtr=False);
                    except serial.SerialException:
                        ser = serial.Serial('COM0', timeout=None, baudrate=9600, rtscts=False, dsrdtr=False);
    time.sleep(0.002);


    while 1 :
        out = ''
        if ser.inWaiting() > 0:
            out = ser.read_all().split(';')[0];

        if out and not out == '' and not out== ' ' and not out == '-':
            try:
                button = int(out);
                if button>0 :
                    play(button)
            except ValueError :
                continue


main();