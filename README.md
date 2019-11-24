Vcf_Converter.py is a tool used to convert vcf file in a `.Sample` file format for the TreeWAS tool. The output file is the following (0/1/2 = HomRef/Het/HomAlt):

```
ID Genotype
sample_0 0
sample_1 1
sample_2 0
sample_3 0
sample_4 2
sample_5 1
sample_6 0
```

The input file is a vcf file.
Vcf_Converter does not convert a `VCF` file having MORE THAN ONE variant and the format is the following:

```
#CHROM  POS ID  REF ALT QUAL    FILTER  INFO    FORMAT  sample_0    sample_1
17  7571752 rs78378222,17:7571752_T_G   T   G   .   .   .   GT:GP   0/0:1,0,0   0/0:1,0,0
```
The sample name in the sample column of the vcf file will be the same in the output file. This tool works only on bi-allelic sites and converts 0/0 in 0, 0/1 in 1 and 1/1 in 2..