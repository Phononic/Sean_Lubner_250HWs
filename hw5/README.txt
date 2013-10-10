AY250 Homework 5
Sean Lubner

################ General ################

################ Audio ################
---- Detected notes ----
file: 1,   notes: C4, D4, G4, (C5, D5)
file: 2,   notes: F3, C5, (F4, F5, C6)
file: 3,   notes: A4, E6
file: 4,   notes: C4, G5, (C5, C6, G6, C7, C8)
file: 5,   notes: G2, D3, B4, (D4)
file: 6,   notes: C5, G6, (C6, C7, C8)
file: 7,   notes: D5, A6, (D6)
file: 8,   notes: F4, C6, (F5)
file: 9,   notes: G3, D5, (G4)
file: 10,  notes: C2, G3, (C3, G4, C6)
file: 11,  notes: E2, B3, (E3, B4)
file: 12,  notes: C2, G3, (C3, C5)

For file 3.aif, a lower freq_threshold (15 Hz) was required to detect any peaks.  This file must be noisier than the others, or else horribly out of tune.

---- Explanation ----
To find the peaks, the Fourier Transformed data is smoothed with a smoothing window to merge peak clusters together into large peaks.  These regions are selected out, via a peak detection threshold, and then for each peak cluster region a single (maximal) peak is identified.  If this peak is within a frequency-threshold of a note, it is then identified as that note.  This is a robust way to avoid both false positives (mini peaks in the peak clusters) and false negatives (from having to set a frequency-threshold for exluding the mini peaks that is so stringent, it also excludes the true peak).

The first plot (red) shows the time-series waveform data of the audio file.  The second plot (blue) shows the power spectrum for that file.  The third plot (green) shows the smoothed power spectrum plotted on linear (not logarithmic) vertical axese, with the peak detection threshold plotted (horizontal black line)

Example plots are in the repo as Example_plot_2.jpg and Example_plot_8.jpg (corresponding to files 2.aif and 8.aif, respectively).