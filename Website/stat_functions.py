# Import statements
import math
from math import log as ln
from operator import index
import numpy as np
import pandas as pd
import allel
import plotly
from itertools import combinations
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go


################# Gene Map Graph ########################
def gene_list_graph(position, database, increment_size):

    # note: Numbers for data to be selected based on position
    start = (position - increment_size)
    finish = (position + increment_size)

    df = pd.read_sql(('SELECT POS, GENE, ID FROM snp WHERE POS BETWEEN %(dstart)s AND %(dfinish)s'), database,
                 params={"dstart": start, "dfinish": finish})

    # note: Gets the first and last positions of each gene in the imported df
    first = dict(df.groupby('GENE')['POS'].first())
    last = dict(df.groupby('GENE')['POS'].last())
    num = df.value_counts('GENE').reset_index(name='NUM')  # note: counts snp num


    # note: Creates a new df of each gene and their start and end positions
    df2 = pd.DataFrame({'first': pd.Series(first), 'last': pd.Series(last)})
    df2.reset_index(level=0, inplace=True)
    df2.columns = ['GENE', 'START', 'END']
    df2['length'] = df2['END'] - df2['START']

    # note: Creates a new df with the SNP numbers in it
    df3 = pd.merge(df2, num, how='inner', on='GENE')
    df3.columns = ['GENE', 'START', 'END', 'Length', 'SNP NUM']

    # note: Sorts the df by Start position
    df4 = df3.sort_values(by=['START'])
    print(df4)

    # note: Plots the graph
    fig = px.bar(df4,
                x='Length',
                y='GENE',
                base='START',
                orientation='h',
                color='SNP NUM',
                custom_data=['START', 'END', 'Length', 'SNP NUM'],
                labels={'GENE': 'Genes',
                        'START': 'Start position',
                        'END': 'End position',
                        'SNP NUM': 'Number of SNPs'})

    # note: Configures the floating label
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{y}</b><br>",
            "First SNP Position: %{customdata[0]:s}",
            "Last SNP Position: %{customdata[1]:s}",
            "Length between SNPs (bp): %{customdata[2]:s}",
            "Number of SNPs: %{customdata[3]:s}"
        ])
    )


    # note: Sets the title & fonts of the graph
    fig.update_layout(title={'text': " Gene Map",
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                    xaxis_title="Chromosome position (bp)",
                    yaxis_title="Genes",
                    font_family="Times New Roman",
                    font_color="Black",
                    title_font_family="Times New Roman",
                    title_font_color="Black")

    # note: Creates a range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=200000,
                        label="200000bp",
                        step="all",
                        stepmode="backward"),
                    dict(count=400000,
                        label="400000bp",
                        step="all",
                        stepmode="backward"),
                    dict(count=600000,
                        label="600000bp",
                        step="all",
                        stepmode="backward"),
                    dict(count=800000,
                        label="800000bp",
                        step="all",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="linear"
        )
    )

    # note: Adds a line at the input
    fig.add_vline(x=position, line_width=2, line_dash="dash", line_color="gray")
    
    # Convert graoh to html
    a=pio.to_html(fig)
  
    return a

#################### SNP map Graph ####################

def snp_map(windowsize, database):

    df = pd.read_sql(('SELECT POS, GENE, ID FROM snp'), database)

    pos = df['POS'][:]

    # note: Creates the windowsize
    bin = np.arange(0, pos.max(), windowsize)

    # note: Uses the window midpoints as x coordinate
    x = (bin[1:] + bin[:-1])/2

    # note: Compute variant density in each window
    h, _ = np.histogram(pos, bins=bin)
    y = h / windowsize

    # note: plots & configures the graph
    fig = go.Figure(go.Line(x=x, y=y,
                            hovertemplate=
                            'Variant density (bp<sup>-1</sup>): %{y}' +
                            '<br>Chromosome position (bp)<extra></extra>: %{x}'))
    fig.update_traces(line_color='goldenrod')

    # note: Centers the title and fonts
    fig.update_layout(title={'text': "Raw Varient Density",
                             'x':0.5,
                             'xanchor': 'center',
                             'yanchor': 'top'},
                      xaxis_title="Chromosome position (bp)",
                      yaxis_title="Variant density (bp<sup>-1</sup>)",
                      font_family="Times New Roman",
                      font_color="Black",
                      title_font_family="Times New Roman",
                      title_font_color="Black")

    # note: Adds cross section cursor
    fig.update_xaxes(showspikes=True, spikecolor="Grey", spikesnap="cursor",
                     spikemode="across")
    fig.update_yaxes(showspikes=True, spikecolor="Black", spikethickness=2)
    fig.update_layout(spikedistance=1000, hoverdistance=100)

    # note: Adds sliding window to the graph
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=200000,
                         label="200000bp",
                         step="all",
                         stepmode="backward"),
                    dict(count=400000,
                         label="400000bp",
                         step="all",
                         stepmode="backward"),
                    dict(count=600000,
                         label="600000bp",
                         step="all",
                         stepmode="backward"),
                    dict(count=800000,
                         label="800000bp",
                         step="all",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="linear"
        )
    )

    # Converts graph to html
    graph=pio.to_html(fig)

    return graph


################# Hudson FST ######################


def makeArray(strings): # Input is a list of tuples of our encoded strings
    
    # initialize sample array with empty list
    bebG, cheG, esnG, gbrG, pelG = [], [], [], [], []
    
    # Decoding level one
    nested_dictionary = {'GBR':{'e':'a', 'f':'b', 'g':'c', 'h': 'd'},
                         'PEL':{'i':'a', 'j':'b', 'k':'c', 'l': 'd'},
                         'ESN':{'m':'a', 'n':'b', 'o':'c', 'p': 'd'},
                         'BEB':{'q':'a', 'r':'b', 's':'c', 't': 'd'},
                         'CHE':{'u':'a', 'v':'b', 'w':'c', 'x': 'd'}}

    # Decoding level two
    ginfo = {'a':'1|0', 'b':'1|1', 'c':'0|1', 'd':'0|0'}

    # Decoding by sub-population
    dic = {'e':'GBR', 'f':'GBR', 'g':'GBR', 'h':'GBR',
           'i':'PEL', 'j':'PEL', 'k':'PEL', 'l':'PEL',
           'm':'ESN', 'n':'ESN', 'o':'ESN', 'p':'ESN',
           'q':'BEB', 'r':'BEB', 's':'BEB', 't':'BEB',
           'u':'CHE', 'v':'CHE', 'w':'CHE', 'x':'CHE'}
    
    # create list of encoded strings
    lst=[]
    for item in strings:
        for p in item:
            lst.append(p)

    # Iterate over stings in list
    for string in lst:
        string = string.strip()
        genotypes = {}
        # Create indexed list of the strings
        for i, c in enumerate(string):
            # take sample as key and 0|1 etc as value
            genotypes.setdefault(dic[c], []).append(ginfo[nested_dictionary[dic[c]][c]])

        # sort dictionary alphabetically
        genotypes = dict(sorted(genotypes.items(), key = lambda x:x[0].lower()))
        # split each 0|1 etc by | and make a list,,,thus apply on each sample
        genotype_array = [[list(map(int, v.split('|'))) for v in val] for val in genotypes.values()]

        # extracting genotype array samples
        bebG.append(genotype_array[0])
        cheG.append(genotype_array[1])
        esnG.append(genotype_array[2])
        gbrG.append(genotype_array[3])
        pelG.append(genotype_array[4])
    # Returns a tuple of lists - Pre-array
    return (bebG, cheG, esnG, gbrG, pelG)

# Gives you single value fst for population comparison
def calc_hudson_fst_1v1(pop_array1, pop_array2):
    genotype_array1 = allel.GenotypeArray(pop_array1)
    genotype_array2 = allel.GenotypeArray(pop_array2)
    ac1 = genotype_array1.count_alleles()
    ac2 = genotype_array2.count_alleles()
    num, den = allel.hudson_fst(ac1, ac2)
    fst = np.sum(num) / np.sum(den)
    return fst 

# Get the FST for all comparisons of the populations selected - output: html table
def all_hudson_fsts(array, subpop):

    # extract genotype array into samples
    bebG, chbG, esnG, gbrG, pelG = array

    fsts={}

    # Run all FST comparisons selected
    if 'BEB' in subpop and 'GBR' in subpop:

        BvG = calc_hudson_fst_1v1(bebG, gbrG)
        fsts['Bengali vs Great Britain']=BvG

    if 'BEB' in subpop and 'CHB' in subpop:

        BvC = calc_hudson_fst_1v1(bebG, chbG)
        fsts['Bengali vs China']=BvC

    if 'BEB' in subpop and 'PEL' in subpop:

        BvP = calc_hudson_fst_1v1(bebG, pelG)
        fsts['Bengali vs Peru']=BvP

    if 'BEB' in subpop and 'ESN' in subpop:

        BvE = calc_hudson_fst_1v1(bebG, esnG)
        fsts['Bengali vs Nigeria']=BvE

    if 'GBR' in subpop and 'CHB' in subpop:

        GvC = calc_hudson_fst_1v1(gbrG, chbG)
        fsts['Great Britain vs China']=GvC

    if 'GBR' in subpop and 'PEL' in subpop:

        GvP = calc_hudson_fst_1v1(gbrG, pelG)
        fsts['Great Britain vs Peru']=GvP

    if 'GBR' in subpop and 'ESN' in subpop:

        GvE = calc_hudson_fst_1v1(gbrG, esnG)
        fsts['Great Britain vs Nigeria']=GvE

    if 'CHB' in subpop and 'PEL' in subpop:

        CvP = calc_hudson_fst_1v1(chbG, pelG)
        fsts['China vs Peru']=CvP

    if 'CHB' in subpop and 'ESN' in subpop:

        CvE = calc_hudson_fst_1v1(chbG, esnG)
        fsts['China vs Nigeria']=CvE

    if 'PEL' in subpop and 'ESN' in subpop:

        PvE = calc_hudson_fst_1v1(pelG, esnG)
        fsts['Peru vs Nigeria ']=PvE

    else:
        pass
    
    # Convert output into a HTML table
    FSTs = pd.DataFrame(list(fsts.items()),columns = ['Subpopulations','Average Hudson FST']).to_html(classes=' content-area clusterize-content table table-stripped table-striped table-bordered table-sm "id="my_id', justify='left', index=False, show_dimensions=False, header=True) #table-responsive makes the table as small as possible

    return FSTs

# Get the FST for all comparisons of the populations selected - output: dictionary
def calc_hudson_fst(array, subpop):
    # passing sequences into makeArray function
    g = array
    # extract genotype array into samples
    bebG, cheG, esnG, gbrG, pelG = g

    l1=[]
    l2=[]

    for item in subpop:

        if item == 'BEB':
            l1.append('BEB')
            l2.append(bebG)

        elif item == 'GBR':
            l1.append('GBR')
            l2.append(gbrG)
        
        elif item == 'CHB':
            l1.append('CHB')
            l2.append(cheG)

        elif item == 'PEL':
            l1.append('PEL')
            l2.append(pelG)
        
        elif item == 'ESN':
            l1.append('ESN')
            l2.append(esnG)
        else:
            pass
    
    FSTs = {}
    # Iterate over dictionary of the created lists
    for pair,val in zip( combinations(l1,2), combinations(l2,2)):
        # Create arrays
        ac1 = allel.GenotypeArray(val[0]).count_alleles()
        ac2 = allel.GenotypeArray(val[1]).count_alleles()
        num, den = allel.hudson_fst(ac1, ac2)
        fst = np.sum(num)/np.sum(den)
        # Output dictionary
        FSTs.update({pair : fst})
    
    return FSTs

# Create dictionary of all fsts for all subpop combinations for each bin 
def fst_dict_calc(positions, array, subpop, dividend=1000): 

    indices = {}

    for i, num in enumerate(sorted(positions)):
        
        # take upper integer value of num
        n = math.ceil(num/dividend)
        
        # add the indices to the corresponding key as n
        indices.setdefault(n, []).append(i)
    
    # sort the dictionariy
    indices = dict(sorted(indices.items(), key=lambda x:x[0]))
    
    fst_dict1 = {}
    fst_dict2 = {}
    index_positions = {}

    for i, val in indices.items():

        ns=[]
        for item in array:
            ns+=[item[val[0]:val[-1]]] 

        results = calc_hudson_fst(ns, subpop)
         
        # update index_positions dictionary as {i : range} pair
        index_positions.update({i : str(val[0])+':'+str(val[-1])})
        
        # update fst_dict2 dictionary as {i : results} pair
        fst_dict2.update({i : results})

        for k, v in results.items():
            
            # nested dictionary as {pops : {index : fst_value}}
            fst_dict1.setdefault(k, {}).update({i : v})

    return fst_dict1

# Converts 200000 to 2M for better legend formating
def strink(num):
    if len(str(num)) <= 5:
        snum = str((num/1000))+'k'
        return snum
    elif len(str(num)) >= 6:
        snum = str((num/1000000))+'M'
        return snum
    else:
        pass

# note: Generates a scatter graph if given a dictionary of values
def FSTscatter(input, start, stop):

    ik = []
    for v in input.values():
        for key in v.keys():
            ik.append(key)

    # note: records the number of steps in the input data
    vlen = []
    for v in input.values():
        vlen.append(len(v.values()))


    # note: Calculates the step size of the input data
    step = int((stop - start)/vlen[0])

    # note: Creates the range caterogies
    bounds = [
             (strink(n)+'-'+strink(min(n+step, stop)))
             for n in range(start, stop, step)
             ]

    # note: Maps each nested key from the input dict to a boundary
    first = ik[0:vlen[0]]
    keydict = dict(zip(first, bounds))


    # note: Creates df for graph
    df = pd.DataFrame.from_dict(input, orient='index').stack().reset_index()
    df['Pop'] = df[['level_0', 'level_1']].agg('-'.join, axis=1)
    del df['level_0']
    del df['level_1']
    df = df.fillna('')
    df.columns = ['Range', 'FST', 'Pop']

    df['Range'].replace(keydict, inplace=True)
 

    # note: Sorts the FST values in the df to auto set max axis values
    FST = list(df['FST'])
    FST = [i for i in FST if i != '']
    FST.sort(key=float)
    #print(FST)

    # note: plots the scatter graph
    fig = px.scatter(df, x="Pop", y="FST", color="Range",
                     color_discrete_sequence=px.colors.qualitative.Dark24,
                     labels={"Range": "Region on Chromosome (bp) ",
                             "Pop": "Subpopulation Comparison",
                             "FST": "Hudson FST"},
                     title="Hudson FST Across the Selected Region",
                     animation_frame="Range",
                     animation_group="Pop")
    fig.update_traces(marker=dict(size=12))

    # note: Sets the fonts and layout
    fig.update_layout(font_family="Times New Roman",
                      font_color="Black",
                      title_font_family="Times New Roman",
                      title_font_color="Black",
                      legend={'traceorder': 'reversed'},
                      showlegend=False,
                      yaxis_range=[FST[0] - 0.01, FST[-1] + 0.01])
    fig.add_hline(y=0.12, line_width=1, line_dash="dash", line_color="gray")
    fig.add_hline(y=0.25, line_width=1, line_dash="dash", line_color="red")


    # Convert graph to html
    graph=pio.to_html(fig)


    return  graph






################### Shannon Diversity ###################


def sdi(af): #A list of allele frequencies per snp 
    index = []
  
    for x in af:
        if x > 0:
            Pi = (x) * ln(x)
            index.append(Pi)
        else:
            pass
    H = -sum(index)
    return H

# Produce a HTML table for shannon diversity
def Shannon(allsnps, BAF, GAF, CAF, PAF, EAF, subpop):

    # Turn extracted list of tuples of strings into a list of floats
    BAF=[float(a) for item in BAF for a in item]
    GAF=[float(a) for item in GAF for a in item]
    CAF=[float(a) for item in CAF for a in item]
    PAF=[float(a) for item in PAF for a in item]
    EAF=[float(a) for item in EAF for a in item]


    #list to be zipped together
    poplst=[]
    for item in subpop:
        if item == 'BEB':
            poplst.append(BAF)

        elif item == 'GBR':
            poplst.append(GAF)
        
        elif item == 'CHB':
            poplst.append(CAF)

        elif item == 'PEL':
            poplst.append(PAF)
        
        elif item == 'ESN':
            poplst.append(EAF)
        else:
            pass

    # Combine lists together into a nested list so that each sublist contains the AF for each subpop
    afs=[list(l) for l in zip(*poplst)]

    allsnp=allsnps # List of tuples the SNPs
    # Convert list of tuples of strings to list of strings
    allsnps=[a for item in allsnp for a in item]

    snlst=[]
    for item in allsnps:

        snlst.append(item)

    shnnlst=[]

    for item in afs:

        shnn=sdi(item)
        shnnlst.append(shnn)

    
    zip_iterator = zip(snlst, shnnlst)
    dictionary=dict(zip_iterator)

    Shannon = pd.DataFrame(list(dictionary.items()),columns = ['SNP name','Shannon Diversity for Selected Populations']).to_html(classes='content-area clusterize-content table table-stripped table-striped table-bordered table-sm "id="my_id1', justify='left', index=False, show_dimensions=False, header=True) #table-responsive makes the table as small as possible

    return Shannon

# Produce a data frame of shannon diversities as graph input
def ShannonG(allsnps, BAF, GAF, CAF, PAF, EAF, subpop, positions):

    # Turn extracted list of tuples of strings into a list of floats
    BAF=[float(a) for item in BAF for a in item]
    GAF=[float(a) for item in GAF for a in item]
    CAF=[float(a) for item in CAF for a in item]
    PAF=[float(a) for item in PAF for a in item]
    EAF=[float(a) for item in EAF for a in item]


    #list to be zipped together
    poplst=[]
    for item in subpop:
        if item == 'BEB':
            poplst.append(BAF)

        elif item == 'GBR':
            poplst.append(GAF)
        
        elif item == 'CHB':
            poplst.append(CAF)

        elif item == 'PEL':
            poplst.append(PAF)
        
        elif item == 'ESN':
            poplst.append(EAF)
        else:
            pass

    # Combine lists together into a nested list so that each sublist contains the AF for each subpop
    afs=[list(l) for l in zip(*poplst)]

    allsnp=allsnps # List of tuples the SNPs
    # Convert list of tuples of strings to list of strings
    allsnps=[a for item in allsnp for a in item]

    snlst=[]
    for item in allsnps:

        snlst.append(item)

    shnnlst=[]

    for item in afs:

        shnn=sdi(item)
        shnnlst.append(shnn)

    
    zip_iterator = zip(snlst, shnnlst)
    dictionary=dict(zip_iterator)


    Shannon = pd.DataFrame(list(dictionary.items()),columns = ['SNP name','Shannon Diversity for Selected Populations'])

    Shannon["POS"]=positions

    return Shannon

# Produce a line graph for shannon diversity
def ShannonGraph(df):

    # Rename columns
    df.columns = ['SNP', 'Shannon', 'POS']

    # note: Plots the graph
    fig = px.line(df, y='Shannon', x='POS',
                  hover_data=["POS", "Shannon", "SNP"],
                  labels={"POS": "Chromosome Position (bp)",
                          "Shannon": "Shannon Diversity",
                          "SNP": "SNP"})
    fig.update_traces(line_color='goldenrod')

    # note: Centers the title and fonts
    fig.update_layout(title={'text': "Shannon Diversity Across the Selected Region",
                             'x':0.5,
                             'xanchor': 'center',
                             'yanchor': 'top'},
                      xaxis_title="Chromosome position (bp)",
                      yaxis_title="Shannon Diversity",
                      font_family="Times New Roman",
                      font_color="Black",
                      title_font_family="Times New Roman",
                      title_font_color="Black")

    # note: Adds cross section cursor
    fig.update_xaxes(showspikes=True, spikecolor="Grey", spikesnap="cursor",
                     spikemode="across")
    fig.update_yaxes(showspikes=True, spikecolor="Black", spikethickness=2)
    fig.update_layout(spikedistance=1000, hoverdistance=100)

    # note: Adds sliding window
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=200000,
                         label="200000bp",
                         step="all",
                         stepmode="backward"),
                    dict(count=400000,
                         label="400000bp",
                         step="all",
                         stepmode="backward"),
                    dict(count=600000,
                         label="600000bp",
                         step="all",
                         stepmode="backward"),
                    dict(count=800000,
                         label="800000bp",
                         step="all",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="linear"
        )
    )
    graph=pio.to_html(fig)

    return graph





##################### Tajimas D ####################





# Create html table showing tajimas d for each subpopulation selected
def Tajimas(genotype_array, subpop):

    # extract genotype array into samples
    bebG, cheG, esnG, gbrG, pelG = genotype_array

    # ONly retain selected populations
    poplst=[]
    poplst2=[]
    for item in subpop:
        if item == 'BEB':
            poplst.append('Bengali')
            poplst2.append(bebG)

        elif item == 'GBR':
            poplst.append('Great Britain')
            poplst2.append(gbrG)
        
        elif item == 'CHB':
            poplst.append('China')
            poplst2.append(cheG)

        elif item == 'PEL':
            poplst.append('Peru')
            poplst2.append(pelG)
        
        elif item == 'ESN':
            poplst.append('Nigeria')
            poplst2.append(esnG)
        else:
            pass



    Tajima_D = {}
    
    for pair,val in zip( combinations([*poplst],1), combinations([*poplst2],1)):
        
        ac = allel.GenotypeArray(val[0]).count_alleles()
       
        fst = allel.tajima_d(ac)
    
        Tajima_D.update({str(pair).strip("(''),") : fst})

    Tajima = pd.DataFrame(list(Tajima_D.items()),columns = ['Subpopulation',"Tajima's D for Selected Population"]).to_html(classes='content-area clusterize-content table table-stripped table-striped table-bordered table-sm "id="my_id2', justify='left', index=False, show_dimensions=False, header=True) #table-responsive makes the table as small as possible
    
    return Tajima

# Create dictionary showing tajimas d for each subpopulation selected
def Tajimas2(genotype_array, subpop):

    # extract genotype array into samples
    bebG, cheG, esnG, gbrG, pelG = genotype_array

    # ONly retain selected populations
    poplst=[]
    poplst2=[]
    for item in subpop:
        if item == 'BEB':
            poplst.append('Bengali')
            poplst2.append(bebG)

        elif item == 'GBR':
            poplst.append('Great Britain')
            poplst2.append(gbrG)
        
        elif item == 'CHB':
            poplst.append('China')
            poplst2.append(cheG)

        elif item == 'PEL':
            poplst.append('Peru')
            poplst2.append(pelG)
        
        elif item == 'ESN':
            poplst.append('Nigeria')
            poplst2.append(esnG)
        else:
            pass



    Tajima_D = {}
    
    for pair,val in zip( combinations([*poplst],1), combinations([*poplst2],1)):
        
        ac = allel.GenotypeArray(val[0]).count_alleles()
       
        fst = allel.tajima_d(ac)
    
        Tajima_D.update({str(pair).strip("(''),") : fst})

    
    return Tajima_D

 # create tajimas d dictionary for all bins to input to graph function
def taj_dict_calc(positions, array, subpop, dividend=1000): 
    
    indices = {}

    for i, num in enumerate(sorted(positions)):
        
        # take upper integer value of num
        n = math.ceil(num/dividend)
        
        # add the indices to the corresponding key as n
        indices.setdefault(n, []).append(i)
    
    # sort the dictionariy
    indices = dict(sorted(indices.items(), key=lambda x:x[0]))
    
    fst_dict1 = {}
    fst_dict2 = {}
    index_positions = {}

    for i, val in indices.items():

        ns=[]
        for item in array:
            ns+=[item[val[0]:val[-1]]]
        

        results = Tajimas2(ns, subpop)
        #print(results)
        
        
        # update index_positions dictionary as {i : range} pair
        index_positions.update({i : str(val[0])+':'+str(val[-1])})
        
        
        # update fst_dict2 dictionary as {i : results} pair
        fst_dict2.update({i : results})

        
        for k, v in results.items():
            
            # nested dictionary as {pops : {index : fst_value}}
            fst_dict1.setdefault(k, {}).update({i : v})

    return fst_dict1

# note: Converts 200000 to 2M for better legend formating
def strink2(num):
    if len(str(num)) <= 5:
        snum = str((num/1000))+'k'
        return snum
    elif len(str(num)) >= 6:
        snum = str((num/1000000))+'M'
        return snum
    else:
        pass

# note: Plots a Barchart for Tajima's D
def TD_Bar(input, start, stop):

    # note: Creates a list of nested keys from input dict
    ik = []
    for v in input.values():
        for key in v.keys():
            ik.append(key)

    # note: records the number of steps in the input data
    vlen = []
    for v in input.values():
        vlen.append(len(v.values()))
    print(vlen)

    # note: Calculates the step size of the input data
    step = int((stop - start)/vlen[0])
    print(step)

    # note: Creates the range caterogies
    bounds = [
             (strink2(n+1)+''+'-'+''+strink2(min(n+step, stop)))
             for n in range(start, stop, step)
             ]
    print(bounds)

    # note: Maps each nested key from the input dict to a boundary
    first = ik[0:vlen[0]]
    keydict = dict(zip(first, bounds))
    print(len(keydict))

    # note: Creates df for graph
    df = pd.DataFrame.from_dict(input, orient='index').stack().reset_index()
    df = df.fillna('')
    df.columns = ['Pop', 'Step', 'TD']
    df['Step'].replace(keydict, inplace=True)
    print(df)

    # note: Plots the graph
    fig = px.bar(df, y='TD', x='Step', color='Pop', barmode='overlay',
                 labels={"Step": "Region on Chromosome (bp) ",
                         "Pop": "Subpopulation",
                         "TD": "Tajima's D"},
                 title="Tajima's D Across the Selected Region",
                 color_discrete_sequence=px.colors.qualitative.G10)

    # note: Sets the fonts and layout
    fig.update_layout(font_family="Times New Roman",
                      font_color="Black",
                      title_font_family="Times New Roman",
                      title_font_color="Black")

    # note: Adds range slider
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)))


    graph=pio.to_html(fig)

    return graph




############# Haplotype diversity ################ 



# Calculate haplotype diversity
def haplotype_diversity(array):
    # extract genotype array into samples
    bebG, cheG, esnG, gbrG, pelG = array
    
    haplotype_diversity = {}
    
    # for each population calculate haplotype diversity
    for pair,val in zip( combinations(['bebG','cheG','esnG','gbrG','pelG'],1), combinations([bebG,cheG,esnG,gbrG,pelG],1)):
        
        # biuld genotype array of list of genotypes
        g = allel.GenotypeArray(val[0])
        
        # convert genotype array into haplotype array
        haplo = g.to_haplotypes()
        
        #calculate haplotype_diversity inside the region selected
        div = allel.haplotype_diversity(haplo)
    
        # update dictionary for returning
        haplotype_diversity.update({str(pair).strip("(''),") : div})
    
    return haplotype_diversity

# Create HTML table for haplotype diversity
def haplotype_diversity2T(positions, array, subpop, snpnum): 
    
    indices = {}

    n = math.ceil(len(positions)/snpnum)

    nlst=list(range(n))

    z=enumerate(sorted(positions))
    z=dict((i,j) for i,j in z)
    v=0
    p=snpnum
    for item in nlst:

        for i in z.keys():

            if i <= p and i >= v:

                indices.setdefault(item, []).append(i)
            else:
                pass
        p+=snpnum
        v+=snpnum 

    # create a dictionary with the the numbe rof bins and the size of each one
    positions=z.values()
    dictiona={}

    count=0
    y=0
    for item in positions:

        if count == snpnum:

            count-=snpnum
            y+=1

        #dictiona[y]+=[item]
        dictiona.setdefault(y, []).append(item)
        count+=1

    for item in nlst:

        dictiona[item]=str(dictiona[item][0])+'-'+str(dictiona[item][-1])


    
    # sort the dictionariy
    indices = dict(sorted(indices.items(), key=lambda x:x[0]))
    
    fst_dict1 = {}
    fst_dict2 = {}
    index_positions = {}

    for i, val in indices.items():

        ns=[]
        for item in array:
            ns+=[item[val[0]:val[-1]]]
        

        results = haplotype_diversity(ns)
        #print(results)
        
        
        # update index_positions dictionary as {i : range} pair
        index_positions.update({i : str(val[0])+':'+str(val[-1])})
        
        
        # update fst_dict2 dictionary as {i : results} pair
        fst_dict2.update({i : results})

        
        for k, v in results.items():
            
            # nested dictionary as {pops : {index : fst_value}}
            fst_dict1.setdefault(k, {}).update({i : v})

    
    inner1=fst_dict1['bebG']
    inner2=fst_dict1['cheG']
    inner3=fst_dict1['esnG']
    inner4=fst_dict1['pelG']
    inner5=fst_dict1['gbrG']

    bebG_k=list(dictiona.values())
    bebG_V=list(inner1.values())

    cheG_k=list(dictiona.values())
    cheG_V=list(inner2.values())

    esnG_k=list(dictiona.values())
    esnG_V=list(inner3.values())

    pelG_k=list(dictiona.values())
    pelG_V=list(inner4.values())

    gbrG_k=list(dictiona.values())
    gbrG_V=list(inner5.values())


    fst4={}
    for item in subpop:

        if item == 'BEB':
            fst4['BEB']=dict(zip(bebG_k, bebG_V))

        elif item == 'CHB':
            fst4['CHB']=dict(zip(cheG_k, cheG_V))
        
        elif item == 'ESN':
            fst4['ESN']=dict(zip(esnG_k, esnG_V))
        
        elif item == 'PEL':
            fst4['PEL']=dict(zip(pelG_k, pelG_V))
        
        elif item == 'GBR':
            fst4['GBR']=dict(zip(gbrG_k, gbrG_V))
        
        else:
            pass

    
    user_ids = []
    frames = []

    for user_id, d in fst4.items():
        user_ids.append(user_id)
        frames.append(pd.DataFrame.from_dict(d, orient='index'))

    df=pd.concat(frames, keys=user_ids)

    df=df.reset_index()

    df.columns=['Subpopulation', 'Location', 'Haplotype Diversity']

    df=df.to_html(classes='content-area clusterize-content table table-stripped table-striped table-bordered table-sm "id="my_id3', justify='left', index=False, show_dimensions=False, header=True) #table-responsive makes the table as small as possible


    return df

# Create dictionary as in put for graph function
def haplotype_diversity2G(positions, array, subpop, snpnum=100): 
    
    indices = {}

    n = math.ceil(len(positions)/snpnum)

    nlst=list(range(n))

    z=enumerate(sorted(positions))
    z=dict((i,j) for i,j in z)
    v=0
    p=snpnum
    for item in nlst:

        for i in z.keys():

            if i <= p and i >= v:

                indices.setdefault(item, []).append(i)
            else:
                pass
        p+=snpnum
        v+=snpnum 

    # create a dictionary with the the numbe rof bins and the size of each one
    positions=z.values()
    dictiona={}

    count=0
    y=0
    for item in positions:

        if count == snpnum:

            count-=snpnum
            y+=1
        

        #dictiona[y]+=[item]
        dictiona.setdefault(y, []).append(item)
        count+=1

    for item in nlst:

        dictiona[item]=str(dictiona[item][0])+'-'+str(dictiona[item][-1])


    
    # sort the dictionariy
    indices = dict(sorted(indices.items(), key=lambda x:x[0]))
    
    fst_dict1 = {}
    fst_dict2 = {}
    index_positions = {}

    for i, val in indices.items():

        ns=[]
        for item in array:
            ns+=[item[val[0]:val[-1]]]
        

        results = haplotype_diversity(ns)
        #print(results)
        
        
        # update index_positions dictionary as {i : range} pair
        index_positions.update({i : str(val[0])+':'+str(val[-1])})
        
        
        # update fst_dict2 dictionary as {i : results} pair
        fst_dict2.update({i : results})

        
        for k, v in results.items():
            
            # nested dictionary as {pops : {index : fst_value}}
            fst_dict1.setdefault(k, {}).update({i : v})

    
    inner1=fst_dict1['bebG']
    inner2=fst_dict1['cheG']
    inner3=fst_dict1['esnG']
    inner4=fst_dict1['pelG']
    inner5=fst_dict1['gbrG']

    bebG_k=list(dictiona.values())
    bebG_V=list(inner1.values())

    cheG_k=list(dictiona.values())
    cheG_V=list(inner2.values())

    esnG_k=list(dictiona.values())
    esnG_V=list(inner3.values())

    pelG_k=list(dictiona.values())
    pelG_V=list(inner4.values())

    gbrG_k=list(dictiona.values())
    gbrG_V=list(inner5.values())



    fst4={}
    for item in subpop:

        if item == 'BEB':
            fst4['BEB']=dict(zip(bebG_k, bebG_V))

        elif item == 'CHB':
            fst4['CHB']=dict(zip(cheG_k, cheG_V))
        
        elif item == 'ESN':
            fst4['ESN']=dict(zip(esnG_k, esnG_V))
        
        elif item == 'PEL':
            fst4['PEL']=dict(zip(pelG_k, pelG_V))
        
        elif item == 'GBR':
            fst4['GBR']=dict(zip(gbrG_k, gbrG_V))
        
        else:
            pass


    return fst4

# Plots a Barchart for haplotype diversity
def hp_Bar(input, start, stop):
    # note: Creates a list of nested keys from input dict
    ik = []
    for v in input.values():
        for key in v.keys():
            ik.append(key)

    # note: records the number of steps in the input data
    vlen = []
    for v in input.values():
        vlen.append(len(v.values()))
    print(vlen)

    # note: Calculates the step size of the input data
    step = int((stop - start)/vlen[0])
    print(step)

    # note: Creates the range caterogies
    bounds = [
             (strink2(n+1)+''+'-'+''+strink2(min(n+step, stop)))
             for n in range(start, stop, step)
             ]

    # note: Maps each nested key from the input dict to a boundary
    first = ik[0:vlen[0]]
    keydict = dict(zip(first, bounds))

    # note: Creates df for graph
    df = pd.DataFrame.from_dict(input, orient='index').stack().reset_index()
    df = df.fillna('')
    df.columns = ['Pop', 'Step', 'HAP']
    df['Step'].replace(keydict, inplace=True)
    print(df)

    print(list(range(start, stop, int((stop - start)/vlen[0]))))

    # note: Plots the graph
    fig = px.bar(df, y='HAP', x='Step', color='Pop', barmode='overlay',
                 labels={"Step": "Region on Chromosome (bp) ",
                         "Pop": "Subpopulation",
                         "HAP": "Haplotype Diversity"},
                 title="Haplotype Diversity Across Selected Region",
                 color_discrete_sequence=px.colors.qualitative.G10)

    # note: Sets the fonts and layout
    fig.update_layout(font_family="Times New Roman",
                      font_color="Black",
                      title_font_family="Times New Roman",
                      title_font_color="Black")

    # note: Adds range slider
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)))

    graph=pio.to_html(fig)

    return graph

