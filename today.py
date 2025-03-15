import QuantLib as ql

# Fix for today's date
today = ql.Date().todaysDate()
ql.Settings.instance().evaluationDate = today

print("Today's Date in QuantLib:", today)
