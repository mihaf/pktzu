def Raw_Filtered_Plot(t,y,fy,measurement='Measurement',xlabel='x',ylabel='y',legend=True,filter=True):
    '''Plot Raw and Filtered data over time'''
    fig = plt.figure()
    plt.plot(t,y,label=f'Neobdelani podatki')# LDJ = {ldj:.0f}')
    if filter: plt.plot(t,fy,label=f'Filtrirani podatki')# LDJ = {ldjf:.0f}')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(measurement)
    if legend: plt.legend(loc='upper right')
    plt.show()

def AnalyzeSignal(d,ydataNo,order=8,CNr=0.1,Start=0,Interval=0,legend=True,filter=True):
    '''Get Raw and Filtered data. Using Lowpass Butterworth filter with order=order and Cnr=f_crit/f_Nyquist'''
    
    # Get sampling frequency over the whole interval (cutting off cut first and last points)
    cut = 0
    t, y = [d.iloc[:,col][cut:-(cut+1)] for col in (0,ydataNo)]
    dtlist = t.diff()[1:]
    fslist = 1/dtlist # Sampling frequency
    fs, sfs = np.average(fslist),np.std(fslist)
    sampling = f', Vzorčenje: $\\nu$ = {fs:.0f} Hz, $\sigma_\\nu =$ {sfs:.0f} Hz'
    
    # Filter and plot interval given in seconds
    if Interval == 0:
        Intervals = len(d)-int(Start*fs)
    else:
        Intervals = int(Interval*fs)
    Starts = int(Start*fs)
    t, y = [d.iloc[:,col][Starts:Starts+Intervals] for col in (0,ydataNo)]
    b, a = signal.butter(order, CNr * (0.5*fs), fs = fs) # Lowpass Butterworth filter with order=order and Cnr=f_crit/f_Nyquist
    fy = signal.filtfilt(b, a, y) # Apply filter forward and backward to a signal
    Raw_Filtered_Plot(t,y,fy,
                      measurement,
                      xlabel=d.columns[0]+sampling,
                      ylabel=d.columns[ydataNo],
                      legend=legend,
                      filter=filter)
    return #t, y, fy