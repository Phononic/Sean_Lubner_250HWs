Sean Lubner
AY 250 Final Project

This program analyzes the output data for my lab's 3-omega thermal conductivity measurements.

It can either analyze one file at a time, or iterate over all the data files in a given directory (which it can distinguish from other non-data files in that directory).

It reads in a text file containing sensor calibration data.

It allows the user to dynamically select the frequency fit interval from the data, as well as pick specific (noisy) data points to exclude.  To do this, when the data is plotted, simply click over the points you wish to fit to.  If you want to adjust your fit, just re-select a new region.  To exclude points, press t to toggle between point exclusion mode and fit region selection mode.

Displays on-screen instructions, as well as on-screen summary of fit values and errors.

(Optionally) saves the fitted figures as pdfs, as well as two output .txt files: one verbose containing all relevant information, and one compact containing the key numbers in tab-delimited format for easy copy/pasting over into Excel files for plotting and further analysis.

Defensive coding implemented in several areas to try to assist user against using the program incorrectly.