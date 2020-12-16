#!/usr/bin/env python

import os
from uuid import uuid1
from random import randint, shuffle

from tqdm import tqdm
from pydub import AudioSegment

packs = []
nb_pack = 0
for i in range(1, len(os.listdir('inputs/sounds/'))):
    pack = []
    nb_pack += 1
    for j in range(1, len(os.listdir(f'inputs/sounds/pack{i}/'))):
        pack.append(AudioSegment.from_file(f"inputs/sounds/pack{i}/{j}.wav", format="wav"))
    packs.append(pack)

noises = []
for i in range(1, len(os.listdir('inputs/noises/'))):
    noises.append(AudioSegment.from_file(f"inputs/noises/{i}.wav", format="wav"))

change_sound_pack_mod = 25
final = noises[0][:2000]
pack = packs[0]
pack_idx = 0
tempo_mod = 30
tempo_idx = 0
tempo_phase = [
    dict(sound=dict(min_=500, max_=1000), noise=dict(min_=1000,max_=3000)),
    dict(sound=dict(min_=100, max_=300), noise=dict(min_=100,max_=500))
]

min_max = tempo_phase[0]
for i in tqdm(range(5000)):
    if i % tempo_mod == 0:
        tempo_idx += 1
        min_max = tempo_phase[tempo_idx%len(tempo_phase)]

    if i % change_sound_pack_mod == 0:
        pack_idx += 1
        pack = packs[pack_idx%nb_pack]

    if i % 2:
        shuffle(pack)
        sound = pack[0]
        min_ = min_max['sound']['min_']
        max_ = min_max['sound']['max_']
    else:
        shuffle(noises)
        sound = noises[0]
        min_ = min_max['noise']['min_']
        max_ = min_max['noise']['max_']

    len_sound = len(sound)
    start = randint(0, max(0, len_sound-max_))
    end = start + randint(min_, max_)
    sample = sound[start:end]
    final += sample

final.export(f"outputs/noise-cut-up_{uuid1()}.mp3", format="mp3")
