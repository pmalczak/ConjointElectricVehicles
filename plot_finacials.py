# -*- coding: utf-8 -*-
__author__ = 'Piotr.Malczak@gpm-sys.com'

import numpy as np
import pandas as pd
from dash.exceptions import PreventUpdate
from plotly import graph_objs as go


def plot_financials(resultsDf, dfFlowLoad, provider, attribute, val, viewType, aggView=False, baseInds=None):

    attLower = attribute.lower()
    clrs = ['mediumblue', 'gold', 'teal', 'deepskyblue', 'red', 'purple', 'orange', 'deeppink']
    aggBrands = ['Chevrolet', 'Jaguar', 'Kia', 'Nissan', 'Tesla', 'Toyota', 'VW']
    segments = ['Millenial', 'Gen X', 'Baby Boomer']
    dfFlow = dfFlowLoad.copy()

    SIO_cols = [col for col in resultsDf.columns if 'SIO_' in col]
    dfSIO = resultsDf[SIO_cols].copy()
    dfSIO.columns = [x[len('SIO_'):] for x in SIO_cols]
    ARPU_cols = [col for col in resultsDf.columns if 'ARPU_' in col]
    dfARPU = resultsDf[ARPU_cols].copy()
    dfARPU.columns = [x[len('ARPU_'):] for x in ARPU_cols]
    Revenue_cols = [col for col in resultsDf.columns if 'Revenue_' in col]
    dfRevenue = resultsDf[Revenue_cols].copy()
    dfRevenue.columns = [x[len('Revenue_'):] for x in Revenue_cols]
    EBIT_cols = [col for col in resultsDf.columns if 'EBIT_' in col]
    dfEBIT = resultsDf[EBIT_cols].copy()
    dfEBIT.columns = [x[len('EBIT_'):] for x in EBIT_cols]

    # the last row of df shows the 'base' (starting) values. Every other row shows 'new' (terminal) values
    dfSIObase = dfSIO.loc[dfSIO.shape[0] - 1]
    dfARPUbase = dfARPU.loc[dfARPU.shape[0] - 1]
    dfRevenueBase = dfRevenue.loc[dfRevenue.shape[0] - 1]
    dfEBITbase = dfEBIT.loc[dfEBIT.shape[0] - 1]

    dfSIO.drop(dfSIO.tail(1).index, inplace=True)
    dfARPU.drop(dfARPU.tail(1).index, inplace=True)
    dfRevenue.drop(dfRevenue.tail(1).index, inplace=True)
    dfEBIT.drop(dfEBIT.tail(1).index, inplace=True)

    if aggView:
        dfSIOold = dfSIO.copy()
        dfSIOold['denomVWgroup'] = dfSIOold['Audi'] + dfSIOold['VW']
        dfSIOold['wghtAudi'] = dfSIOold['Audi'] / dfSIOold['denomVWgroup']
        dfSIOold['wghtVW'] = dfSIOold['VW'] / dfSIOold['denomVWgroup']

        attCols = [col for col in dfEBIT.columns if attLower in col]
        dfSIOcopy = dfSIO[attCols].copy()
        dfSIOcopy['Chevrolet'] = dfSIO['Chevrolet'].copy()
        dfSIOcopy['Jaguar'] = dfSIO['Jaguar'].copy()
        dfSIOcopy['Kia'] = dfSIO['Kia'].copy()
        dfSIOcopy['Nissan'] = dfSIO['Nissan'].copy()
        dfSIOcopy['Tesla'] = dfSIO['Tesla'].copy()
        dfSIOcopy['Toyota'] = dfSIO['Toyota'].copy()
        dfSIOcopy['VW'] = dfSIO['Audi'] + dfSIO['VW']
        dfSIO = dfSIOcopy.copy()

        dfARPUcopy = dfARPU[attCols].copy()
        dfARPUcopy['Chevrolet'] = dfARPU['Chevrolet'].copy()
        dfARPUcopy['Jaguar'] = dfARPU['Jaguar'].copy()
        dfARPUcopy['Kia'] = dfARPU['Kia'].copy()
        dfARPUcopy['Nissan'] = dfARPU['Nissan'].copy()
        dfARPUcopy['Tesla'] = dfARPU['Tesla'].copy()
        dfARPUcopy['Toyota'] = dfARPU['Toyota'].copy()
        dfARPUcopy['VW'] = (dfSIOold['wghtAudi'] * dfARPU['Audi']) + \
                            (dfSIOold['wghtVW'] * dfARPU['VW'])
        dfARPU = dfARPUcopy.copy()

        dfRevenueCopy = dfRevenue[attCols].copy()
        dfRevenueCopy['Chevrolet'] = dfRevenue['Chevrolet'].copy()
        dfRevenueCopy['Jaguar'] = dfRevenue['Jaguar'].copy()
        dfRevenueCopy['Kia'] = dfRevenue['Kia'].copy()
        dfRevenueCopy['Nissan'] = dfRevenue['Nissan'].copy()
        dfRevenueCopy['Tesla'] = dfRevenue['Tesla'].copy()
        dfRevenueCopy['Toyota'] = dfRevenue['Toyota'].copy()
        dfRevenueCopy['VW'] = dfRevenue['Audi'] + dfRevenue['VW']
        dfRevenue = dfRevenueCopy.copy()

        dfEBITcopy = dfEBIT[attCols].copy()
        dfEBITcopy['Chevrolet'] = dfEBIT['Chevrolet'].copy()
        dfEBITcopy['Jaguar'] = dfEBIT['Jaguar'].copy()
        dfEBITcopy['Kia'] = dfEBIT['Kia'].copy()
        dfEBITcopy['Nissan'] = dfEBIT['Nissan'].copy()
        dfEBITcopy['Tesla'] = dfEBIT['Tesla'].copy()
        dfEBITcopy['Toyota'] = dfEBIT['Toyota'].copy()
        dfEBITcopy['VW'] = dfEBIT['Audi'] + dfEBIT['VW']
        dfEBIT = dfEBITcopy.copy()

    if (viewType == "Consolidated + Initial Baseline") or (viewType == "Individual + Initial Baseline"):

        if viewType == "Consolidated + Initial Baseline":
            dfSIObase['VW'] = dfSIObase['Audi'] + dfSIObase['VW']
            dfSIObase = pd.Series(dfSIObase[attCols + aggBrands])
            dfSIObase.index = attCols + aggBrands

            dfRevenueBase['VW'] = dfRevenueBase['Audi'] + dfRevenueBase['VW']
            dfRevenueBase = pd.Series(dfRevenueBase[attCols + aggBrands])
            dfRevenueBase.index = attCols + aggBrands

            dfEBITbase['VW'] = dfEBITbase['Audi'] + dfEBITbase['VW']
            dfEBITbase = pd.Series(dfEBITbase[attCols + aggBrands])
            dfEBITbase.index = attCols + aggBrands

            dfARPUbase['VW'] = dfRevenueBase['VW'] / dfSIObase['VW']
            dfARPUbase = pd.Series(dfARPUbase[attCols + aggBrands])
            dfARPUbase.index = attCols + aggBrands

        dfSIO = dfSIO - dfSIObase
        dfARPU = dfARPU - dfARPUbase
        dfRevenue = dfRevenue - dfRevenueBase
        dfEBIT = dfEBIT - dfEBITbase
    else:
        dfSIO = dfSIO - dfSIO.loc[baseInds[0]]
        dfARPU = dfARPU - dfARPU.loc[baseInds[0]]
        dfRevenue = dfRevenue - dfRevenue.loc[baseInds[0]]
        dfEBIT = dfEBIT - dfEBIT.loc[baseInds[0]]

    dfSIO = dfSIO.round(3)
    dfARPU = dfARPU.round(3)
    dfRevenue = dfRevenue.round(3)
    dfEBIT = dfEBIT.round(3)

    if (attLower + '_1') not in dfFlow.columns:
        return None, None, None, None, None, None, None, None
    elif len(dfFlow[attLower + '_1'].unique()) <= 1:
        return None, None, None, None, None, None, None, None

    if attribute == 'Monthly':
        xText = ["-" + "$" + str(round(abs(x))) + 'p/m' if x < 0 else "+" + "$" + str(round(x)) + 'p/m'
                                for x in dfARPU[attLower + '_1']]
    elif attribute == 'Upfront':
        xText = ["-" + "$" + str(round(abs(x))) if x < 0 else "+" + "$" + str(round(x))
                                for x in dfARPU[attLower + '_1']]

    if aggView:
        ChevroletBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['Chevrolet'], name='Chevrolet', marker_color=clrs[1])
        JaguarBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['Jaguar'], name='Jaguar', marker_color=clrs[2])
        KiaBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['Kia'], name='Kia', marker_color=clrs[3])
        NissanBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['Nissan'], name='Nissan', marker_color=clrs[4])
        TeslaBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['Tesla'], name='Tesla', marker_color=clrs[5])
        ToyotaBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['Toyota'], name='Toyota', marker_color=clrs[6])
        VWBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['VW'], name='VW', marker_color=clrs[7])
        dataUse = [ChevroletBars, JaguarBars, KiaBars, NissanBars, TeslaBars, ToyotaBars, VWBars]
    else:
        AudiBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['Audi'], name='Audi', marker_color=clrs[0])
        ChevroletBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['Chevrolet'], name='Chevrolet', marker_color=clrs[1])
        JaguarBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['Jaguar'], name='Jaguar', marker_color=clrs[2])
        KiaBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['Kia'], name='Kia', marker_color=clrs[3])
        NissanBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['Nissan'], name='Nissan', marker_color=clrs[4])
        TeslaBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['Tesla'], name='Tesla', marker_color=clrs[5])
        ToyotaBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['Toyota'], name='Toyota', marker_color=clrs[6])
        VWBars = go.Bar(x=dfSIO[attLower + '_1'], y=dfSIO['VW'], name='VW', marker_color=clrs[7])
        dataUse = [AudiBars, ChevroletBars, JaguarBars, KiaBars, NissanBars, TeslaBars, ToyotaBars, VWBars]

    SIOfigure = {
        'data': dataUse,
        'layout': go.Layout(
            hovermode="closest",
            xaxis={'title': attribute + " Change", 'titlefont': {'color': 'black', 'size': 14},
                   'tickmode': 'array',
                   'tickvals': dfARPU[attLower + '_1'],
                   'ticktext': xText,
                   'tickfont': {'size': 9, 'color': 'black'}},
            yaxis={'title': "SIOs Change (Thousands)", 'titlefont': {'color': 'black', 'size': 14, },
                   'ticksuffix': 'K',
                   'tickfont': {'color': 'black'}}
        )
    }

    if aggView:
        ChevroletBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['Chevrolet'], name='Chevrolet', marker_color=clrs[1])
        JaguarBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['Jaguar'], name='Jaguar', marker_color=clrs[2])
        KiaBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['Kia'], name='Kia', marker_color=clrs[3])
        NissanBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['Nissan'], name='Nissan', marker_color=clrs[4])
        TeslaBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['Tesla'], name='Tesla', marker_color=clrs[5])
        ToyotaBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['Toyota'], name='Toyota', marker_color=clrs[6])
        VWBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['VW'], name='VW', marker_color=clrs[7])
        dataUse = [ChevroletBars, JaguarBars, KiaBars, NissanBars, TeslaBars, ToyotaBars, VWBars]
    else:
        AudiBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['Audi'], name='Audi', marker_color=clrs[0])
        ChevroletBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['Chevrolet'], name='Chevrolet', marker_color=clrs[1])
        JaguarBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['Jaguar'], name='Jaguar', marker_color=clrs[2])
        KiaBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['Kia'], name='Kia', marker_color=clrs[3])
        NissanBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['Nissan'], name='Nissan', marker_color=clrs[4])
        TeslaBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['Tesla'], name='Tesla', marker_color=clrs[5])
        ToyotaBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['Toyota'], name='Toyota', marker_color=clrs[6])
        VWBars = go.Bar(x=dfARPU[attLower + '_1'], y=dfARPU['VW'], name='VW', marker_color=clrs[7])
        dataUse = [AudiBars, ChevroletBars, JaguarBars, KiaBars, NissanBars, TeslaBars, ToyotaBars, VWBars]

    ARPUfigure = {
        'data': dataUse,
        'layout': go.Layout(
            hovermode="closest",
            xaxis={'title': attribute + " Change", 'titlefont': {'color': 'black', 'size': 14},
                   'tickmode': 'array',
                   'tickvals': dfARPU[attLower + '_1'],
                   'ticktext': xText,
                   'tickfont': {'size': 9, 'color': 'black'}},
            yaxis={'title': "ARPU Change", 'titlefont': {'color': 'black', 'size': 14, },
                   'tickprefix': '$',
                   'tickfont': {'color': 'black'}}
        )
    }

    if aggView:
        ChevroletBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['Chevrolet'], name='Chevrolet',
                               marker_color=clrs[1])
        JaguarBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['Jaguar'], name='Jaguar', marker_color=clrs[2])
        KiaBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['Kia'], name='Kia', marker_color=clrs[3])
        NissanBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['Nissan'], name='Nissan', marker_color=clrs[4])
        TeslaBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['Tesla'], name='Tesla', marker_color=clrs[5])
        ToyotaBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['Toyota'], name='Toyota', marker_color=clrs[6])
        VWBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['VW'], name='VW', marker_color=clrs[7])
        dataUse = [ChevroletBars, JaguarBars, KiaBars, NissanBars, TeslaBars, ToyotaBars, VWBars]
    else:
        AudiBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['Audi'], name='Audi', marker_color=clrs[0])
        ChevroletBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['Chevrolet'], name='Chevrolet',
                               marker_color=clrs[1])
        JaguarBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['Jaguar'], name='Jaguar', marker_color=clrs[2])
        KiaBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['Kia'], name='Kia', marker_color=clrs[3])
        NissanBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['Nissan'], name='Nissan', marker_color=clrs[4])
        TeslaBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['Tesla'], name='Tesla', marker_color=clrs[5])
        ToyotaBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['Toyota'], name='Toyota', marker_color=clrs[6])
        VWBars = go.Bar(x=dfRevenue[attLower + '_1'], y=dfRevenue['VW'], name='VW', marker_color=clrs[7])
        dataUse = [AudiBars, ChevroletBars, JaguarBars, KiaBars, NissanBars, TeslaBars, ToyotaBars, VWBars]

    RevenueFigure = {
        'data': dataUse,
        'layout': go.Layout(
            hovermode="closest",
            xaxis={'title': attribute + " Change", 'titlefont': {'color': 'black', 'size': 14},
                   'tickmode': 'array',
                   'tickvals': dfRevenue[attLower + '_1'],
                   'ticktext': xText,
                   'tickfont': {'size': 9, 'color': 'black'}},
            yaxis={'title': "Revenue Change (per month)", 'titlefont': {'color': 'black', 'size': 14, },
                   'tickprefix': '$',
                   'ticksuffix': 'K',
                   'tickfont': {'color': 'black'}}
        )
    }

    if aggView:
        ChevroletBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['Chevrolet'], name='Chevrolet', marker_color=clrs[1])
        JaguarBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['Jaguar'], name='Jaguar', marker_color=clrs[2])
        KiaBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['Kia'], name='Kia', marker_color=clrs[3])
        NissanBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['Nissan'], name='Nissan', marker_color=clrs[4])
        TeslaBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['Tesla'], name='Tesla', marker_color=clrs[5])
        ToyotaBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['Toyota'], name='Toyota', marker_color=clrs[6])
        VWBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['VW'], name='VW', marker_color=clrs[7])
        dataUse = [ChevroletBars, JaguarBars, KiaBars, NissanBars, TeslaBars, ToyotaBars, VWBars]
    else:
        AudiBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['Audi'], name='Audi', marker_color=clrs[0])
        ChevroletBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['Chevrolet'], name='Chevrolet', marker_color=clrs[1])
        JaguarBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['Jaguar'], name='Jaguar', marker_color=clrs[2])
        KiaBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['Kia'], name='Kia', marker_color=clrs[3])
        NissanBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['Nissan'], name='Nissan', marker_color=clrs[4])
        TeslaBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['Tesla'], name='Tesla', marker_color=clrs[5])
        ToyotaBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['Toyota'], name='Toyota', marker_color=clrs[6])
        VWBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfEBIT['VW'], name='VW', marker_color=clrs[7])
        dataUse = [AudiBars, ChevroletBars, JaguarBars, KiaBars, NissanBars, TeslaBars, ToyotaBars, VWBars]

    EBITfigure = {
        'data': dataUse,
        'layout': go.Layout(
            hovermode="closest",
            xaxis={'title': attribute + " Change", 'titlefont': {'color': 'black', 'size': 14},
                   'tickmode': 'array',
                   'tickvals': dfEBIT[attLower + '_1'],
                   'ticktext': xText,
                   'tickfont': {'size': 9, 'color': 'black'}},
            yaxis={'title': "EBIT Change (per month)", 'titlefont': {'color': 'black', 'size': 14, },
                   'tickprefix': '$',
                   'ticksuffix': 'K',
                   'tickfont': {'color': 'black'}}
        )
    }

    segVec = [None for x in range(len(segments))]
    for i, segment in enumerate(segments):
        dfUse = dfFlow[dfFlow['Segment'] == segment].iloc[:, :8]
        dfUse[provider] = dfUse[provider] - 1
        attCols = [col for col in dfUse.columns if attLower in col]
        if aggView:
            dfUseCopy = dfUse[attCols].copy()
            dfUseCopy['Chevrolet'] = dfUse['Chevrolet'].copy()
            dfUseCopy['Jaguar'] = dfUse['Jaguar'].copy()
            dfUseCopy['Kia'] = dfUse['Kia'].copy()
            dfUseCopy['Nissan'] = dfUse['Nissan'].copy()
            dfUseCopy['Tesla'] = dfUse['Tesla'].copy()
            dfUseCopy['Toyota'] = dfUse['Toyota'].copy()
            dfUseCopy['VW'] = dfUse['Audi'] + dfUse['VW']
            dfUseCopy = dfUseCopy.round(4)
            dfUse = dfUseCopy.copy()
            ChevroletBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['Chevrolet'], name='Chevrolet',
                                   marker_color=clrs[1])
            JaguarBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['Jaguar'], name='Jaguar', marker_color=clrs[2])
            KiaBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['Kia'], name='Kia', marker_color=clrs[3])
            NissanBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['Nissan'], name='Nissan', marker_color=clrs[4])
            TeslaBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['Tesla'], name='Tesla', marker_color=clrs[5])
            ToyotaBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['Toyota'], name='Toyota', marker_color=clrs[6])
            VWBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['VW'], name='VW', marker_color=clrs[7])
            dataUse = [ChevroletBars, JaguarBars, KiaBars, NissanBars, TeslaBars, ToyotaBars, VWBars]
        else:
            AudiBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['Audi'], name='Audi', marker_color=clrs[0])
            ChevroletBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['Chevrolet'], name='Chevrolet',
                                   marker_color=clrs[1])
            JaguarBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['Jaguar'], name='Jaguar', marker_color=clrs[2])
            KiaBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['Kia'], name='Kia', marker_color=clrs[3])
            NissanBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['Nissan'], name='Nissan', marker_color=clrs[4])
            TeslaBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['Tesla'], name='Tesla', marker_color=clrs[5])
            ToyotaBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['Toyota'], name='Toyota', marker_color=clrs[6])
            VWBars = go.Bar(x=dfEBIT[attLower + '_1'], y=dfUse['VW'], name='VW', marker_color=clrs[7])
            dataUse = [AudiBars, ChevroletBars, JaguarBars, KiaBars, NissanBars, TeslaBars, ToyotaBars, VWBars]


        segmentFigure = {
            'data': dataUse,
            'layout': go.Layout(
                hovermode="closest",
                title=segment,
                xaxis={'title': attribute + " Change", 'titlefont': {'color': 'black', 'size': 14},
                       'tickmode': 'array',
                       'tickvals': dfEBIT[attLower + '_1'],
                       'ticktext': xText,
                       'tickfont': {'size': 9, 'color': 'black'}},
                yaxis={'title': "Percentage Shift in Customers", 'titlefont': {'color': 'black', 'size': 14, },
                       'tickformat': ',.2%',
                       'tickfont': {'color': 'black'}}
            )
        }
        segVec[i] = segmentFigure

    if val is not None:
        if attLower == "monthly":
            val = int(val[1:len(val)-3])
        elif attLower == "upfront":
            val = int(val[1:])
        uniqXval = np.array(dfFlow[attLower + '_1'].unique())
        #print(uniqXval)
        indCalc = np.where(uniqXval == val)[0]

        # in case where grid has changed, need to update calculations before updating plots
        if len(indCalc) == 0:
            raise PreventUpdate

        index = indCalc[0]
    else:
        index = 0
    yVal = dfFlow[attLower + '_1'].unique()[index]
    xVal = [x for x in range(len(segments))]
    if aggView:
        attCols = [col for col in dfFlow.columns if attLower in col]
        dfFlowCopy = dfFlow[attCols].copy()
        dfFlowCopy['Chevrolet'] = dfFlow['Chevrolet'].copy()
        dfFlowCopy['Jaguar'] = dfFlow['Jaguar'].copy()
        dfFlowCopy['Kia'] = dfFlow['Kia'].copy()
        dfFlowCopy['Nissan'] = dfFlow['Nissan'].copy()
        dfFlowCopy['Tesla'] = dfFlow['Tesla'].copy()
        dfFlowCopy['Toyota'] = dfFlow['Toyota'].copy()
        dfFlowCopy['VW'] = dfFlow['Audi'] + dfFlow['VW']
        dfFlowCopy = dfFlowCopy.round(6)
        if provider == 'Audi':
            dfFlowCopy['VW'] = dfFlowCopy['VW'] - 1
        else:
            dfFlowCopy[provider] = dfFlowCopy[provider] - 1
        ChevroletBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['Chevrolet'],
                               name='Chevrolet', marker_color=clrs[1])
        JaguarBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['Jaguar'],
                            name='Jaguar', marker_color=clrs[2])
        KiaBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['Kia'],
                         name='Kia', marker_color=clrs[3])
        NissanBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['Nissan'],
                            name='Nissan', marker_color=clrs[4])
        TeslaBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['Tesla'],
                           name='Tesla', marker_color=clrs[5])
        ToyotaBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['Toyota'],
                            name='Toyota', marker_color=clrs[6])
        VWBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['VW'],
                        name='VW', marker_color=clrs[7])
        dataUse = [ChevroletBars, JaguarBars, KiaBars, NissanBars, TeslaBars, ToyotaBars, VWBars]
    else:
        dfFlowCopy = dfFlow.copy()
        dfFlowCopy = dfFlowCopy.round(6)
        dfFlowCopy[provider] = dfFlowCopy[provider] - 1
        AudiBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['Audi'],
                          name='Audi', marker_color=clrs[0])
        ChevroletBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['Chevrolet'],
                               name='Chevrolet', marker_color=clrs[1])
        JaguarBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['Jaguar'],
                            name='Jaguar', marker_color=clrs[2])
        KiaBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['Kia'],
                         name='Kia', marker_color=clrs[3])
        NissanBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['Nissan'],
                            name='Nissan', marker_color=clrs[4])
        TeslaBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['Tesla'],
                           name='Tesla', marker_color=clrs[5])
        ToyotaBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['Toyota'],
                            name='Toyota', marker_color=clrs[6])
        VWBars = go.Bar(x=xVal, y=dfFlowCopy[dfFlowCopy[attLower + '_1'] == yVal]['VW'],
                        name='VW', marker_color=clrs[7])
        dataUse = [AudiBars, ChevroletBars, JaguarBars, KiaBars, NissanBars, TeslaBars, ToyotaBars, VWBars]

    segmentFigure = {
        'data': dataUse,
        'layout': go.Layout(
            hovermode="closest",
            xaxis={'title': attribute + " Change", 'titlefont': {'color': 'black', 'size': 14},
                   'tickmode': 'array',
                   'tickvals': xVal,
                   'ticktext': segments,
                   'tickfont': {'size': 9, 'color': 'black'}},
            yaxis={'title': "Percentage Shift in Customers", 'titlefont': {'color': 'black', 'size': 14, },
                   'tickformat': ',.2%',
                   'tickfont': {'color': 'black'}}
        )
    }

    return SIOfigure, ARPUfigure, RevenueFigure, EBITfigure, segVec[0], segVec[1], segVec[2], segmentFigure
