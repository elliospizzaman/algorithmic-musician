import pyaudio
from numpy import linspace,sin,int16,concatenate

# Amplitude must be in the closed interval [-32768, 32768] because that is the max a 2 byte int can store
def note(freq, length=1, amp=1, rate=44100):
    TAU = 6.2831852 # tau is 2 * pi
    # Create numpy array length*rate long with the first value at 0 and the last at length
    t = linspace(0,length,length*rate)
    # Calculate the sine wave at the given frequency and multiply by amplitude
    data = sin(TAU * freq * t) * amp
    # convert the numpy array to 2 byte integers
    return data.astype(int16)

# Create a chord from multiple notes
def chord(*args):
     return sum(n//len(args) for n in args)
     
def phrase(*args):
    return concatenate(args)

# Test Case
if __name__=="__main__":
    # Open a pyaudio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                    channels=1,
                    rate=44100,
                    output=True)
    # create the tone of a C2 bowed bass
    notes = []
    notes.append(note(68,1,amp=32000))
    notes.append(note(100,1,amp=32000))
    notes.append(note(130,1,amp=6000))
    notes.append(note(260,1,amp=6000))
    song = phrase(notes[2], notes[3], chord(*notes))
    stream.write(song.tostring())
    # close the Pyaudio stream
    stream.stop_stream()
    stream.close()
    p.terminate()