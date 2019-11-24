import argparse

# --> Command:
# python3 /Users/matteo/git/MyREPO/SCRIPT_LICR/PYTHON_SCRIPT/UKB-Scripts/VCF-CONVERTER/Vcf_Converter.py /
# -I /Users/matteo/Desktop/OUTPUT_FILES/rs78378222_filtered.vcf /
# -O /Users/matteo/Desktop/OUTPUT_FILES/Genotypes_rs78378222
# -Stat

if __name__ == '__main__':

    parser = argparse.ArgumentParser('This tool convert vcf genotypes in .Sample file to be used in TreeWAS.')

    parser.add_argument('-I','--input',help="path to the vcf input file")
    parser.add_argument('-O','--out',help="path to the .Sample output file without specify the extension (automatically added by Vcf_converter). For example, as path/to/file/Ukb-data")
    parser.add_argument('-Stat','--Statfile',action="store_true",help="Report a Statistical file including number of HomRef, Het, HomAlt and their frequencies.")
    parser.add_argument('-Plot','--Plotgraph',action="store_true",help="Report a plot including summary informations.")


    global opts

    print('\n\nBioinformatic to rule them all, Bioinformatic to find them, Bioinformatic to bring them all, and in the darkness bind them\n\n')

    opts = parser.parse_args()

    out_str1 = opts.out + '_' + 'Genotypes.Sample'
    out_str2 = opts.out + '_' + 'Stat.txt'

    Sample_out = open(out_str1,'w')
    Stat_out = open(out_str2,'w')

    Count_genotypes = {}

    Count_genotypes['HomRef'] = 0
    Count_genotypes['Het'] = 0
    Count_genotypes['HomAlt'] = 0
    Count_genotypes['Total'] = 0
    Count_genotypes['Missing'] = 0
    Count_genotypes['Allele_Number'] = 0
    Count_genotypes['Allele_Count'] = 0
    Count_genotypes['Ref_Count'] = 0
    Count_genotypes['Alt_Count'] = 0

    with open(opts.input) as vcf:

        for row in vcf:

            row = row.rstrip()
            row = row.split('\t')

            if row[0].startswith('##'):
                continue

            elif row[0].startswith('#CHROM'):

                header = row

                new_header = ['ID', 'Sample']

                Sample_out.write('\t'.join(new_header) + '\n')

            else:

                REF_Allele = row[header.index('REF')]
                ALT_Allele = row[header.index('ALT')]

                # For loop over all the samples in the vcf file header. Since all the sample are written in
                # the format 'sample_X' with X = (number of the sample)
                for samples in header:

                    # Skip the non-sample header
                    if 'sample_' not in samples:
                        continue

                    else:
                        GT = row[header.index(samples)].split(':')[0]

                        if opts.Statfile:
                            Count_genotypes['Total'] += 1
                            Count_genotypes['Allele_Number'] += 2

                        if GT == '0/0':
                            genotype = '0'
                            if opts.Statfile:
                                Count_genotypes['HomRef'] += 1
                                Count_genotypes['Ref_Count'] += 2

                        elif GT == '0/1':
                            genotype = '1'
                            if opts.Statfile:
                                Count_genotypes['Het'] += 1
                                Count_genotypes['Allele_Count'] += 1
                                Count_genotypes['Ref_Count'] += 1
                                Count_genotypes['Alt_Count'] += 1


                        elif GT == '1/1':
                            genotype = '2'
                            if opts.Statfile:
                                Count_genotypes['HomAlt'] += 1
                                Count_genotypes['Allele_Count'] += 2
                                Count_genotypes['Alt_Count'] += 2

                        else:
                            if opts.Statfile:
                                Count_genotypes['Missing'] += 1
                                Count_genotypes['Allele_Number'] -= 2
                            continue

                    Sample_out.write(samples + '\t' + genotype + '\n')

        Total_No_Miss=Count_genotypes['Total']-Count_genotypes['Missing']

        Missing = '# Missing genotypes: '+str(Count_genotypes['Missing'])
        HomRef = '# HomRef genotypes: '+str(Count_genotypes['HomRef'])
        Het = '# Het genotypes: '+str(Count_genotypes['Het'])
        HomAlt = '# HomAlt genotypes: '+str(Count_genotypes['HomAlt'])
        Total = '# Total samples (including missing genotypes): '+str(Count_genotypes['Total'])
        Total_no_missing = '# Total samples (excluding missing genotypes): '+str(Total_No_Miss)
        Separator = '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
        Percentage = 'Allele and genotype frequencies (excluding missing genotypes):'
        Missing_perc = '% Missing genotypes: '+str(float(Count_genotypes['Missing'])/float(Total_No_Miss))
        HomRef_perc = '% HomRef genotypes: '+str(float(Count_genotypes['HomRef'])/float(Total_No_Miss))
        Het_perc = '% Het genotypes: '+str(float(Count_genotypes['Het'])/float(Total_No_Miss))
        HomAlt_Perc = '% HomAlt genotypes: '+str(float(Count_genotypes['HomAlt'])/float(Total_No_Miss))
        Ref_perc = 'Ref Allele - '+str(REF_Allele)+': '+str(float(Count_genotypes['Ref_Count'])/float(Count_genotypes['Allele_Number']))
        Alt_Perc = 'Alt Allele - '+str(ALT_Allele)+': '+str(float(Count_genotypes['Alt_Count'])/float(Count_genotypes['Allele_Number']))

        Stamp = [Missing]+[HomRef]+[Het]+[HomAlt]+[Total]+[Total_no_missing]+[Separator]+[Percentage]+[Missing_perc]+[HomRef_perc]+[Het_perc]+[HomAlt_Perc]+[Ref_perc]+[Alt_Perc]

        Stat_out.write('\n'.join(Stamp))

    Sample_out.close()
    Stat_out.close()








