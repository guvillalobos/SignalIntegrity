import SignalIntegrity.Lib as si
sdp=si.p.SystemDescriptionParser()
sdp.AddLines(['device DV 4','device ZI 4','device ZO 2',
    'port 1 ZI 1 2 ZI 2 3 ZO 2 4 DV 3',
    'connect ZI 3 DV 2','connect ZI 4 DV 1','connect ZO 1 DV 4'])
ssps=si.sd.SystemSParametersSymbolic(sdp.SystemDescription(),size='small')
ssps.AssignSParameters('DV',si.sy.VoltageControlledVoltageSource('\\alpha'))
ssps.AssignSParameters('ZI',si.sy.ShuntZ(4,'Z_i'))
ssps.AssignSParameters('ZO',si.sy.SeriesZ('Z_o'))
ssps.LaTeXSolution(size='big').Emit()
