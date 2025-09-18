# coding: utf-8
from json import load
from types import LambdaType
import numpy as np
import mne
from mne.time_frequency import psd_array_multitaper
from scipy.integrate import simpson

def preprocess(data_arr, info_arr):
    ch_t = ['eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg']
    ch_n = np.array(info_arr)
    ch_n = ch_n[1:]
    info = mne.create_info(ch_names=ch_n.tolist(), sfreq=info_arr[0], ch_types=ch_t)
    data = mne.io.RawArray(data_arr, info)

    iir_params = {'order':4, 'ftype':"butter"}
    data.set_montage('standard_1020')
    data.filter(1.,47., method='iir', iir_params=iir_params)
    data.notch_filter(60, fir_design='firwin')
    data.notch_filter(50, fir_design='firwin')

    xX=data.get_data()
    spec = data.compute_psd(method='welch', fmin=3, fmax=46, picks='eeg')
    psds = spec.data
    freqs = spec.freqs
    #psds, freqs = mne.time_frequency.psd_array_welch(x=xX, sfreq=int(info_arr[0]), n_fft=int(1*int(info_arr[0])))
    #psds, freqs = psd_array_multitaper(xX, int(info_arr[0]), adaptive=True, normalization='full', verbose=0)

    bands = {
        #'delta': (1, 4),
        #'theta': (4, 8),
        'alpha': (8, 12),
        'beta': (12, 30),
        #'gamma': (30, 45)    
    }

    powers = []
    for band_name, (fmin, fmax) in bands.items():
        freq_res = freqs[1] - freqs[0]
        idx_band = np.logical_and(freqs >= fmin, freqs <= fmax)
        #freq_res = np.fft.rfftfreq(len(xX[0]), 1.0/int(info_arr[0]))
        #idx_band = np.where((freq_res >= fmin) & (freq_res <= fmax))
        powers_ch = []
        for ch in range(8):
            power = simpson(psds[ch, idx_band], dx=freq_res)
            #fft_vals = np.absolute(np.fft.rfft(xX[ch]))
            #psds, freqs = raw.compute_psd(method='welch', fmin=4, fmax=46, picks='eeg')
            #power = np.mean(fft_vals[idx_band])
            #power /= simpson(psds[ch], dx=freq_res)
            #power = round(power, 3) 
            powers_ch.append(power)
        powers.append(powers_ch)

    #np_powers_t = np.array(powers[0])
    np_powers_a = np.array(powers[0])
    np_powers_b = np.array(powers[1])
    #np_powers_g = np.array(powers[3])
    np_powers_a_F = np.array([np_powers_a[3], np_powers_a[4]])
    np_powers_b_F = np.array([np_powers_b[3], np_powers_b[4]])
    #np_powers_g_F = np.array([np_powers_g[3], np_powers_g[4]])
    np_powers_a_O = np.array([np_powers_a[0], np_powers_a[7]])
    np_powers_b_O = np.array([np_powers_b[0], np_powers_b[7]])
    #np_powers_t_C = np.array([np_powers_t[2], np_powers_t[5]])

    p_mean_a_f = np.mean(np_powers_a_F)
    p_mean_b_f = np.mean(np_powers_b_F)
    #p_mean_g_f = np.mean(np_powers_g_F)
    p_mean_a_o = np.mean(np_powers_a_O)
    p_mean_b_o = np.mean(np_powers_b_O)
    #p_mean_t_c = np.mean(np_powers_t_C)
    return p_mean_a_f, p_mean_b_f, p_mean_a_o, p_mean_b_o#, p_mean_t_c
    #if (p_mean_a > p_mean_b):
    #    return True
    #else:
    #    return False