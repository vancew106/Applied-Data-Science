import pandas as pd 
import numpy as np
import matplotlib as plt

def get_energy():
    Energy = pd.read_excel('Energy Indicators.xls')
    Energy = Energy[16:243].drop( Energy.columns[[0, 1]], axis=1 ).reset_index(drop=True)
    Energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    # remove numbers from country names
    Energy['Country'] = Energy['Country'].str.replace('\d+', '')
    # replace '...' value with NaN
    Energy['Energy Supply'] = Energy['Energy Supply'].replace('...', np.NaN)
    Energy['Energy Supply per Capita'] = Energy['Energy Supply per Capita'].replace('...', np.NaN)
    Energy['Energy Supply'] = Energy['Energy Supply'] * 1000000
    dicts = {"Republic of Korea": "South Korea",
                 "United States of America": "United States",
                 "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                 "China, Hong Kong Special Administrative Region": "Hong Kong"}
    Energy['Country'] = Energy['Country'].replace(dicts)
    # remove where country names contains paranthesises. 
    Energy['Country'] = Energy['Country'].str.replace(' \(.*\)', '')
    return Energy

def get_GDP():
    GDP = pd.read_csv('world_bank.csv', encoding="ISO-8859-1", skiprows=4)
    dicts = {"Korea, Rep.": "South Korea", 
                 "Iran, Islamic Rep.": "Iran",
                 "Hong Kong SAR, China": "Hong Kong"}
    GDP['Country Name'] = GDP['Country Name'].replace(dicts)
    GDP.rename(columns={"Country Name": "Country"}, inplace=True)
    return GDP

def get_ScimEn():
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    return ScimEn

def answer_one():
    Energy = get_energy()
    GDP = get_GDP()
    ScimEn = get_ScimEn()

    GDP = GDP[['Country', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    ScimEn = ScimEn.head(15)
    df1 = pd.merge(ScimEn, Energy, how='inner', left_on="Country", right_on="Country")
    df2 = pd.merge(df1, GDP, how="inner", left_on="Country", right_on="Country")
    df2 = df2.set_index('Country')
    return df2

def answer_two():
    Energy = get_energy()
    GDP = get_GDP()
    ScimEn = get_ScimEn()

    inner1 = pd.merge(ScimEn, Energy, how='inner', left_on="Country", right_on="Country")
    inner2 = pd.merge(inner1, GDP, how="inner", left_on="Country", right_on="Country")
    inner2 = inner2.set_index('Country')
    inner_row = len(inner2.index)

    outer1 = pd.merge(ScimEn, Energy, how='outer', left_on="Country", right_on="Country")
    outer2 = pd.merge(outer1, GDP, how="outer", left_on="Country", right_on="Country")
    outer2 = outer2.set_index('Country')
    outer_row = len(outer2.index)

    return int(outer_row - inner_row)

def answer_three():
    Top15 = answer_one()[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    Top15['average GDP'] = Top15.mean(axis=1)
    avgGDP = pd.Series( data=Top15['average GDP'], index=Top15.index ).sort_values( axis=0, ascending=False )
    return avgGDP

def answer_four():
    Top6th = answer_one()[['2006', '2015']].loc['United Kingdom']
    change =  Top6th['2015'] - Top6th['2006']
    return change

def answer_five():
    espc = answer_one()['Energy Supply per Capita']
    espc = espc.mean()
    return espc

def answer_six():
    maxrenew = answer_one()['% Renewable']
    (idx, val) = (maxrenew.idxmax(), maxrenew.max())
    return (idx, val)
#print(answer_six())

def answer_seven():
    ratio = answer_one()[['Self-citations', 'Citations']]
    ratio['ratio'] = ratio['Self-citations'] / ratio['Citations']
    (idx, val) = ( ratio['ratio'].idxmax(), ratio['ratio'].max() )
    return (idx, val)
#print(answer_seven())

def answer_eight():
    popul = answer_one()[['Energy Supply', 'Energy Supply per Capita']]
    popul['Population'] = popul['Energy Supply'] / popul['Energy Supply per Capita']
    popul = popul.sort_values('Population', ascending=False)
    country = popul.index[2]
    return country
#print(answer_eight())

def answer_nine():
    number = answer_one()[['Energy Supply', 'Energy Supply per Capita', 'Citable documents']]
    number['Population'] = number['Energy Supply'] / number['Energy Supply per Capita']
    number['Citable docs per Capita'] = number['Citable documents'] / number['Population']
    number = number.drop( ['Energy Supply', 'Citable documents', 'Population'], axis=1 )
    return number.corr('pearson').iloc[0, 1]
#print(answer_nine())

def answer_ten():
    HighRenew = answer_one()
    HighRenew = HighRenew['% Renewable'].sort_values()
    renew_med = HighRenew.median()
    for idx, val in HighRenew.iteritems():
        if val < renew_med:
            HighRenew[idx] = 0
        else:
            HighRenew[idx] = 1
    return HighRenew
#print(answer_ten())

def answer_eleven():
    contin = answer_one()[['Energy Supply', 'Energy Supply per Capita']]
    contin['Population'] = contin['Energy Supply'] / contin['Energy Supply per Capita']
    ContinentDict  = {'China':'Asia',
                      'United States':'North America',
                      'Japan':'Asia',
                      'United Kingdom':'Europe',
                      'Russian Federation':'Europe',
                      'Canada':'North America',
                      'Germany':'Europe',
                      'India':'Asia',
                      'France':'Europe',
                      'South Korea':'Asia',
                      'Italy':'Europe',
                      'Spain':'Europe',
                      'Iran':'Asia',
                      'Australia':'Australia',
                      'Brazil':'South America'}
    contin['Continent'] = pd.Series(ContinentDict)
    contin = contin.drop(['Energy Supply', 'Energy Supply per Capita'], axis=1)
    contin_info = contin.groupby('Continent')['Population'].agg( {'size':np.size, 'sum':np.sum, 'mean':np.mean, 'std':np.std} )
    return contin_info

def answer_twelve():
    ContinentDict  = {'China':'Asia',
                      'United States':'North America',
                      'Japan':'Asia',
                      'United Kingdom':'Europe',
                      'Russian Federation':'Europe',
                      'Canada':'North America',
                      'Germany':'Europe',
                      'India':'Asia',
                      'France':'Europe',
                      'South Korea':'Asia',
                      'Italy':'Europe',
                      'Spain':'Europe',
                      'Iran':'Asia',
                      'Australia':'Australia',
                      'Brazil':'South America'}
    renew = answer_one()[['% Renewable']]
    renew['Continent'] = pd.Series(ContinentDict)
    renew = renew.set_index('Continent')
    renew['bin'] = pd.cut(renew['% Renewable'], 5)
    renew_bin = renew.groupby([renew.index, 'bin'])['% Renewable'].agg(np.size)
    return renew_bin
#print(answer_twelve())

def answer_thirteen():
    PopEst = answer_one()[['Energy Supply', 'Energy Supply per Capita']]
    PopEst['Population'] = PopEst['Energy Supply'] / PopEst['Energy Supply per Capita']
    PopEst = PopEst.drop(['Energy Supply', 'Energy Supply per Capita'], axis=1).ix[:,0]
    for idx, val in PopEst.iteritems():
        PopEst[idx] = "{:,}".format(PopEst[idx])
    return PopEst
#print(answer_thirteen())

def plot_optional():
    import matplotlib as plt
    #%matplotlib inline
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. \
This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' \
2014 GDP, and the color corresponds to the continent.")
print(plot_optional())