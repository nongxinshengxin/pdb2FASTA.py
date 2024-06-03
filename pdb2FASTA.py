#!/usr/bin/env python3

import os
import re
from collections import defaultdict
import argparse


class pdbChange():
    def __init__(self,inputs,outputs=""):
        self.inputs=inputs
        self.outputs=outputs

    def readfile(self):
        for file in os.listdir(f"{self.inputs}"):
            with open(f"{self.inputs}/{file}") as f:
                for line in f:
                    yield file,line
    

    def pdb2fasta(self):
        aa_dict = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G', 'HIS': 'H',
'ILE': 'I', 'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S', 'THR': 'T', 'TRP': 'W',
'TYR': 'Y', 'VAL': 'V'}
        fasta_dict=defaultdict(list)
        for file,line in self.readfile():
            file=file[:-4]
            line=re.split("\s+",line)
            if len(line) >=6:
                if aa_dict.get(line[3]):
                    if not fasta_dict[file] or fasta_dict[file][-1] != (aa_dict[line[3]],line[5]):
                        fasta_dict[file].append((aa_dict[line[3]],line[5]))
                    else:
                        continue

                else:
                    continue
            else:
                continue
        if self.outputs:
            outfile=self.outputs
        else:
            outfile=f"{self.inputs}/out.fasta"
        with open(outfile,"w") as w:
            newdict=defaultdict(list)
            for key,value in fasta_dict.items():
                for aa in value:
                    newdict[key].append(aa[0])
                
            #print(newdict)

            for key in newdict.keys():
                w.write(f">{key}\n")
                w.write(f"{''.join(newdict[key])}\n")


              



def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('PDBdir',type=str,help='存储PDB文件的目录')
    parser.add_argument('output_fasta',type=str,nargs='?',help='输出的fasta文件所在路径以及名称，如未设置，默认在pdb文件存储路径，名称为out.fasta')
    args=parser.parse_args()

    pdb=pdbChange(args.PDBdir,args.output_fasta)
    pdb.pdb2fasta()


if __name__=="__main__":
    main()
