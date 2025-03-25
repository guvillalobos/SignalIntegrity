import SignalIntegrity.Lib as si
sdp=si.p.SystemDescriptionParser()
sdp.AddLines(['device DV 4','device ZI 2','device ZO 2','connect ZI 1 DV 2',
    'connect ZI 2 DV 1','connect ZO 1 DV 4','port 1 ZI 1 2 ZI 2 3 ZO 2 4 DV 3'])
ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),size='small')
ssps.AssignSParameters('DV',si.sy.VoltageControlledVoltageSource('\\alpha'))
ssps.AssignSParameters('ZI',si.sy.SeriesZ('Z_i'))
ssps.AssignSParameters('ZO',si.sy.SeriesZ('Z_o'))
ssps.LaTeXSolution(size='big').Emit()
