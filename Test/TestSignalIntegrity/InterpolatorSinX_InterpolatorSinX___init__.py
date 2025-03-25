class InterpolatorSinX(FirFilter):
    def __init__(self,U):
        F=0.
        FirFilter.__init__(self,FilterDescriptor(U,self.S+F,2*self.S),SinX(self.S,U,F))
    def FilterWaveform(self,wf):
        fd=self.FilterDescriptor()
        us=[0. for k in range(len(wf)*fd.U)]
        for k in range(len(wf)):
            us[k*fd.U]=wf[k]
        return FirFilter.FilterWaveform(self,Waveform(wf.td,us))

