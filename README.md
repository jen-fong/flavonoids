# flavonoids
cli using python and pandas to analyze large amounts of research data


-using the updated kamepferol csv file
- the original contains the following structure 
  wavelength | fluorescence | wv | fluor | wv | fluor
- this is not convenient because we want to be able to just plot all the fluors against the one wv as the x axis.
- we will need to transform this file to remove all those columns not labeled as intensity if its not column 1
- In the updated file, there are 3 sections
  - section 1 - the wv columsn removed. We will do this in the python script to automate it
  - section 2 - this is the percent difference. it appears that the buffer intensity is subtracted from 'after addition of flavonoid' or 'control' (no flav) and then again when the h2o2 is added to both. columns Q and R are essentially the difference between h2o2 - flav or h2o2 - control. The percent difference is then calculated from this in the last column of section 2. 
- Section 3 - This is just section 1 but subtracting the buffer from all the other columns. Buffer is column 2 (flav) and 3(control).

Now for the percent inhibition @ 570 nm
- amplex red fluoresces at ~585 nm so we set the excitation wavelength to 570nm, just before it happens
- still cannot figure this out. really wihs I documented this
- got it, from the updated file, just the last two rows subtracted from each other
- this was actually done using data from march 2013! that's why the numbers were not matching!


- finally, we can move along
- we can use the most recent data to do it - april 2014

for next time
- learn to install ipython or jupyter notebooks 
- use offline mode and set the graphs to show right on the notebook
- learn how to get max height or more likely, the value at 585
- check to see if this works for data at 293
- also check to see what the percent different was used for
- bar plots for the % inhibit
