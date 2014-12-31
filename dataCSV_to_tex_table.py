#======================================
import sys
import csv
#======================================


#===================
# GIVE READFILE
#=================== 
# - give start and stop line
# - first and last col be read

file = 'forsok1_1.csv'
data_startline = 13
data_stopline = -1
col_start = 2
col_stop = 5
delimiter = ';'
caption = "Raadata til forsok 2"
label = "tab: forsok2raw"

#file = 'forsok1_1 (copy).csv'; data_startline = 13; data_stopline = -1; col_start = 2; col_stop = 6; delimiter = ';' ;caption = "Raadata til forsok 2"; label = "tab: forsok2raw"

#file = 'forsok2_1 (copy).csv'; data_startline = 13; data_stopline = 507; col_start = 2; col_stop = 6; delimiter = ';'; caption = "Raadata til forsok 1"; label = "tab: forsok1raw"

#file = 'csv_testdata.csv'; data_startline = 3; col_start = 1; col_stop = 4; delimiter = ';' ;caption = "Tabelltekst her  lissom"; label = "tab: tabell"


#======================================
# END GIVE READFILE
#======================================


#======================================
# READCSV:Leser inn CSV-fil
#=====================================
def ReadCSV( file ):

    #--------------------------------------
    # Block to revmove NULL byte Error char
    # This block is ruining the readfile after
    #--------------------------------------
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
    # Starting to read the file
    #-----------------------------------
    lines = []
    with open(file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            lines.append( row )
    #------------------------------------

    return lines

#========================================
# END READCSV
#=====================================

#==================================================
# GIVE WRITEFILE: Filen det skal skrives til 
#=================================================

lines = ReadCSV(file)

writefile = "table_test.tex"
#writefile = file[:-11] + "_table.tex"


# opens the write file
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
        
        # as long as it is not the last col
        if (i != num_cols-1 ):
            
            if i==0:
                outfile.write("\multicolumn{1}{|c|}{\\textbf{ %s }} & \n" % col_names[i] )
            
            else:
                outfile.write("\multicolumn{1}{c|}{\\textbf{ %s }} & \n" % col_names[i] )

    # for the last col
        else:
            outfile.write("\multicolumn{1}{c|}{\\textbf{ %s }} \\\\" % col_names[i] )

#=======================================================

# writes the tex code to start longtable
#--------------------------------------------
num_cols = col_stop - col_start + 1
nc = " c " * num_cols 

start_table = """\\begin{center} 
\\begin{longtable}{%s} 
\\caption{%s} 
\\label{%s} \\\\ \n""" %(nc, caption, label) 

outfile.write(start_table)

# writes the col titles
if csv:
    col_names = lines[data_startline-1][col_start:col_stop+1]

outfile.write("\n\hline \n")


ColNames() # writes the col names        
outfile.write("\\hline")  
outfile.write("\n\endfirsthead \n\n")

# spilt header top text
split_header_toptext = "Fortsettelse fra forrige side"
splitpage_header1 = "\multicolumn{%d}{c} \n{{\\bfseries \\tablename\ \\thetable{} %s}} \n\\\\ \n\hline " %(num_cols, split_header_toptext)
outfile.write(splitpage_header1)

ColNames()

# spilt header bottom text
split_header_bottomtext = "Fortsetter paa neste side"
splitpage_header2 = """\n\endhead

\n\hline \multicolumn{%d}{|r|}{{ %s }} \\\\ \hline
\endfoot \\\\

\hline \hline \\\\
\endlastfoot \n""" %(num_cols, split_header_bottomtext) 
outfile.write(splitpage_header2)

#-----------------------------------------------
# writes the data to tex file
#------------------------------------------------

i = 0
for line in lines[data_startline : data_stopline]:

    j = col_start
    for word in line[col_start : col_stop+1]:

        word = word.strip()
        print word
        # as long as it is not the last line
        if j < col_stop:
#            outfile.write("%8.3f & " %( float(word) ))
            outfile.write("%s & " %( word ) )
            j += 1

        # the last line
        else:
#            outfile.write("%8.3f  " % float(word))
            outfile.write("%s" %( word ) )
             
    if i != (len(lines) - 1):
          outfile.write(" \\\\ \\hline \n")

    elif i == len(lines) - 1:
        outfile.write(" \\\\ \\hline \n")

    i += 1
#------------------------------------------------

# ending the table
outfile.write("\\end{longtable}\n")
outfile.write("\\end{center}\n")

# close the write file
outfile.close()
