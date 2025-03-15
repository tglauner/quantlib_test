import QuantLib as ql

# Set today's date
today = ql.Date().todaysDate()
ql.Settings.instance().evaluationDate = today

# Market data
flat_curve_rate = 0.01
yield_curve = ql.YieldTermStructureHandle(ql.FlatForward(today, flat_curve_rate, ql.Actual365Fixed()))

# Hull-White model
hw_model = ql.HullWhite(yield_curve)

# Swaption details
exercise_dates = [today + ql.Period(i, ql.Years) for i in range(1, 6)]
exercise = ql.BermudanExercise(exercise_dates)

# Corrected Swaption Engine
swaption_engine = ql.TreeSwaptionEngine(hw_model, 50)


# Define a swap (a simple placeholder, modify as needed)
fixed_leg = ql.Schedule(today, today + ql.Period(5, ql.Years), ql.Period(ql.Annual), ql.NullCalendar(), ql.Unadjusted, ql.Unadjusted, ql.DateGeneration.Forward, False)
floating_leg = ql.Schedule(today, today + ql.Period(5, ql.Years), ql.Period(ql.Annual), ql.NullCalendar(), ql.Unadjusted, ql.Unadjusted, ql.DateGeneration.Forward, False)

notional = 1000000
fixed_rate = 0.02
spread = 0.0
index = ql.Euribor6M(yield_curve)
day_count = ql.Actual360()

swap = ql.VanillaSwap(ql.VanillaSwap.Payer, notional, fixed_leg, fixed_rate, day_count, floating_leg, index, spread, day_count)

# Create Swaption
swaption = ql.Swaption(swap, exercise)
swaption.setPricingEngine(swaption_engine)

# Print result
print(f"Bermudan Swaption NPV: {swaption.NPV()}")
