# import the app factory (the app)
from audioop import reverse
from operator import itemgetter
from os import sep

from Website import create_app
# Import flask and associated packages 
from flask import render_template, redirect, request, send_file, send_from_directory, url_for, session
# MySQL connector to connect to and search db
import mysql.connector 
from mysql.connector import connect, Error
# To time searches
import time
# import pandas 
import pandas as pd

#Import stat functions
from Website.stat_functions import *

# Start app
app = create_app()

# Set up a connection with the MySQL database
try:
    mydb = mysql.connector.connect(host="34.89.113.123",
                                    user="User3",
                                    database="SnPip") # Database Name

    mycursor = mydb.cursor(buffered=True)
except Error as e:
    print(e)


@app.route('/') # this is the home page
def home(): # this function will run whenever we go to this route
    return render_template('home.html') # Home page template

@app.route('/about') # this is the about page
def about(): # this function will run whenever we go to this route
    return render_template('about.html')

@app.route('/documentation') # this is the documentation page
def documentation(): # this function will run whenever we go to this route
    return render_template('documentation.html')

@app.route('/doc_download')# Documentation downloa route
def doc_download():
    return send_file('static/Documentation.pdf', as_attachment=True, cache_timeout=0)

@app.route('/No_Gene') # this is the error page for when a gene that is not in the database is searched
def No_Gene(): # this function will run whenever we go to this route
    return render_template('No_Gene.html')

@app.route('/No_Position') # this is the error page for when a position not in the database is searched
def No_Position(): # this function will run whenever we go to this route
    return render_template('No_Position.html')

@app.route('/No_SNP') # this is the error page for when an SNP not in the database is searched
def No_SNP(): # this function will run whenever we go to this route
    return render_template('No_SNP.html')

@app.route('/No_Subpop') # this is the error page for when no sub-population is selected
def No_Subpop(): # this function will run whenever we go to this route
    return render_template('No_Subpop.html')

@app.route('/max_window') # Error page for when maximum search window is exceeded
def max_window():
    return render_template('max_window.html')

@app.route('/snp_info') # this page produces a table with the SNP information
def snp_info(): # this function will run whenever we go to this route

    # If a gene was searched
    try:

        # Use the session function to call a variable defined on another page
        gene=session['gene']

        # Search for all SNPs in the snp table in the specified gene
        mycursor.execute("SELECT CHROM, POS, GENE, ID, REF, ALT, FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM snp WHERE GENE LIKE %s ", [gene])
        data = mycursor.fetchall() # Store data 
        # Create pandas dataframe and then html tale of the collected data
        data=pd.DataFrame(data, columns=['Chromosome','Position', 'Gene','rsID','Reference','Alternate','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('snp_info.html', data=data)

    except:
        pass

    # If a SNP was searched 
    try:

        # Use the session function to call a variable defined on another page
        snp=session['snp']

        # Search for SNP in the snp table 
        mycursor.execute("SELECT CHROM, POS, GENE, ID, REF, ALT, FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM snp WHERE ID LIKE %s ", [snp])
        data = mycursor.fetchall() # Store data
        # Create pandas dataframe and then html tale of the collected data
        data=pd.DataFrame(data, columns=['Chromosome','Position', 'Gene','rsID','Reference','Alternate','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('snp_info.html', data=data)

    except:
        pass

    # If a location was searched 
    try:
        # Use the session function to call a variable defined on another page
        areastart=session['areastart']
        areaend=session['areaend']

        # Search for SNPs in the snp table in the specified range
        mycursor.execute("SELECT CHROM, POS, GENE, ID, REF, ALT, FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM snp WHERE %s <= POS AND POS <= %s ", (areastart, areaend ))
        data = mycursor.fetchall() # Store data
        # Create pandas dataframe and then html tale of the collected data
        data=pd.DataFrame(data, columns=['Chromosome','Position', 'Gene','rsID','Reference','Alternate','ALT|REF','REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=False)
        # Return the page with the stored table
        return render_template('snp_info.html', data=data)

    except:
        pass


@app.route('/BEB_info') # this is the documentation page
def BEB_info(): # this function will run whenever we go to this route

    # Need to handle it not being gene

    try:

        # Use the session function to call a variable defined on another page
        gene=session['gene']


        # Search for all SNPs in the subpop table in the specified gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Bengali' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
        BEB = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        BEB=pd.DataFrame(BEB, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('BEB_info.html', BEB=BEB)

    except:
        pass

    try:

        # Search for SNP in the snp table 
        snp=session['snp']

        # Search for SNP in the subpop table 
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'Bengali'", [snp])
        BEB = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        BEB=pd.DataFrame(BEB, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('BEB_info.html', BEB=BEB)

    except:
        pass

    try:

        # Use the session function to call a variable defined on another page
        areastart=session['areastart']
        areaend=session['areaend']

        # Search for SNPs in the subpop table in the specified range
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Bengali' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s)", (areastart, areaend))
        BEB = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        BEB=pd.DataFrame(BEB, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('BEB_info.html', BEB=BEB)

    except:
        pass



@app.route('/GBR_info') # this is the documentation page
def GBR_info(): # this function will run whenever we go to this route

    try:

        # Use the session function to call a variable defined on another page
        gene=session['gene']

        # Search for all SNPs in the subpop table in the specified gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'GBR' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
        GBR = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        GBR=pd.DataFrame(GBR, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('GBR_info.html', GBR=GBR)

    except:
        pass

    try:

        # Search for SNP in the snp table 
        snp=session['snp']

        # Search for SNP in the subpop table 
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'GBR'", [snp])
        GBR = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        GBR=pd.DataFrame(GBR, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('GBR_info.html', GBR=GBR)

    except:
        pass

    try:

        # Use the session function to call a variable defined on another page
        areastart=session['areastart']
        areaend=session['areaend']

        # Search for SNPs in the subpop table in the specified range
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'GBR' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s)", (areastart, areaend))
        GBR = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        GBR=pd.DataFrame(GBR, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('GBR_info.html', GBR=GBR)

    except:
        pass



@app.route('/CHB_info') # this is the documentation page
def CHB_info(): # this function will run whenever we go to this route

    try:

        # Use the session function to call a variable defined on another page
        gene=session['gene']

        # Search for all SNPs in the subpop table in the specified gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'China' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
        CHB = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        CHB=pd.DataFrame(CHB, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('CHB_info.html', CHB=CHB)

    except:
        pass

    try:
        # Use the session function to call a variable defined on another page
        snp=session['snp']

        # Search for SNP in the subpop table 
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'China'", [snp])
        CHB = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        CHB=pd.DataFrame(CHB, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('CHB_info.html', CHB=CHB)

    except:
        pass

    try:
        # Use the session function to call a variable defined on another page
        areastart=session['areastart']
        areaend=session['areaend']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'China' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s)", (areastart, areaend))
        CHB = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        CHB=pd.DataFrame(CHB, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('CHB_info.html', CHB=CHB)

    except:
        pass



@app.route('/PEL_info') # this is the documentation page
def PEL_info(): # this function will run whenever we go to this route

    try:

        # Use the session function to call a variable defined on another page
        gene=session['gene']

        # Search for all SNPs in the subpop table in the specified gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Peru' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
        PEL = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        PEL=pd.DataFrame(PEL, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('PEL_info.html', PEL=PEL)

    except:
        pass

    try:
        # Use the session function to call a variable defined on another page
        snp=session['snp']

        # Search for SNP in the subpop table 
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'Peru'", [snp])
        PEL = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        PEL=pd.DataFrame(PEL, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('PEL_info.html', PEL=PEL)

    except:
        pass

    try:
        # Use the session function to call a variable defined on another page
        areastart=session['areastart']
        areaend=session['areaend']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Peru' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s)", (areastart, areaend))
        PEL = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        PEL=pd.DataFrame(PEL, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('PEL_info.html', PEL=PEL)

    except:
        pass



@app.route('/ESN_info') # this is the documentation page
def ESN_info(): # this function will run whenever we go to this route

    try:

        # Use the session function to call a variable defined on another page
        gene=session['gene']

        # Search for all SNPs in the subpop table in the specified gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Nigeria' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
        ESN = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        ESN=pd.DataFrame(ESN, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('ESN_info.html', ESN=ESN)

    except:
        pass

    try:
        # Use the session function to call a variable defined on another page
        snp=session['snp']

        # Search for SNP in the subpop table 
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE ID LIKE %s AND SUBPOP LIKE 'Nigeria'", [snp])
        ESN = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        ESN=pd.DataFrame(ESN, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('ESN_info.html', ESN=ESN)

    except:
        pass

    try:
        # Use the session function to call a variable defined on another page
        areastart=session['areastart']
        areaend=session['areaend']

        # SNP info table - search all infor for SNPs in gene
        mycursor.execute("SELECT ID, SUBPOP, FORMAT(AF,5), FORMAT(ALTREF,5), FORMAT(REFALT,5), FORMAT(ALTALT,5), FORMAT(REFREF,5) FROM subpop WHERE SUBPOP LIKE 'Nigeria' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s)", (areastart, areaend))
        ESN = mycursor.fetchall() # store data
        # Create pandas dataframe and then html tale of the collected data
        ESN=pd.DataFrame(ESN, columns=['ID', 'SUBPOP', 'MAF', 'ALT|REF', 'REF|ALT', 'ALT|ALT', 'REF|REF']).to_html(classes='table table-stripped table-striped table-bordered table-sm', justify='left', index=False, show_dimensions=True, header=True)
        # Return the page with the stored table
        return render_template('ESN_info.html', ESN=ESN)

    except:
        pass

    

@app.route('/search_one') # Initia search page for user input
def search_one():

    # SNP distribution graph
    map_snp=snp_map(100000, mydb) # Only visible pre-search 

    return render_template('search_one.html', map_snp=map_snp)

@app.route('/search_out_snp') # Search results when only an SNP is searched
def search_out_snp():
    
    pos = session['pos'] # call the session position variable
    snp=session['snp'] # call the session snp variable

    # Gene map graph relevant to the search
    gene_map=gene_list_graph(pos, mydb, 1000000)

    return render_template('search_out_snp.html', gene_map=gene_map, snp=snp)



@app.route('/search_out', methods=['GET', 'POST']) # this is the search results page for gene or location search
def search_out(): # this function will run whenever we go to this route


    select=request.form['select'] # The option selected from dopdown bar

    #Time how long the search takes to run
    start_time = time.time()
    
    try:
        # Create a list containing the population codes of selected sub-populations
        subpop=request.form.getlist('subpop')

    except:

        # If no populations are selected
        return 'You must select at least one population'

    
    if len(subpop) == 0: # check that at least one sub-population has been selected
        # If no subpopulations selected return error page
        return render_template('No_Subpop.html')

    else: # If at least one sub-population has been selected

        # Define empty strings that will be filled if subpop selected
        # If subpop not selected then link button will be blank due to empty string here
        bclick=''
        gclick=''
        cclick=''
        pclick=''
        eclick=''
        
        # Iterate over the sub-populations selected
        for item in subpop:
            # If sub-population in list/subpop selected
            if item == 'BEB':
                # Name the link button that will appear on the results page
                bclick='Open BEB SNP Infomormation'

            elif item == 'GBR':
                gclick='Open GBR SNP Infomormation'

            elif item == 'CHB':
                cclick='Open CHB SNP Infomormation'
            
            elif item == 'PEL':
                pclick='Open PEL SNP Infomormation'
                
            elif item == 'ESN':
                eclick='Open ESN SNP Infomormation'
            
            else:
                pass

        # If searching by snp name (from select menu)
        if select == 'SNP Name':

            # Create a string of the sub-populations searched to output to the user 
            sp=str(subpop).strip("[]")
            sp=sp.replace("'","")
            Searched_pops='Sub-Populations searched: ' + sp + '.'

            # Check that searched SNP is in the databse
            mycursor.execute("SELECT ID FROM snp") # Select all rsIDs from snp table
            snptbl_rsIDs=mycursor.fetchall() # list of tuples of strings of all rsIDs
            snptbl_rsIDs=[a for item in snptbl_rsIDs for a in item] # list of strings of all rsIDs

            # Define snp as the text box search input
            snp = request.form['snp']

            # Check that the searched snp is in the list of all snps
            if snp in snptbl_rsIDs:

                # define snp as a variable that can be called on other pages
                session['snp']=snp # using session function

                # Select position for gene distribution graph
                mycursor.execute("SELECT POS FROM snp WHERE ID = %s ", [snp]) # extract position of snp from database
                pos = float(str(mycursor.fetchall()).strip("''[](),")) # Position as a float

                # define snp position as a variable that can be called on other pages
                session['pos']=pos

                # Gene map graph relevant to the snp search
                gene_map=gene_list_graph(pos, mydb, 1000000)
                
                # Return runtime of search/data extraction
                runtime=('Search time: '+ str(time.time() - start_time)+ ' seconds.')  

                # Return the search template with these vairables newly defined 
                return render_template('search_out_snp.html',
                                        runtime=runtime,
                                        gene_map=gene_map,
                                        Searched_pops=Searched_pops,
                                        bclick=bclick, 
                                        gclick=gclick,
                                        cclick=cclick,
                                        pclick=pclick,
                                        eclick=eclick
                                        )
            else: # If the SNP not found in database 

                return render_template('No_SNP.html') # SNP error page
        
        # If searching by Gene name (from select menu)
        if select == 'Gene Name':

            # Store the gene name entered into the text search box as a string
            gene = request.form['snp'].upper()

            # define the gene name as a variable that can be called on other pages
            session['gene']=gene

            # Create a string of the sub-populations searched to output to the user 
            sp=str(subpop).strip("[]")
            sp=sp.replace("'","")
            Searched_pops='Sub-Populations searched: ' + sp + '.'


            # Check that search item is in the databse
            mycursor.execute("SELECT GENE FROM snp") # Select all genes from snp table
            snptbl_genes=mycursor.fetchall() # list of tuples of strings of all genes
            snptbl_genes=[a for item in snptbl_genes for a in item] # list of strings of all genes

            if gene in snptbl_genes: # Gene is in the list of all genes 

                # Search the SNP table for all SNPs in that gene - for counting
                mycursor.execute("SELECT ID FROM snp WHERE GENE LIKE %s ", [gene])
                allsnps=mycursor.fetchall()
                snps = len(allsnps) # Store data in a list
                # String stating the number of SNPs in the specified gene - counter
                num_snps = ('Number of SNPs found in ' + gene.upper() + ': ' + (str(snps) + '.')) 


                # Select position for gene distribution graph
                mycursor.execute("SELECT POS FROM snp WHERE GENE = %s ", [gene])
                pos = float(str(mycursor.fetchone()).strip("''[](),")) # Position number

                # Gene map graph relevant to the gene searched
                gene_map=gene_list_graph(pos, mydb, 1000000)

                
                ################ FST #######################

                # Select genotype string for SNPs in searched gene
                mycursor.execute("SELECT GT FROM snp WHERE GENE LIKE %s ", [gene])
                geno_list = mycursor.fetchall()

                #Make genotype array
                array=makeArray(geno_list)

                #### create FST table ####
                fst_T = all_hudson_fsts(array, subpop)

                #### Creating an FST graph ####
                # Select all positions in the gene region
                mycursor.execute("SELECT POS FROM snp WHERE GENE = %s",[gene])
                positions=mycursor.fetchall()
                positions=[float(a) for item in positions for a in item] # convert output to a list of strings
                # Sort the positions in ascending order
                sorting=positions
                sorting.sort(reverse=False, key=float)

                # Create a variable of the distance between the first and final positions
                dist=(sorting[-1]-sorting[0])
                dist=int(0.1*dist) # define dist as 10% of the total distance between first and last position
                
                # Create a dictionary that can be used as input for the graph function
                fst_G=fst_dict_calc(positions, array, subpop, dist ) # Outputs a nested dictionry with FST for each bin and for each subpop

                # Generate html graph from the first and last positions of the gene
                fst_G=FSTscatter(fst_G, int(positions[0]), int(positions[-1]))

                
                #################### Shannon Diversity #######################

                # Empty lists of tuples of strings for subpops not selected
                BAF=[('1')]
                GAF=[('1')]
                CAF=[('1')]
                PAF=[('1')]
                EAF=[('1')]

                # Extract allele frequency data from databse for selected populations
                for item in subpop:

                    if item == 'BEB': # If population selected
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'Bengali' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        BAF=mycursor.fetchall() #list of tuples

                    elif item == 'GBR':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'GBR' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        GAF=mycursor.fetchall() #list of tuples
                    
                    elif item == 'CHB':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'China' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        CAF=mycursor.fetchall() #list of tuples

                    elif item == 'PEL':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'Peru' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        PAF=mycursor.fetchall() #list of tuples
                    
                    elif item == 'ESN':
                        mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'Nigeria' AND ID IN (SELECT ID FROM snp WHERE GENE LIKE %s)", [gene])
                        EAF=mycursor.fetchall() #list of tuples
                    
                    else:
                        pass
                
            
                # Calculate shannon diversity
                # Create shannon diversity tabele
                shan_T=Shannon(allsnps, BAF, GAF, CAF, PAF, EAF, subpop)
                # Produce dictionary input for shannon diversity graoh function
                shan_G=ShannonG(allsnps, BAF, GAF, CAF, PAF, EAF, subpop, positions)
                # Create shannon diversity graoh
                shan_G=ShannonGraph(shan_G)


                #################### Tajimas D ######################

                # Create Tajimas D table
                taj_T=Tajimas(array, subpop)
                # Create input dictionary for Tajimas graph function
                taj_G=taj_dict_calc(positions, array, subpop, dist/2)
                # Create tajimas d graph for positions of specified gene
                taj_G=TD_Bar(taj_G, int(positions[0]), int(positions[-1]))


                ################## Haplotype diversity #######################

                # Create haplotype diversity table
                haplo_T=haplotype_diversity2T(positions, array, subpop, snpnum=100)
                # Create dictionary input for haplotype diversity graph function
                haplo_G=haplotype_diversity2G(positions, array, subpop, snpnum=50)
                # Create haplotype diversity graph
                haplo_G=hp_Bar(haplo_G, int(positions[0]), int(positions[-1]))

                
                
                # Return runtime of search/data extraction
                runtime=('Search time: '+ str(time.time() - start_time)+ ' seconds.')

                # Return the search template with these vairables newly defined 
                return render_template('search_out.html',
                                        num_snps=num_snps,
                                        runtime=runtime,
                                        gene_map=gene_map,
                                        Searched_pops=Searched_pops,
                                        bclick=bclick, 
                                        gclick=gclick,
                                        cclick=cclick,
                                        pclick=pclick,
                                        eclick=eclick,
                                        fst_T=fst_T,
                                        fst_G=fst_G,
                                        shan_T=shan_T,
                                        shan_G=shan_G,
                                        taj_T=taj_T,
                                        taj_G=taj_G,
                                        haplo_T=haplo_T,
                                        haplo_G=haplo_G
                                        )


            else: # Gene not in database

                return render_template('No_Gene.html') # gene error page 


        # If searching by location/position (from select menu)
        if select == 'Location':

            # Store the positions entered into the text search box as a string
            location = request.form['snp']

            try:
                # Split the tring at the dash 
                location=location.split('-')
                # Turn the two numbers in the list in to inetgers and seperate them
                areastart=int(location[0])
                areaend=int(location[1])
            except:
                return render_template('No_Position.html') # no positions error page


            if areaend-areastart > 1000000:

                return render_template('max_window.html')
            else:

                # Save start and end positions as variable that can be called on other pages
                session['areastart']=areastart
                session['areaend']=areaend

                # Create a string of the sub-populations searched to output to the user 
                sp=str(subpop).strip("[]")
                sp=sp.replace("'","")
                Searched_pops='Sub-Populations searched: ' + sp + '.'

                # Check that search range is in the databse
                mycursor.execute("SELECT POS FROM snp") # Select all positions from snp table
                snptbl_position=mycursor.fetchall() # list of tuples of strings of all positions
                snptbl_position=[float(a) for item in snptbl_position for a in item] # list of strings of all positions

                # Count the number of positions within the specified range found in the database
                not_out_of_bounds=0
                for item in snptbl_position:

                    if item > areastart and item < areaend: # if position falls in given range
                        not_out_of_bounds+=1
                    else:
                        pass
                
                if not_out_of_bounds > 0: # If positon range given conatains at least one snp


                    # Search the SNP table for all SNPs in that gene - for counting
                    mycursor.execute("SELECT ID FROM snp WHERE %s <= POS AND POS <= %s ", (areastart, areaend ))
                    allsnps=mycursor.fetchall()
                    snps = len(allsnps) # Store data in a list
                    # String containing the number of SNPs in the gene - counter
                    num_snps = ('Number of SNPs found in the range of ' + str(areastart) + ' - ' + str(areaend) + ': ' + (str(snps) + '.'))

                    # Gene map graph relevant to the search
                    gene_map=gene_list_graph(areastart, mydb, 1000000)


                    ################ FST #######################

                    # Select genotype string for SNPs in searched gene
                    mycursor.execute("SELECT GT FROM snp WHERE %s <= POS AND POS <= %s ", (areastart, areaend ))
                    geno_list = mycursor.fetchall()

                    #Make genotype array
                    array=makeArray(geno_list)

                    #### create FST table ####
                    fst_T = all_hudson_fsts(array, subpop)

                    #### Creating an FST graph ####
                    # Select all positions in the gene region
                    mycursor.execute("SELECT POS FROM snp WHERE %s <= POS AND POS <= %s ", (areastart, areaend ))
                    positions=mycursor.fetchall()
                    positions=[float(a) for item in positions for a in item] # convert output to a list of strings
                    # Sort the positions in ascending order
                    sorting=positions
                    sorting.sort(reverse=False, key=float)

                    # Create a variable of the distance between the first and final positions
                    dist=(sorting[-1]-sorting[0])
                    dist=int(0.1*dist) # define dist as 10% of the total distance between first and last position
                    
                    # Create a dictionary that can be used as input for the graph function
                    fst_G=fst_dict_calc(positions, array, subpop, dist ) # Outputs a nested dictionry with FST for each bin and for each subpop

                    # Generate html graph from the first and last positions of the gene
                    fst_G=FSTscatter(fst_G, int(positions[0]), int(positions[-1]))

                    
                    #################### Shannon Diversity #######################

                    # Empty lists of tuples of strings for subpops not selected
                    BAF=[('1')]
                    GAF=[('1')]
                    CAF=[('1')]
                    PAF=[('1')]
                    EAF=[('1')]

                    # Extract allele frequency data from databse for selected populations
                    for item in subpop:

                        if item == 'BEB': # If population selected
                            mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'Bengali' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                            BAF=mycursor.fetchall() #list of tuples

                        elif item == 'GBR':
                            mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'GBR' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                            GAF=mycursor.fetchall() #list of tuples
                        
                        elif item == 'CHB':
                            mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'China' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                            CAF=mycursor.fetchall() #list of tuples

                        elif item == 'PEL':
                            mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'Peru' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                            PAF=mycursor.fetchall() #list of tuples
                        
                        elif item == 'ESN':
                            mycursor.execute("SELECT FORMAT(AF, 5) FROM subpop WHERE SUBPOP LIKE 'Nigeria' AND ID IN (SELECT ID FROM snp WHERE %s <= POS AND POS <= %s) ", (areastart, areaend ))
                            EAF=mycursor.fetchall() #list of tuples
                        
                        else:
                            pass
                    
                
                    # Calculate shannon diversity
                    # Create shannon diversity tabele
                    shan_T=Shannon(allsnps, BAF, GAF, CAF, PAF, EAF, subpop)
                    # Produce dictionary input for shannon diversity graoh function
                    shan_G=ShannonG(allsnps, BAF, GAF, CAF, PAF, EAF, subpop, positions)
                    # Create shannon diversity graoh
                    shan_G=ShannonGraph(shan_G)


                    #################### Tajimas D ######################

                    # Create Tajimas D table
                    taj_T=Tajimas(array, subpop)
                    # Create input dictionary for Tajimas graph function
                    taj_G=taj_dict_calc(positions, array, subpop, dist/2)
                    # Create tajimas d graph for positions of specified gene
                    taj_G=TD_Bar(taj_G, int(positions[0]), int(positions[-1]))


                    ################## Haplotype diversity #######################

                    # Create haplotype diversity table
                    haplo_T=haplotype_diversity2T(positions, array, subpop, snpnum=100)
                    # Create dictionary input for haplotype diversity graph function
                    haplo_G=haplotype_diversity2G(positions, array, subpop, snpnum=50)
                    # Create haplotype diversity graph
                    haplo_G=hp_Bar(haplo_G, int(positions[0]), int(positions[-1]))

                    
                    # Return runtime of search/data extraction
                    runtime=('Search time: '+ str(time.time() - start_time)+ ' seconds.')

                    # Return the search template with these vairables newly defined
                    return render_template('search_out.html',
                                            num_snps=num_snps,
                                            runtime=runtime,
                                            gene_map=gene_map,
                                            Searched_pops=Searched_pops,
                                            bclick=bclick, 
                                            gclick=gclick,
                                            cclick=cclick,
                                            pclick=pclick,
                                            eclick=eclick,
                                            fst_T=fst_T,
                                            fst_G=fst_G,
                                            shan_T=shan_T,
                                            shan_G=shan_G,
                                            taj_T=taj_T,
                                            taj_G=taj_G,
                                            haplo_T=haplo_T,
                                            haplo_G=haplo_G
                                            )

                else:

                    return render_template('No_Position.html') # Location not valid error


        





if __name__ == '__main__': # only if we run this file will we execute the line below
    # run the Flask app & start a web server
    app.run(debug=True) # debug means that if code changes server is auto re-run
