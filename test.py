import pandas as pd 
import time

tuple_cur = ('CNY', 'HKD', 'USD')

def get_trans(date, account):
    #读取交易数据
    df_trans_all = pd.read_excel('A_Shares.xlsx',sheet_name='Trans')
    df_trans_all['Date'] = df_trans_all[['Date','Symbol_Code']].astype(str)
    df_trans = df_trans_all[df_trans_all['Date'] <= date]
    df_trans = df_trans[df_trans['Account'].isin(account)]
    df_trans = df_trans.round(4)
    return df_trans

def get_cost(code, qt, df):
    df_code = df[df['Symbol_Code'].isin([code])]
    df_code.sort_values(by = ['Date'],axis = 0,ascending = False, inplace=True)
    
    #从当前持仓日往前取买入即分红送股数据获取成本金额
    #直至当前持仓数量扣除完整为止
    amt_cost = 0
    for i in df_code.index.tolist():
        if qt <= 0:
            break
        else:
            qt_trans = df_code.loc[i,'Quantity']
            amt_trans =  df_code.loc[i,'Settle_Amt']
            amt_cost = amt_cost + (amt_trans * (qt/qt_trans if qt_trans>qt else 1)) * -1
            qt = qt - qt_trans
    
    return amt_cost

     
def get_holding(date, df_trans):
    #取股票持仓
    df_trans_stock = df_trans[~df_trans['Symbol_Code'].isin(tuple_cur)]
    df_group_stock = df_trans_stock.loc[:, ['Symbol_Code', 'Symbol_Name', 'Cur', 'Quantity']]
    df_group_stock = df_group_stock.groupby(['Symbol_Code', 'Symbol_Name', 'Cur']).sum()
    df_group_stock = df_group_stock.reset_index()
    df_group_stock.drop(index=(df_group_stock.loc[(df_group_stock['Quantity']==0)].index), inplace=True)
    df_group_stock['Date'] = date
    
    #取持仓股票成本
    df_trans_buy = df_trans_stock[df_trans_stock['Quantity']>=0]
    df_group_stock['Cost_Amt'] = float(0)
    for i in df_group_stock.index.tolist():
        code = df_group_stock.loc[i,'Symbol_Code']
        hold_quantity = df_group_stock.loc[i,'Quantity']
        if hold_quantity > 0:
            cost_amt = get_cost(code, hold_quantity, df_trans_buy)
            df_group_stock.at[i, 'Cost_Amt'] = cost_amt

    #取现金持仓
    df_trans_cur = df_trans
    df_group_cur = df_trans_cur.loc[:, ['Cur', 'Settle_Amt']]
    df_group_cur = df_group_cur.groupby(['Cur']).sum()
    df_group_cur = df_group_cur.reset_index()
    df_group_cur['Date'] = date
    df_group_cur['Symbol_Code'] = df_group_cur['Cur']
    df_group_cur['Symbol_Name'] = df_group_cur['Cur']
    df_group_cur.rename(columns={'Settle_Amt':'Quantity'}, inplace=True)
    df_group_cur['Cost_Amt'] = df_group_cur['Quantity']
    
    #合并资金及股票持仓
    df_hold = df_group_stock.append(df_group_cur, ignore_index=True)
    df_hold = df_hold.round(4)
    df_hold.sort_values(by = ['Cur', 'Symbol_Code'],axis = 0,ascending = True, inplace=True)
    
    #获取行业信息
    df_sector = pd.read_excel('A_Shares.xlsx',sheet_name='Sector')
    df_hold = pd.merge(df_hold, df_sector, how='left')
    df_hold = df_hold[['Date','Symbol_Code', 'Symbol_Name', 'Sector', 'Cur', 'Quantity', 'Cost_Amt']]
    
    return df_hold


##############################################################################

trade_date = '20190814'
trade_date = time.strftime('%Y%m%d')

account_id = 'All'
if account_id == 'All':
    account_id = ['CMS', 'Citic']
else:
    account_id = [account_id]

trans_date = get_trans(trade_date, account_id)
hold = get_holding(trade_date, trans_date)
print(hold)


