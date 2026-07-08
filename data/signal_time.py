from datetime import datetime

# Stock -> Signal Time
signal_times = {}


def update_signal_time(stock, signal):

    # केवल BUY Signals के लिए Time Save होगा
    if signal not in ["🟢 BUY CE", "🔴 BUY PE"]:
        return "-"

    # अगर पहली बार Signal आया है
    if stock not in signal_times:

        signal_times[stock] = datetime.now().strftime("%H:%M")

    return signal_times[stock]


def get_signal_time(stock):

    return signal_times.get(stock, "-")