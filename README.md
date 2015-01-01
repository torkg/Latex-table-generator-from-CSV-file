latex-table-generator of data in a CSV file
==============================================

latex table generator with python script

MAJOR BUG! it ruins the readfile so use a copy! I think happens because I read the csv file twice. First 
to get rid of some character ( \x00 ) that give NULL byte error. Then the second round read in the data and write to a 
tex file. 

If there is no NULL error you can just comment out the first read and everything should be fine. 

It uses the longtable package in latex and output an tex file. So include \usepackage{longtable} in the preamble
for your latex project.
