#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 10:39:38 2017

Testing out writing text files, plan to use this approach to generate .pos
files for LAMMPS

@author: as14014
"""

from datetime import datetime
import numpy as np

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
    
    

def write_atom_chain(f,starting_id,number_of_atoms,spacing,y_coord,z_coord,vacuum_gap_multiplier):#must use inside another func, f is undefined
    
    
    ids = range(starting_id,starting_id+number_of_atoms)
    x_multiples = np.arange(number_of_atoms)
    half_row_number = int(number_of_atoms / 2)
    y_coord_str = str(y_coord)
    z_coord_str = str(z_coord)
    
    for i,j in zip(ids,x_multiples):
        
        id = str(i)
        x_position = str( j*spacing )
        yz_string = str("    %s    %s" %(y_coord_str,z_coord_str) )
        
        if i <= ids[half_row_number-1]:
            
            atom_type = str(1)
            molecule_type = str(1)
            f.write("%s %s %s %s %s \n" %(id,molecule_type,atom_type,x_position,yz_string))
                  
        else:
            atom_type = str(2)
            molecule_type = str(2)
            x_position = str ( (j-1)*spacing + vacuum_gap_multiplier*spacing )
            f.write("%s %s %s %s %s \n" %(id,molecule_type,atom_type,x_position,yz_string))   



def generate_2D_pos(name=datetime.now().strftime('%d-%m_%H.%M')+"_2D.pos",wall_gap_multiplier=3,\
                 row_atoms=16,rows=4,atomic_spacing=0.45,vacuum_gap_multiplier=3):
    atoms = int(row_atoms*rows) 
    total_bonds =  int(rows*(2*row_atoms -2) - row_atoms)
    spacing = atomic_spacing
    vacuum_gap = vacuum_gap_multiplier * spacing
    x_lo = str(-1*wall_gap_multiplier*spacing)
    x_hi = str( (row_atoms - 1)*spacing + vacuum_gap + wall_gap_multiplier*spacing )
    y_lo = str( -1*wall_gap_multiplier*spacing)
    y_hi = str( (rows-1)*spacing + wall_gap_multiplier*spacing )
    z_lo = str( -0.9*spacing)
    z_hi = str( 0.1*spacing)
    
    f = open(file=name,mode='x')
    
    f.write(str(row_atoms)+"x%sx1 (001) layers of simple cubic lattice \n \n" %(str(rows)) )
    f.write(str(atoms)+" atoms \n"+str(total_bonds)+" bonds \n \n")
    
    f.write("2 atom types \n1 bond types \n \n")
    
    f.write(x_lo+" "+x_hi+" xlo xhi \n")
    f.write(y_lo+" "+y_hi+" ylo yhi \n")
    f.write(z_lo+" "+z_hi+" zlo zhi \n \n")

    f.write("Atoms \n \n")
    
    atom_ids = range(1,atoms+1)
    starting_ids_y_coords = zip(  atom_ids[::row_atoms], np.arange(rows) )
    
    for i,j in starting_ids_y_coords:
        
        write_atom_chain(f,i,row_atoms,atomic_spacing,j*atomic_spacing,0.00000,vacuum_gap_multiplier)
        
        
        
    f.write("\n")
    f.write("Bonds \n \n")

    
    bond_type = "1"
    half_number = int(row_atoms /2) 
    no_bond_ids = []
    for i in atom_ids:
        no_bond_ids.append(i)
    del no_bond_ids[half_number-1::half_number]
    #no_bond_ids = no_bond_ids[:-1]
    
    counter = 1
    for i in no_bond_ids: #this adds horizontal bonds
        
        source_atom = str(i)
        target_atom = str(i+1)
        f.write("%s %s %s %s \n" %(i,bond_type,source_atom,target_atom) )
        counter +=1
    
    first_vertical_id = no_bond_ids[-1]+1
    first_source = 1
    first_target = first_source + row_atoms
    while counter <= total_bonds: #this adds vertical bonds
        counter +=1
        f.write("%s %s %s %s \n" %(first_vertical_id,bond_type,first_source,first_target))
        first_vertical_id +=1
        first_source += 1
        first_target += 1
        

        
    f.write("\n")
    
    f.write("Bond Coeffs \n \n")
    f.write("1 0.5 1.0 \n \n")
    
    f.write("Masses \n \n")
    f.write("1 1.0 \n2 1.0")
    
    f.close()
    
    print("Position file has been written.")
    
generate_2D_pos(row_atoms=50,rows=25,atomic_spacing=4.5,vacuum_gap_multiplier=(10/4.5))    
    