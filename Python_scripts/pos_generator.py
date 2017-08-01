#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 10:39:38 2017

Testing out writing text files, plan to use this approach to generate .pos
files for LAMMPS

@author: as14014
"""

from datetime import datetime

def generate_pos(name=datetime.now().strftime('%d-%m_%H.%M')+".pos",wall_gap_multiplier=3,\
                 total_number_of_atoms=16,atomic_spacing=0.45,vacuum_gap_multiplier=3):
    atoms = str(int(total_number_of_atoms))
    bonds = str(total_number_of_atoms - 2)
    spacing = atomic_spacing
    vacuum_gap = vacuum_gap_multiplier * spacing
    x_lo = str(-3*spacing)
    x_hi = str( (total_number_of_atoms - 1)*spacing + vacuum_gap + 3*spacing )
    y_lo = str( -2*spacing)
    y_hi = str( 2*spacing)
    z_lo = str( -0.00110000)
    z_hi = str( 0.00110000)
    
    f = open(file=name,mode='x')
    
    f.write(atoms+"x1x1 (001) layers of simple cubic lattice \n \n" )
    f.write(atoms+" atoms \n"+bonds+" bonds \n \n")
    
    f.write("2 atom types \n1 bond types \n \n")
    
    f.write(x_lo+" "+x_hi+" xlo xhi \n")
    f.write(y_lo+" "+y_hi+" ylo yhi \n")
    f.write(z_lo+" "+z_hi+" zlo zhi \n \n")
    
    f.write("Atoms \n \n")
    
    atom_ids = range(1,total_number_of_atoms+1)
    half_number = int(total_number_of_atoms / 2)
    
    for i in atom_ids:
        
        atom_id = str(i)
        position = str( i*spacing )
        zero_string = str("    0.00000000    0.00000000") #since y,z coords are 0 for 1D 
        
        if i <= half_number:
            
            atom_type = str(1)
            molecule_type = str(1)
            f.write("%s %s %s %s %s \n" %(atom_id,molecule_type,atom_type,position,zero_string))
                  
        else:
            atom_type = str(2)
            molecule_type = str(2)
            f.write("%s %s %s %s %s \n" %(atom_id,molecule_type,atom_type,position,zero_string))
        
    
    f.write("\n")
    f.write("Bonds \n \n")
    
    bond_type = "1"
    
    for i in atom_ids[:half_number-1]:
        
        source_atom = str(i)
        target_atom = str(i+1)
        f.write("%s %s %s %s \n" %(i,bond_type,source_atom,target_atom) )
        
    for i in atom_ids[half_number-1:-2]:
        
        source_atom = str(i+1)
        target_atom = str(i+2)
        f.write("%s %s %s %s \n" %(i,bond_type,source_atom,target_atom) )
        
    f.write("\n")
    
    f.write("Bond Coeffs \n \n")
    f.write("1 0.5 1.0 \n \n")
    
    f.write("Masses \n \n")
    f.write("1 1.0 \n2 1.0")
    
    f.close()
    
    print("Position file has been written.")
    
generate_pos()    
    