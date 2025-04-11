import backtrader as bt
import pandas as pd

# Создаём стратегию
class STLStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.trend = self.datas[0].trend

        # Добавляем тренд как индикатор для отображения на графике
        self.trend_plot = TrendIndicator(self.datas[0], plotmaster=self.datas[0])

    def next(self):
        if not self.position:
            if self.dataclose[0] < self.trend[0]:
                self.buy()
        else:
            if self.dataclose[0] > self.trend[0]:
                self.sell()

# Класс DataFeed с добавленным трендом
class PandasWithTrend(bt.feeds.PandasData):
    lines = ('trend',)
    params = (('trend', -1),)

class TrendIndicator(bt.Indicator):
    lines = ('trend',)
    plotlines = dict(trend=dict(color='orange', linewidth=2, linestyle='--'))

    def __init__(self):
        self.lines.trend = self.data.trend



# Загружаем данные
data = pd.read_csv('data/spx_bt.csv', index_col='Date', parse_dates=True)
datafeed = PandasWithTrend(dataname=data)

# Настраиваем "движок"
cerebro = bt.Cerebro()
cerebro.addstrategy(STLStrategy)
cerebro.adddata(datafeed)
cerebro.broker.setcash(100000.0)

# Запускаем
print(f'Начальный капитал: {cerebro.broker.getvalue():.2f}')
cerebro.run()
print(f'Конечный капитал: {cerebro.broker.getvalue():.2f}')

# Отображение
cerebro.plot()
