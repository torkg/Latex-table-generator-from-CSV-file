#======================================
import sys
import csv
#======================================


#===================
# GIVE READFILE
#===================
# angi: 
# - filen det skal leses fra 
# - paa hvilken linje dataene starter og slutter
# - forste og siste kollonne som skal leser inn

file = 'xy.dat'; data_startline = 0; data_stopline = -1; col_start = 0; col_stop = 1; caption = "Raadata til forsok 2"; label = "tab: forsok2raw"

#file = 'forsok1_1.csv'; data_startline = 13; data_stopline = -1; col_start = 2; col_stop = 6; delimiter = ';' ;caption = "Raadata til forsok 2"; label = "tab: forsok2raw"

#file = 'forsok1_1 (copy).csv'; data_startline = 13; data_stopline = -1; col_start = 2; col_stop = 6; delimiter = ';' ;caption = "Raadata til forsok 2"; label = "tab: forsok2raw"

#file = 'forsok2_1 (copy).csv'; data_startline = 13; data_stopline = 507; col_start = 2; col_stop = 6; delimiter = ';'; caption = "Raadata til forsok 1"; label = "tab: forsok1raw"

#file = 'csv_testdata.csv'; data_startline = 3; col_start = 1; col_stop = 4; delimiter = ';' ;caption = "Tabelltekst her  lissom"; label = "tab: tabell"


#======================================
# END GIVE READFILE
#======================================


#======================================
# READ RAW: leser inn infile og lukker filen etterpa
#=====================================
def ReadRAW( file ):
    infile = open(file, "r")
    lines = infile.readlines()
    infile.close()
    
    for line in lines:
        print line
    return lines

#======================================
# END READ RAW
#======================================


#======================================
# READCSV:Leser inn CSV-fil
#=====================================
def ReadCSV( file ):

    #---------------------------------
    # Blokk som fjerner NULL byte Error
    #---------------------------------
    infile = open(file, 'rb')
    data = infile.read()
    infile.close()
    
    outfile = open(file, 'wb')
    outfile.write( data.replace('\x00', '') )
    #outfile.write( data.replace('\xff', '') )
    #outfile.write( data.replace('\xfe', '') )
    outfile.close()
    #---------------------------------

    #---------------------------------
    # Her starter innlesningen av filen
    #-----------------------------------
    lines = []
    with open(file, 'rb') as csvfile:
        
        spamreader = csv.reader(csvfile, delimiter=';')
                
        for row in spamreader:
#            print row
            lines.append( row )
    #------------------------------------

    return lines

#========================================
# END READCSV
#=====================================


if file[-3:] == "csv":
    lines = ReadCSV(file)
    csv = 1
else:
    lines = ReadRAW(file)


#==================================================
# GIVE WRITEFILE: Filen det skal skrives til 
#=================================================

writefile = "table_test.tex"
#writefile = file[:-11] + "_table.tex"


# apner filen det skal skrives til
#---------------------------------------
outfile = open(writefile, "w")


#=====================================================
# END GIVE WRITEFILE
#=====================================================


#====================================================
# WRITE DATA TO FILE 
#====================================================

#=======================================================
def ColNames():

    for i in range(0, num_cols):
        
        # sa lenge det ikke er det siste kolonnenavnet
        if (i != num_cols-1 ):
            
            if i==0:
                outfile.write("\multicolumn{1}{|c|}{\\textbf{ %s }} & \n" % col_names[i] )
            
            else:
                outfile.write("\multicolumn{1}{c|}{\\textbf{ %s }} & \n" % col_names[i] )

    # for den siste kolonnetitelen
        else:
            outfile.write("\multicolumn{1}{c|}{\\textbf{ %s }} \\\\" % col_names[i] )

#=======================================================

# skriver starten pa tabellen
#--------------------------------------------
num_cols = col_stop - col_start + 1
nc = " c " * num_cols 

start_table = """\\begin{center} 
\\begin{longtable}{%s} 
\\caption{%s} 
\\label{%s} \\\\ \n""" %(nc, caption, label) 

outfile.write(start_table)

# skriver ut kolonnetitlene
if csv:
    col_names = lines[data_startline-1][col_start:col_stop+1]

outfile.write("\n\hline \n")


ColNames() # skriver kolonnenavn          
outfile.write("\\hline")  
outfile.write("\n\endfirsthead \n\n")

split_header_toptext = "Fortsettelse fra forrige side"
splitpage_header1 = "\multicolumn{%d}{c} \n{{\\bfseries \\tablename\ \\thetable{} %s}} \n\\\\ \n\hline " %(num_cols, split_header_toptext)
outfile.write(splitpage_header1)

ColNames()

split_header_bottomtext = "Fortsetter paa neste side"
splitpage_header2 = """\n\endhead

\n\hline \multicolumn{%d}{|r|}{{ %s }} \\\\ \hline
\endfoot \\\\

\hline \hline \\\\
\endlastfoot \n""" %(num_cols, split_header_bottomtext) 
outfile.write(splitpage_header2)

#-----------------------------------------------
# skriver ut dataene i filen linje for linje
#------------------------------------------------

i = 0
for line in lines[data_startline : data_stopline]:

    j = col_start
    for word in line[col_start : col_stop+1]:

        word = word.strip()
        print word
        # sa lenge det ikke er siste kolonn
        if j < col_stop:
#            outfile.write("%8.3f & " %( float(word) ))
            outfile.write("%s & " %( word ) )
            j += 1

        # til slutt for siste kolonne
        else:
#            outfile.write("%8.3f  " % float(word))
            outfile.write("%s" %( word ) )
             
    if i != (len(lines) - 1):
          outfile.write(" \\\\ \\hline \n")

    elif i == len(lines) - 1:
        outfile.write(" \\\\ \\hline \n")

    i += 1
#------------------------------------------------

# skriver siste linjene til tabellkoden
outfile.write("\\end{longtable}\n")
outfile.write("\\end{center}\n")

# lukker filen 
outfile.close()
