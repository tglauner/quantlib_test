import QuantLib as ql
import pandas as pd

def build_sofr_curve(today, sofr_rates):
    dates = [today + ql.Period(i+1, ql.Years) for i in range(len(sofr_rates))]
    helpers = [ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(rate/100)),
                                    ql.Period(1, ql.Years), 2,
                                    ql.UnitedStates(), ql.ModifiedFollowing,
                                    False, ql.Actual360()) for rate in sofr_rates]
    curve = ql.PiecewiseLinearZero(today, helpers, ql.Actual360())
    return curve

def create_swap(start, maturity, rate, curve):
    fixed_leg_tenor = ql.Period('1Y')
    fixed_schedule = ql.Schedule(start, maturity, fixed_leg_tenor, ql.UnitedStates(),
                                 ql.ModifiedFollowing, ql.ModifiedFollowing,
                                 ql.DateGeneration.Forward, False)
    float_schedule = fixed_schedule
    swap = ql.VanillaSwap(ql.VanillaSwap.Payer, 1000000,
                          fixed_schedule, rate/100, ql.Thirty360(),
                          float_schedule, ql.Sofr(curve), 0.0, ql.Actual360())
    engine = ql.DiscountingSwapEngine(ql.YieldTermStructureHandle(curve))
    swap.setPricingEngine(engine)
    return swap

def create_european_swaption(swap, curve, exercise_date):
    exercise = ql.EuropeanExercise(exercise_date)
    swaption = ql.Swaption(swap, exercise)
    model = ql.BlackSwaptionEngine(ql.YieldTermStructureHandle(curve), 0.01)
    swaption.setPricingEngine(model)
    return swaption

def create_bermudan_swaption(swap, curve, exercise_dates):
    exercise = ql.BermudanExercise(exercise_dates)
    swaption = ql.Swaption(swap, exercise)
    model = ql.BlackSwaptionEngine(ql.YieldTermStructureHandle(curve), 0.01)
    swaption.setPricingEngine(model)
    return swaption

def price_portfolio(sofr_rates):
    today = ql.Date.todaysDate()
    ql.Settings.instance().evaluationDate = today
    curve = build_sofr_curve(today, sofr_rates)

    swap = create_swap(today, today + ql.Period(5, ql.Years), 3.0, curve)
    european_swaption = create_european_swaption(
        swap, curve, today + ql.Period(1, ql.Years))
    bermudan_dates = [today + ql.Period(i, ql.Years) for i in range(1, 4)]
    bermudan_swaption = create_bermudan_swaption(swap, curve, bermudan_dates)

    securities = [
        {'Type': 'Swap', 'NPV': swap.NPV()},
        {'Type': 'European Swaption', 'NPV': european_swaption.NPV()},
        {'Type': 'Bermudan Swaption', 'NPV': bermudan_swaption.NPV()}
    ]
    return pd.DataFrame(securities)
