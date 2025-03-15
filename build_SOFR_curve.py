import QuantLib as ql
import pandas as pd
from datetime import datetime, timedelta

def build_sofr_curve():
    # Set evaluation date
    today = ql.Date().todaysDate()
    ql.Settings.instance().evaluationDate = today

    # Define SOFR overnight rate
    sofr_rate = 0.05  # 5% overnight rate
    overnight_quote = ql.SimpleQuote(sofr_rate)
    flat_forward = ql.FlatForward(today, ql.QuoteHandle(overnight_quote), ql.Actual360())
    overnight_handle = ql.YieldTermStructureHandle(flat_forward)
    overnight_index = ql.OvernightIndex("SOFR", 0, ql.USDCurrency(), ql.NullCalendar(), ql.Actual360(), overnight_handle)


    # Define SOFR swap rates (assume market data)
    swap_maturities = [1, 2, 3, 5, 7, 10, 15, 20, 30]  # Years
    swap_rates = [0.051, 0.053, 0.055, 0.057, 0.059, 0.06, 0.062, 0.064, 0.065]  # Corresponding SOFR swap rates

    # Convert to deposit and swap helpers
    rate_helpers = [ql.OISRateHelper(2, ql.Period("1D"), ql.QuoteHandle(overnight_quote), overnight_index)]

    for tenor, rate in zip(swap_maturities, swap_rates):
        swap_quote = ql.SimpleQuote(rate)
        swap_handle = ql.QuoteHandle(swap_quote)
        swap_helper = ql.OISRateHelper(2, ql.Period(tenor, ql.Years), swap_handle, overnight_index)
        rate_helpers.append(swap_helper)

    # Build SOFR curve
    sofr_curve = ql.PiecewiseLogCubicDiscount(today, rate_helpers, ql.Actual360())

    # Convert to term structure handle
    sofr_handle = ql.YieldTermStructureHandle(sofr_curve)

    return sofr_handle

today = ql.Date().todaysDate()
ql.Settings.instance().evaluationDate = today
sofr_handle = build_sofr_curve()

# Print discount factors for different maturities
print("SOFR Discount Factors:")
for years in [1, 2, 5, 10, 20, 30]:
    date = today + ql.Period(years, ql.Years)
    discount_factor = sofr_handle.discount(date)
    print(f"{years}Y: {discount_factor:.6f}")

# Generate daily discount factors for one year
dates, discount_factors = [], []
for day_offset in range(366):
    date = today + day_offset
    dates.append(datetime(date.year(), date.month(), date.dayOfMonth()))
    discount_factors.append(sofr_handle.discount(date))

# Create DataFrame
df_daily = pd.DataFrame({'Date': dates, 'Discount Factor': discount_factors})

# Display DataFrame to user
print(df_daily.head())

