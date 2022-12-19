from wave import open
from struct import struct
from math import floor

FRAME_RATE = 11035
C_FREQ, E_FREQ, G_FREQ = 261.63, 329.63, 392.00
def encode(x):
    """ ENcode float x between -1 and 1 as two bytes """
    i = int(16384 * x)
    return Struct('h').pack(i)

def play(sampler, name = "song.wav", seconds = 2):
    """ Write the output of a sampler function as a wav file. """
    out = open(name, 'wb')
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(FRAME_RATE)
    t = 0
    while t < seconds * FRAME_RATE:
        sample = sampler(t)
        out.writeframes(encode(sample))
        t = t + 1
    out.close()

def tri(frequency, amplitude = 0.3):
    """ A continuous triangle wave """
    period = FRAME_RATE // frequency
    def sampler(t):
        saw_wave = t / period -floor(t / period + 0.5)
        tri_wave = 2 * abs(2 * saw_wave) - 1
        return amplitude * tri_wave
    
    return sampler

def both(f, q):
    return lambda t: f(t) + g(t)

def note(f, start, end, fade = 0.01):
    def sampler(t):
        seconds = t / FRAME_RATE
        if seconds < start:
            return 0
        elif seconds > end:
            return 0
        elif seconds < start + fade:
            return (seconds - start) / fade * f(t)
        elif seconds > end - fade:
            return (end - seconds) / fade * f(t)
        else:
            return f(t)
    return sampler

def mario_at(octave):
    c, e = tri(octave * C_FREQ), tri(octave * E_FREQ)
    g, low_g = tri(octave * G_FREQ), tri(octave * G_FREQ / 2)
    return mario(c, e, g, low_g)

def mario(c, e, g, low_g):
    z = 0
    song = note(e, z, z + 1/8)
    z += 1/8
    song = both(song, note(e, z + 1/8))
    z += 1/4
    song = both(song, note(e, z + 1/8))
    z += 1/4
    song = both(song, note(e, z + 1/8))
    z += 1/8
    song = both(song, note(e, z + 1/8))
    z += 1/4
    song = both(song, note(e, z + 1/4))
    z += 1/2
    song = both(song, note(e, z + 1/4))
    return song

play(both(mario_at(1), mario_at(1/2)))

