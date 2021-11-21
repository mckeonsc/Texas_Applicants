import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import scipy.stats as stats 

#win loss records for texas, am and texas tech
ut_url = 'https://en.wikipedia.org/wiki/List_of_Texas_Longhorns_football_seasons'
am_url = 'https://en.wikipedia.org/wiki/List_of_Texas_A%26M_Aggies_football_seasons'
tt_url = 'https://en.wikipedia.org/wiki/List_of_Texas_Tech_Red_Raiders_football_seasons'
#excel files for applicants to texas, am and texas tech
am_00to08 = pd.read_excel(r'C:\Users\j513991\Desktop\Week4\am_00to08.xlsx')
am_09to18 = pd.read_excel(r'C:\Users\j513991\Desktop\Week4\AM_09to18.xlsx')
tt_00to08 = pd.read_excel(r'C:\Users\j513991\Desktop\Week4\tt_00to08.xlsx')
tt_09to18 = pd.read_excel(r'C:\Users\j513991\Desktop\Week4\TT_09to18.xlsx')
ut_00to08 = pd.read_excel(r'C:\Users\j513991\Desktop\Week4\ut_00to08.xlsx')
ut_09to18 = pd.read_excel(r'C:\Users\j513991\Desktop\Week4\UT_09to18.xlsx')
#clean urls and extract a win loss ratio
def url_clean(url):
    df = pd.read_html(url,header=0)[0]
    df.columns = [x.strip().lower() for x in df.columns]
    cols_keep = ['year','overall']
    df = df[cols_keep]
    df['year']=df['year'].replace('[A-Z].*',np.nan,regex=True)
    df.dropna(inplace=True)
    df = df.loc[(df['year']>='2000') & (df['year']<'2019')]
    df['split'] = df['overall'].str.split('–')
    df['win'] = [np.float64(x[0]) for x in df['split'].values]
    df['loss'] = [np.float64(x[1]) for x in df['split'].values]
    df['ratio'] = df['win']/(df['win']+df['loss'])
    return df

#extract texas applicants and total applicants for years 2000 to 2008
def data_clean8(df):
    df.rename(columns = {'Unnamed: 1':'Resident','Unnamed: 2':'Resident Totals'}, inplace=True)
    cols_keep = ['Resident','Resident Totals']
    df = df[cols_keep]
    df.dropna(inplace=True)
    rows_keep = ['Texas Resident','Total']
    df = df[df['Resident'].isin(rows_keep)==True]
    df['Resident Totals'] = df['Resident Totals'].astype('int')
    df_texres = df[df['Resident']=='Texas Resident']
    df_tot = df[df['Resident']=='Total']
    df_texres['Resident Totals'] = df_texres['Resident Totals'].nlargest(9)
    df_texres.dropna(inplace=True)
    years = [2008,2007,2006,2005,2004,2003,2002,2001,2000]
    df_texres['year'] = years
    df_tot['Resident Totals'] = df_tot['Resident Totals'].nlargest(9)
    df_tot.dropna(inplace=True)
    df_tot['year'] = years
    #merge dataframes to create one large dataframe
    df = df_texres.merge(df_tot,how='inner',on='year')
    return df

#extract texas applicants and total applicants for years 2009 to 2018
def data_clean18(df):
    df.rename(columns = {'Unnamed: 1':'Resident','Unnamed: 2':'Resident Totals'}, inplace=True)
    cols_keep = ['Resident','Resident Totals']
    df = df[cols_keep]
    df.dropna(inplace=True)
    rows_keep = ['Texas Resident','Total']
    df = df[df['Resident'].isin(rows_keep)==True]
    df['Resident Totals'] = df['Resident Totals'].astype('int')
    df_texres = df[df['Resident']=='Texas Resident']
    df_tot = df[df['Resident']=='Total']
    df_texres['Resident Totals'] = df_texres['Resident Totals'].nlargest(10)
    df_texres.dropna(inplace=True)
    years = [2018,2017,2016,2015,2014,2013,2012,2011,2010,2009]
    df_texres['year'] = years
    df_tot['Resident Totals'] = df_tot['Resident Totals'].nlargest(10)
    df_tot.dropna(inplace=True)
    df_tot['year'] = years
    #merge dataframes to create one large dataframe
    df = df_texres.merge(df_tot,how='inner',on='year')
    return df

#merge dataframes for each school so that all years are together
def merge_sort(df1,df2):
    df_apps = df1.merge(df2,how='outer')
    df_apps.set_index('year',inplace=True)
    df_apps.sort_index(ascending=True,inplace=True)
    df_apps['Resident Totals_x'] = df_apps['Resident Totals_x'].apply(int)
    df_apps['Resident Totals_y'] = df_apps['Resident Totals_y'].apply(int)
    df_apps['tex_total_ratio'] = df_apps['Resident Totals_x']/df_apps['Resident Totals_y']
    df_apps.reset_index(inplace=True)
    return df_apps

am_00to08 = data_clean8(df=am_00to08)
tt_00to08 = data_clean8(df=tt_00to08)
ut_00to08 = data_clean8(df=ut_00to08)
am_09to18 = data_clean18(df=am_09to18)
tt_09to18 = data_clean18(df=tt_09to18)
ut_09to18 = data_clean18(df=ut_09to18)
am_applicants = merge_sort(df1=am_00to08,df2=am_09to18)
tt_applicants = merge_sort(df1=tt_00to08,df2=tt_09to18)
ut_applicants = merge_sort(df1=ut_00to08,df2=ut_09to18)
ut_winloss = url_clean(url=ut_url)
am_winloss = url_clean(url=am_url)
tt_winloss = url_clean(url=tt_url)

#merge win loss ratio and texas applicants and keep only the ratios

def merge_dataframes(df1,df2):
    df2['year'] = df2['year'].apply(int)
    df2['year'] = df2['year']+1 #adding one because we want to compare the 2000 fb season to 2001 admissions
    #(fb season already started so addimissions for year of fb season are not affected by fb season result)
    df_final = df1.merge(df2, how='inner',on='year')
    cols_keep = ['year','tex_total_ratio','ratio']
    df_final = df_final[cols_keep]
    df_final.set_index('year',inplace=True)
    return df_final

am_final = merge_dataframes(df1=am_applicants,df2=am_winloss)
tt_final = merge_dataframes(df1=tt_applicants,df2=tt_winloss)
ut_final = merge_dataframes(df1=ut_applicants,df2=ut_winloss)

#find pval and correlation for each data set
def pval_corr(df):
    corr, pval = stats.pearsonr(df['ratio'],df['tex_total_ratio'])
    return corr, pval

am_result = pval_corr(df=am_final)
tt_result = pval_corr(df=tt_final)
ut_result = pval_corr(df=ut_final)

print(am_result,tt_result,ut_result)

#plot the years and the ratios all on the same plot

fig, (ax1,ax2,ax3) = plt.subplots(3,1)
ax1.plot(am_final.index,am_final['ratio'],color='r')
ax1.plot(am_final.index,am_final['tex_total_ratio'],color='b')
ax2.plot(tt_final.index,tt_final['ratio'],color='r')
ax2.plot(tt_final.index,tt_final['tex_total_ratio'],color='b')
ax3.plot(ut_final.index,ut_final['ratio'],color='r')
ax3.plot(ut_final.index,ut_final['tex_total_ratio'],color='b')

def title_axis(plot,chart_title,result):
    plot.set_xlabel('Fall Admissions Year')
    plot.set_ylabel('Ratio')
    plot.set_xlim([2001,2018])
    plot.set_ylim([0,1])
    corr = round(result[0],4)
    pval = round(result[1],4)
    plot.legend(['Football Win/Loss Ratio','Texas Applicants/Total Applicants'],bbox_to_anchor=(1,0.5),loc='center left')
    plot.set_title(chart_title + '\n' + 'Correlation:' +' ' + str(corr) + '\n' + 'P-Value:' +' ' + str(pval))
    return plot


ut_title = 'University of Texas, Austin Football Win/Loss Ratio Compared to \n Following Year Texas Applicants to Total Applicants between 2001 and 2018'
am_title = 'Texas A&M Football Win/Loss Ratio Compared to Following Year \n Texas Applicants to Total Applicants between 2001 and 2018'
tt_title = 'Texas Tech Football Win/Loss Ratio Compared to Following Year \n Texas Applicants to Total Applicants between 2001 and 2018'


ax1 = title_axis(plot=ax1,chart_title=am_title,result=am_result)
ax2 = title_axis(plot=ax2,chart_title=tt_title,result=tt_result)
ax3 = title_axis(plot=ax3,chart_title=ut_title,result=ut_result)

fig.set_size_inches(13,8)
plt.tight_layout()
plt.show()
