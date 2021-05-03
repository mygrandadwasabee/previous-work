import numpy
import pygame
import math
import time

# MICROTONAL SYNTHESISER
# PLAY SOUNDS BY PRESSING THE KEYS LISTED IN THE keys ARRAY
# USE LEFT SHIFT KEY AS A SUSTAIN PEDAL
# define the sound of the instrument by listing the strength of each overtone
overtones = [0.72,0,0.29,0,0.12,0,0.04,0,0.01,0,0.03,0,0.03,0,0.02]
# These are the keys which will make sounds when pressed, in ascending order of frequency
keys = [pygame.K_q,pygame.K_2,pygame.K_w,pygame.K_3,pygame.K_e,pygame.K_4,pygame.K_r,pygame.K_t,pygame.K_6,pygame.K_y,pygame.K_7,pygame.K_u,pygame.K_8,pygame.K_i,pygame.K_9,pygame.K_o,pygame.K_0,pygame.K_p,pygame.K_MINUS,pygame.K_LEFTBRACKET,
        pygame.K_s,pygame.K_x,pygame.K_d,pygame.K_c,pygame.K_f,pygame.K_v,pygame.K_b,pygame.K_h,pygame.K_n,pygame.K_j,pygame.K_m,pygame.K_k,pygame.K_COMMA,pygame.K_l,pygame.K_PERIOD]
# The number of tones to fit into an "octave"
I = 19
# The frequency multiplier for the "octave"
b = 2








size = (1366, 720)

bits = 16
#the number of channels specified here is NOT 
#the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels

pygame.mixer.pre_init(44100, -bits, 2)
pygame.init()
_display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)


#freqency for the left speaker
frequency_l = 440
#frequency for the right speaker
frequency_r = 550
frequencies = [440]

#this sounds totally different coming out of a laptop versus coming out of headphones

sample_rate = 44100

max_sample = 2**(bits - 1) - 1

def find_number_of_wavelengths(f):
    l = []
    for i in range(1,100):
        l.append(min(i*f-int(i*f),1-i*f+int(i*f)))
    return l.index(min(l))+1

def sawtooth(x):
    return 2*(x-int(x))-1

def wave(x):
    return math.sin(2*math.pi*x)

def synth(x):
    t = sum(overtones)
    total = 0
    for i in range(len(overtones)):
        total += overtones[i]/t*wave((i+1)*x)
    return total

def square(x):
    if x-int(x) > 0.5:
        return 1
    else:
        return -1

def spikey(x):
    if x - int(x) > 0.5:
        return sawtooth(2-2*x)
    else:
        return sawtooth(2*x)

def superpose(fs,t):
    sum_ = 0
    for f in fs:
        #sum_ += 0.2*max_sample*math.sin(2*math.pi*f*t)
        sum_ += 0.2*max_sample*synth(f*t)
    return int(round(sum_))

def test(x):
    return 0.1468*math.sin(2*math.pi*x)+0.1875*math.sin(4*math.pi*x)+0.375*math.sin(6*math.pi*x)+0.167*math.sin(8*math.pi*x)+0.021*math.sin(10*math.pi*x)+0.083*math.sin(12*math.pi*x)

def note(frequencies):
    duration = find_number_of_wavelengths(frequencies[0])/frequencies[0]
    n_samples = int(round(duration*sample_rate))
    #setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
    buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
    for s in range(n_samples):
        t = float(s)/sample_rate    # time in seconds

        #grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
        buf[s][0] = superpose(frequencies,t)        # left
        buf[s][1] = superpose(frequencies,t)        # right

    sound = pygame.sndarray.make_sound(buf)
    return sound



clock = pygame.time.Clock()

sounds = []
rs = []
sustain = False
for i in range(len(keys)):
    sounds.append(note([130*b**(i/I)]))
    rs.append(b**(i/I))
_quit = False
while not _quit:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            try:
                print(rs[keys.index(event.key)])
                sounds[keys.index(event.key)].play(loops=-1)
            except:
                if event.key == pygame.K_z:
                    sounds[keys.index(pygame.K_LEFTBRACKET)].play(loops=-1)
                elif event.key == pygame.K_LSHIFT:
                    sustain = True
                else:
                    print("No clue")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                sustain = False
                for i in range(len(keys)):
                    if not pygame.key.get_pressed()[i]:
                        sounds[i].stop()
            elif not sustain:
                try: sounds[keys.index(event.key)].stop()
                except:
                    if event.key == pygame.K_z:
                        sounds[keys.index(pygame.K_LEFTBRACKET)].stop()
                    else:
                        print("No clue")
        elif event.type == pygame.QUIT:
            _quit = True
    clock.tick(100)


pygame.quit()

