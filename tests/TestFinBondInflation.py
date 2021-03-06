##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################

import sys
sys.path.append("..//..//")

from FinTestCases import FinTestCases, globalTestCaseMode
from financepy.finutils.FinFrequency import FinFrequencyTypes
from financepy.finutils.FinDayCount import FinDayCountTypes
from financepy.finutils.FinDate import FinDate
from financepy.products.bonds.FinBondInflation import FinBondInflation
from financepy.products.bonds import FinYTMCalcType

testCases = FinTestCases(__file__, globalTestCaseMode)

##########################################################################

##########################################################################
# https://data.bloomberglp.com/bat/sites/3/2017/07/SF-2017_Paul-Fjeldsted.pdf
# Page 10 TREASURY NOTE SCREENSHOT
##########################################################################

def test_FinInflationBond():

    testCases.banner("BLOOMBERG US TIPS EXAMPLE")
    settlementDate = FinDate(21, 7, 2017)
    issueDate = FinDate(15, 7, 2010)
    maturityDate = FinDate(15, 7, 2020)
    coupon = 0.0125
    freqType = FinFrequencyTypes.SEMI_ANNUAL
    accrualType = FinDayCountTypes.ACT_ACT_ICMA
    face = 100.0

    bond = FinBondInflation(issueDate,
                            maturityDate,
                            coupon,
                            freqType,
                            accrualType,
                            face)

    testCases.header("FIELD", "VALUE")
    cleanPrice = 104.03502

    yld = bond.currentYield(cleanPrice)
    testCases.print("Current Yield = ", yld)

    ###########################################################################
    # Inherited functions that just calculate real yield without CPI adjustments
    ###########################################################################

    ytm = bond.yieldToMaturity(settlementDate, cleanPrice,
                               FinYTMCalcType.UK_DMO)
    testCases.print("UK DMO REAL Yield To Maturity = ", ytm)

    ytm = bond.yieldToMaturity(settlementDate, cleanPrice,
                               FinYTMCalcType.US_STREET)
    testCases.print("US STREET REAL Yield To Maturity = ", ytm)

    ytm = bond.yieldToMaturity(settlementDate, cleanPrice,
                               FinYTMCalcType.US_TREASURY)
    testCases.print("US TREASURY REAL Yield To Maturity = ", ytm)

    fullPrice = bond.fullPriceFromYTM(settlementDate, ytm)
    testCases.print("Full Price from REAL YTM = ", fullPrice)

    cleanPrice = bond.cleanPriceFromYTM(settlementDate, ytm)
    testCases.print("Clean Price from Real YTM = ", cleanPrice)

    accd = bond._accruedInterest
    testCases.print("REAL Accrued Interest = ", accd)

    ###########################################################################
    # Inflation functions that calculate nominal yield with CPI adjustment
    ###########################################################################

    baseCPIValue = 218.08532
    refCPIValue = 244.65884

    ytm = bond.nominalYieldToMaturity(settlementDate, cleanPrice,
                                      baseCPIValue, refCPIValue,
                                      FinYTMCalcType.UK_DMO)

    testCases.print("UK DMO REAL Yield To Maturity = ", ytm)

    ytm = bond.nominalYieldToMaturity(settlementDate, cleanPrice,
                                      baseCPIValue, refCPIValue,
                                      FinYTMCalcType.US_STREET)

    testCases.print("US STREET REAL Yield To Maturity = ", ytm)

    ytm = bond.nominalYieldToMaturity(settlementDate, cleanPrice,
                                      baseCPIValue, refCPIValue,
                                      FinYTMCalcType.US_TREASURY)

    testCases.print("US TREASURY REAL Yield To Maturity = ", ytm)


    accd = bond._accruedInterest
    testCases.print("Accrued = ", accd)

    accddays = bond._accruedDays
    testCases.print("Accrued Days = ", accddays)

    duration = bond.dollarDuration(settlementDate, ytm)
    testCases.print("Dollar Duration = ", duration)

    modifiedDuration = bond.modifiedDuration(settlementDate, ytm)
    testCases.print("Modified Duration = ", modifiedDuration)

    macauleyDuration = bond.macauleyDuration(settlementDate, ytm)
    testCases.print("Macauley Duration = ", macauleyDuration)

    conv = bond.convexityFromYTM(settlementDate, ytm)
    testCases.print("Convexity = ", conv)

##########################################################################


test_FinInflationBond()
testCases.compareTestCases()
