import akshare as ak

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties

# 设置中文字体
font_path = '/Users/hierifer/Downloads/MiSans/ttf/MiSans-Demibold.ttf'
plt.rcParams['font.family'] = 'MiSans'
plt.rcParams['axes.unicode_minus'] = False
font_prop = FontProperties(fname=font_path)

def calculate_rsi(data, period=14):
    """计算RSI指标"""
    data = data.copy()
    # 计算价格变化
    delta = data['收盘'].diff()
    
    # 分离上涨和下跌
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # 计算平均上涨和下跌
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    # 计算相对强度(RS)
    rs = avg_gain / avg_loss
    
    # 计算RSI
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # 添加超买超卖线
    data['超买线'] = 70
    data['超卖线'] = 30
    
    return data

def backtest_rsi_strategy_with_capital(data, initial_capital=100000, trade_volume=100, commission_rate=0.0003, rsi_period=14, overbought=70, oversold=30):
    """带资金管理的RSI策略回测"""
    # 初始化列
    data = data.copy()
    data['signal'] = 0
    data['position'] = 0
    data['cash'] = initial_capital
    data['stock_value'] = 0.0
    data['total_asset'] = initial_capital
    data['trade_amount'] = 0.0
    
    # 计算RSI指标
    data = calculate_rsi(data, rsi_period)
    
    for i in range(1, len(data)):
        # 获取前一天和当天的数据
        prev_row = data.iloc[i-1]
        current_row = data.iloc[i]
        
        # 初始化当天值
        data.iloc[i, data.columns.get_loc('position')] = prev_row['position']
        data.iloc[i, data.columns.get_loc('cash')] = prev_row['cash']
        data.iloc[i, data.columns.get_loc('signal')] = 0
        data.iloc[i, data.columns.get_loc('trade_amount')] = 0
        
        # 超卖区域后回升，买入信号
        if i >= 2 and prev_row['RSI'] > oversold and data.iloc[i-2]['RSI'] <= oversold:
            current_open = current_row['开盘']
            buy_cost = current_open * trade_volume * (1 + commission_rate)
            
            if prev_row['cash'] >= buy_cost:
                data.iloc[i, data.columns.get_loc('signal')] = 1
                data.iloc[i, data.columns.get_loc('position')] = prev_row['position'] + trade_volume
                data.iloc[i, data.columns.get_loc('cash')] = prev_row['cash'] - buy_cost
                data.iloc[i, data.columns.get_loc('trade_amount')] = -buy_cost
        
        # 超买区域后回落，卖出信号
        elif i >= 2 and prev_row['RSI'] < overbought and data.iloc[i-2]['RSI'] >= overbought:
            if prev_row['position'] >= trade_volume:
                current_open = current_row['开盘']
                sell_revenue = current_open * trade_volume * (1 - commission_rate)
                
                data.iloc[i, data.columns.get_loc('signal')] = -1
                data.iloc[i, data.columns.get_loc('position')] = prev_row['position'] - trade_volume
                data.iloc[i, data.columns.get_loc('cash')] = prev_row['cash'] + sell_revenue
                data.iloc[i, data.columns.get_loc('trade_amount')] = sell_revenue
        
        # 计算当天股票市值和总资产
        current_close = current_row['收盘']
        data.iloc[i, data.columns.get_loc('stock_value')] = data.iloc[i, data.columns.get_loc('position')] * current_close
        data.iloc[i, data.columns.get_loc('total_asset')] = data.iloc[i, data.columns.get_loc('cash')] + data.iloc[i, data.columns.get_loc('stock_value')]
    
    return data

# 填写股票代码
stock_code = "601318"  # 示例：中国平安
start_date = "20230101"
end_date = "20231231"
stock_df = ak.stock_zh_a_hist(symbol=stock_code, start_date=start_date, end_date=end_date, adjust="hfq")
stock_df.index = pd.to_datetime(stock_df['日期'])

# 执行回测
initial_capital = 100000
trade_volume = 100
rsi_period = 14
overbought = 70
oversold = 30

result_df = backtest_rsi_strategy_with_capital(
    stock_df, 
    initial_capital, 
    trade_volume, 
    rsi_period=rsi_period, 
    overbought=overbought, 
    oversold=oversold
)

result_df.to_excel('RSI.xlsx')

# 分析结果
final_asset = result_df['total_asset'].iloc[-1]
total_return = (final_asset - initial_capital) / initial_capital
annualized_return = (1 + total_return) ** (252/len(result_df)) - 1

# 打印交易记录
trade_records = result_df[result_df['signal'] != 0]
print("\n=== 交易记录 ===")
print(trade_records[['开盘', '收盘', 'RSI', 'signal', 'position', 'cash', 'stock_value', 'total_asset']])

print("\n=== 策略绩效 ===")
print(f"RSI参数: 周期={rsi_period}, 超买={overbought}, 超卖={oversold}")
print(f"初始资金: {initial_capital:,.2f}元")
print(f"最终总资产: {final_asset:,.2f}元")
print(f"总收益率: {total_return:.2%}")
print(f"年化收益率: {annualized_return:.2%}")
print(f"交易次数: {len(trade_records)}次")
print(f"最终持仓: {result_df['position'].iloc[-1]:,}股")
print(f"最终现金: {result_df['cash'].iloc[-1]:,.2f}元")
print(f"最终股票市值: {result_df['stock_value'].iloc[-1]:,.2f}元")

# 可视化
plt.figure(figsize=(14, 12))

# 价格和RSI指标
ax1 = plt.subplot(3, 1, 1)
plt.plot(result_df['收盘'], label='收盘价', color='b')
plt.title(f'中国平安({stock_code})RSI策略回测', fontproperties=font_prop, pad=20)
plt.legend(loc='upper left', prop=font_prop)

ax2 = ax1.twinx()
plt.plot(result_df['RSI'], label='RSI指标', color='orange', linewidth=2)
plt.plot(result_df['超买线'], label='超买线(70)', color='red', linestyle='--')
plt.plot(result_df['超卖线'], label='超卖线(30)', color='green', linestyle='--')
plt.fill_between(result_df.index, result_df['RSI'], 70, 
                where=(result_df['RSI'] >= 70), 
                color='red', alpha=0.3)
plt.fill_between(result_df.index, result_df['RSI'], 30, 
                where=(result_df['RSI'] <= 30), 
                color='green', alpha=0.3)
plt.ylim(0, 100)
plt.legend(loc='upper right', prop=font_prop)

# 买卖信号
plt.subplot(3, 1, 2)
plt.plot(result_df['收盘'], label='收盘价', color='b', alpha=0.3)
buy_signals = result_df[result_df['signal'] == 1]
sell_signals = result_df[result_df['signal'] == -1]
plt.scatter(buy_signals.index, buy_signals['收盘'], label='买入信号(RSI超卖回升)', marker='^', color='red', alpha=1)
plt.scatter(sell_signals.index, sell_signals['收盘'], label='卖出信号(RSI超买回落)', marker='v', color='green', alpha=1)
plt.legend(prop=font_prop)

# 资产变化
plt.subplot(3, 1, 3)
plt.plot(result_df['total_asset'], label='总资产', color='purple')
plt.plot(result_df['stock_value'], label='股票市值', color='green', linestyle='--')
plt.plot(result_df['cash'], label='现金', color='blue', linestyle=':')
plt.legend(prop=font_prop)

plt.tight_layout()
plt.show()



