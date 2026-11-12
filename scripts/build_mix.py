#!/usr/bin/env python3
"""Build assets/mix.wav for the V3 train short.

Voice (voice/voice.wav, Warm Pebble, 50.184s) + a synthesized music bed
(soft pad chords + sub bass) + timed SFX (alert beep, speed whoosh, brake
screech, teardown clinks, crack ting, bubble blips, gauge alarm, counter
ticks), loudnormed to -14.5 LUFS, exactly 50.184s, stereo 48kHz.

Run from ~/workspace/blender_shorts_4/v3_train:
  python3 scripts/build_mix.py
"""
import os
import subprocess
import sys

import numpy as np
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, ".."))
SR = 48000
DUR = 50.184
N = int(SR * DUR)  # 2408832 samples

# ---------------------------------------------------------------- helpers

def tone(freq, dur_s, sr=SR, harmonics=(1.0,), attack=0.01, decay=None):
    """Sine-stack tone with attack/decay envelope. Returns float array."""
    n = max(1, int(dur_s * sr))
    t = np.arange(n) / sr
    out = np.zeros(n)
    for i, amp in enumerate(harmonics):
        out += amp * np.sin(2 * np.pi * freq * (i + 1) * t)
    env = np.ones(n)
    a = max(1, int(attack * sr))
    env[:a] = np.linspace(0, 1, a)
    if decay is not None:
        d = max(1, int(decay * sr))
        env[-d:] *= np.linspace(1, 0, d)
    return out * env


def add_at(track, sig, start_s):
    """Add sig into track at start_s (clipped to track length)."""
    i0 = int(start_s * SR)
    i1 = min(len(track), i0 + len(sig))
    if i1 > i0:
        track[i0:i1] += sig[:i1 - i0]


def fade_edges(sig, fade_s=0.05):
    n = len(sig)
    f = int(fade_s * SR)
    sig[:f] *= np.linspace(0, 1, f)
    sig[-f:] *= np.linspace(1, 0, f)
    return sig


# ------------------------------------------------------------------- voice

def load_voice():
    sr, data = wavfile.read(os.path.join(PROJ, "voice", "voice.wav"))
    assert sr == SR, f"voice sr {sr} != {SR}"
    v = data.astype(np.float64)
    if data.dtype == np.int16:
        v /= 32768.0
    elif data.dtype == np.int32:
        v /= 2147483648.0
    if v.ndim > 1:
        v = v.mean(axis=1)
    if len(v) < N:
        v = np.concatenate([v, np.zeros(N - len(v))])
    return v[:N]


# ---------------------------------------------------------------- music bed

# Am - F - C - G, one chord per ~12.5s, soft pad (sine stack) + sub root.
CHORDS = [
    (0.0, [110.00, 164.81, 220.00, 261.63]),   # A2 E3 A3 C4 (Am)
    (12.55, [87.31, 174.61, 220.00, 261.63]),  # F2 F3 A3 C4 (F)
    (25.10, [98.00, 196.00, 261.63, 329.63]),  # G2 G3 C4 E4 (C)
    (37.65, [98.00, 146.83, 196.00, 246.94]),  # G2 D3 G3 B3 (G)
]


def build_bed():
    bed_l = np.zeros(N)
    bed_r = np.zeros(N)
    for start, freqs in CHORDS:
        dur = 13.5  # overlaps the next chord for a smooth crossfade
        n = int(dur * SR)
        t = np.arange(n) / SR
        sig = np.zeros(n)
        for f in freqs:
            sig += 0.5 * np.sin(2 * np.pi * f * t)
            sig += 0.18 * np.sin(2 * np.pi * f * 2 * t)
        # slow attack + release crossfade
        env = np.ones(n)
        a = int(2.0 * SR)
        env[:a] = np.linspace(0, 1, a)
        env[-a:] = np.linspace(1, 0, a)
        sig *= env
        # slight stereo widening: detuned copy on the right
        sig_r = np.zeros(n)
        for f in freqs:
            sig_r += 0.5 * np.sin(2 * np.pi * (f * 1.002) * t)
            sig_r += 0.18 * np.sin(2 * np.pi * (f * 2.004) * t)
        sig_r *= env
        add_at(bed_l, sig * 0.10, start)
        add_at(bed_r, sig_r * 0.10, start)
        # sub bass root
        sub = tone(freqs[0] / 2, dur, harmonics=(1.0,), attack=2.0,
                   decay=2.0)
        add_at(bed_l, sub * 0.06, start)
        add_at(bed_r, sub * 0.06, start)
    return bed_l, bed_r


# --------------------------------------------------------------------- SFX

def build_sfx():
    sfx = np.zeros(N)
    # red alert beeps f279-297 (9.33-9.93s): 3 two-tone pulses
    for i, t0 in enumerate((9.33, 9.53, 9.73)):
        add_at(sfx, tone(880, 0.09, attack=0.005, decay=0.02) * 0.20, t0)
        add_at(sfx, tone(660, 0.09, attack=0.005, decay=0.02) * 0.20,
               t0 + 0.10)
    # speed whoosh f303-411 (10.1-13.7s): rising filtered noise + rumble
    rng = np.random.default_rng(7)
    n = int(3.6 * SR)
    noise = rng.standard_normal(n)
    # simple rising lowpass feel: cumulative smoothing with shrinking window
    k = np.ones(40) / 40
    noise = np.convolve(noise, k, mode="same")
    noise *= np.linspace(0.1, 1.0, n)  # swell
    noise = fade_edges(noise, 0.4)
    add_at(sfx, noise * 0.10, 10.1)
    t = np.arange(n) / SR
    rumble = np.sin(2 * np.pi * (55 + 40 * t / 3.6) * t) * np.linspace(
        0.2, 1.0, n)
    add_at(sfx, fade_edges(rumble, 0.4) * 0.12, 10.1)
    # brake screech f508-539 (16.95-17.97s): metallic highs + rumble decay
    n = int(1.05 * SR)
    t = np.arange(n) / SR
    vib = 1 + 0.03 * np.sin(2 * np.pi * 9 * t)
    screech = (np.sin(2 * np.pi * 2150 * vib * t)
               + 0.7 * np.sin(2 * np.pi * 2780 * vib * t)
               + 0.5 * np.sin(2 * np.pi * 3120 * vib * t))
    screech *= np.exp(-1.2 * t) * np.minimum(1, t / 0.05)
    add_at(sfx, screech * 0.10, 16.95)
    # teardown clinks f618-680 (20.6-22.67s): 5 metallic pings
    for i, (t0, f) in enumerate(((20.6, 1450), (20.95, 1900),
                                 (21.3, 1200), (21.7, 2300),
                                 (22.1, 1650))):
        ping = tone(f, 0.22, harmonics=(1.0, 0.4, 0.2), attack=0.002)
        ping *= np.exp(-np.arange(len(ping)) / SR * 18)
        add_at(sfx, ping * 0.22, t0)
    # crack ting f870-907 (29.0-30.24s): high ting + low thud
    ting = tone(3200, 0.5, harmonics=(1.0, 0.3), attack=0.002)
    ting *= np.exp(-np.arange(len(ting)) / SR * 8)
    add_at(sfx, ting * 0.22, 29.05)
    add_at(sfx, tone(70, 0.4, attack=0.005, decay=0.3) * 0.30, 29.05)
    # bubble blips f980-1054 (32.67-35.13s): 6 rising blips
    for i, t0 in enumerate((32.67, 32.93, 33.20, 33.47, 33.73, 34.00)):
        blip = tone(520 + i * 70, 0.12, attack=0.01, decay=0.06)
        add_at(sfx, blip * 0.16, t0)
    # gauge alarm rise f1142-1165 (38.07-38.85s): soft rising tone
    n = int(0.78 * SR)
    t = np.arange(n) / SR
    rise = np.sin(2 * np.pi * (500 + 300 * t / 0.78) * t)
    add_at(sfx, fade_edges(rise, 0.15) * 0.08, 38.07)
    # counter ticks f1196-1270 (39.87-42.33s): 8 ticks
    for i in range(8):
        tick = tone(2000, 0.04, attack=0.002, decay=0.03)
        add_at(sfx, tick * 0.18, 39.87 + i * 0.33)
    # resolve chord at the end (48.3-50.18s): warm C major swell
    n = int(1.88 * SR)
    t = np.arange(n) / SR
    chord = sum(np.sin(2 * np.pi * f * t)
                for f in (261.63, 329.63, 392.00))
    chord *= np.linspace(0, 1, n) ** 2
    add_at(sfx, chord * 0.06, 48.3)
    return sfx


# -------------------------------------------------------------------- main

def main():
    voice = load_voice()
    bed_l, bed_r = build_bed()
    sfx = build_sfx()
    # mix: voice dominant, bed + sfx underneath
    mix_l = voice * 1.0 + bed_l + sfx * 0.9
    mix_r = voice * 1.0 + bed_r + sfx * 0.9
    # safety peak limit before loudnorm (avoid clipping the premix)
    peak = max(np.abs(mix_l).max(), np.abs(mix_r).max())
    if peak > 0.98:
        mix_l *= 0.98 / peak
        mix_r *= 0.98 / peak
    stereo = np.stack([mix_l, mix_r], axis=1)
    premix = os.path.join(PROJ, "assets", "premix.wav")
    final = os.path.join(PROJ, "assets", "mix.wav")
    os.makedirs(os.path.join(PROJ, "assets"), exist_ok=True)
    wavfile.write(premix, SR, (stereo * 32767).astype(np.int16))
    # loudnorm to -14.5 LUFS (single pass, linear), exactly 50.184s
    cmd = ["ffmpeg", "-y", "-i", premix, "-af",
           "loudnorm=I=-14.5:TP=-1.5:LRA=11:linear=true",
           "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", final]
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)
    # verify: duration + loudness
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_name,sample_rate,channels",
         "-of", "default=noprint_wrappers=1", final],
        capture_output=True, text=True, check=True)
    print(probe.stdout)
    loud = subprocess.run(
        ["ffmpeg", "-i", final, "-vn", "-af", "ebur128", "-f", "null",
         "-"], capture_output=True, text=True)
    for line in loud.stderr.splitlines():
        if "Integrated loudness" in line or "True Peak" in line:
            print(line.strip())
    print("MIX OK:", final)


if __name__ == "__main__":
    main()
