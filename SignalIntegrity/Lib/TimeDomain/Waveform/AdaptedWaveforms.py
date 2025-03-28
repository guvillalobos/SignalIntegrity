"""
AdaptedWaveforms.py
"""

# Copyright (c) 2021 Nubis Communications, Inc.
# Copyright (c) 2018-2020 Teledyne LeCroy, Inc.
# All rights reserved worldwide.
#
# This file is part of SignalIntegrity.
#
# SignalIntegrity is free software: You can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>

class AdaptedWaveforms(list):
    """waveforms adapted to common time axis"""
    def __init__(self,wfl):
        """Constructor  
        insternally adapts all of the waveforms provided and keeps them internally in
        a list.
        @param wfl list of instances of class Waveform to be adapted
        """
        from SignalIntegrity.Lib.TimeDomain.Filters.WaveformTrimmer import WaveformTrimmer
        from SignalIntegrity.Lib.TimeDomain.Filters.InterpolatorSinX import InterpolatorSinX
        from SignalIntegrity.Lib.TimeDomain.Filters.InterpolatorSinX import FractionalDelayFilterSinX
        from SignalIntegrity.Lib.TimeDomain.Filters.InterpolatorLinear import InterpolatorLinear
        from SignalIntegrity.Lib.TimeDomain.Filters.InterpolatorLinear import FractionalDelayFilterLinear
        from SignalIntegrity.Lib.Rat import Rat
        strategy=wfl[0].adaptionStrategy

        #upsample all of the waveforms first
        # udfl is a list of (U,D) tuples containing upsample and decimation factor
        # todo: this change was made to prevent a failure, presumably when decimation was needed (and would
        # create an integer upsample factor of 0).  Now, for example, it might have an upsample factor of 1 and
        # a downsample factor of 2, instead of 0 for the integer upsample factor, which caused failure.  But, it's
        # unclear how the downsample factor is handled downstream of this and this needs to be investigated.
        # in any case, all the unit tests pass with this change.
        udfl=[Rat(wfl[0].td.Fs/wf.td.Fs) for wf in wfl]
        wfl=[wf if uf[0] == 1 else wf*
            (InterpolatorSinX(uf[0]) if strategy=='SinX' else InterpolatorLinear(uf[0]))
            for (uf,wf) in zip(udfl,wfl)]
        adl=[wfl[0].td/wf.td for wf in wfl]
        fdl=[ad.D-int(ad.D) for ad in adl]
        wfl=[wf if fd == 0.0 else wf*
            (FractionalDelayFilterSinX(fd,True) if strategy=='SinX' else FractionalDelayFilterLinear(fd,True))
            for (fd,wf) in zip(fdl,wfl)]
        overlapping=wfl[0].td
        for wf in wfl[1:]: overlapping=overlapping.Intersection(wf.td)
        # overlapping now contains the overlapping waveform
        adl=[overlapping/wf.td for wf in wfl]
        trl=[WaveformTrimmer(max(0,int(round(ad.TrimLeft()))),max(0,int(round(ad.TrimRight())))) for ad in adl]
        list.__init__(self,[wf*tr for (wf,tr) in zip(wfl,trl)])
