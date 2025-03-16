from flask import Flask, render_template, request
from portfolio import price_portfolio

app = Flask(__name__)

DEFAULT_RATES = [5.0, 5.1, 5.2, 5.3, 5.4]

@app.route('/', methods=['GET', 'POST'])
def blotter():
    sofr_rates = DEFAULT_RATES.copy()
    if request.method == 'POST':
        sofr_rates = [float(request.form.get(f'rate{i}', sofr_rates[i])) for i in range(len(sofr_rates))]

    df = price_portfolio(sofr_rates)
    return render_template('blotter.html', tables=[df.to_html(classes='data', header=True)],
                           sofr_rates=sofr_rates)

if __name__ == '__main__':
    app.run(debug=True)
