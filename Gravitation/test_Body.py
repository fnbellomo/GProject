#!/usr/bin/env python3 

import unittest
import doctest
from Body import Body
from Gravitation import Gravitation
from Plot import make_plot 

class TestProject(unittest.TestCase):
    """ Testing Body.py"""
    # Give the id, mass, distance and velocity to the Body
 
    def test_constructor1(self):
        b = Body("A",-2,[3,2],[1.0,-1.0])
        self.assertEqual(b.obj_id,"A")
        # we have to protect the value of the mass from  negative or zero
        # In this case the mass is negative 
        self.assertEqual(b.obj_mass,-2)
        self.assertEqual(b.obj_position,[3,2] ) 
        self.assertEqual(b.obj_velocity, [1.0,-1.0])


    def test_constructor2(self):
        b = Body("B",3.0,[-1.0,0],[-1.0,1])
        self.assertEqual(b.obj_id,"B")
        self.assertEqual(b.obj_mass,3.0)
        self.assertEqual(b.obj_position, [-1.0,0])
        self.assertEqual(b.obj_velocity, [-1.0,1])

    def test_output1(self):
        b = Body("A",2.0,[3.0,5],[-1.0,3])
        b.obj_position = [3.0,5]
        self.assertEqual(str(b.obj_position),'[3.0, 5]')

#    def test_assert1(self):
#        with self.assertRaises(ValueError):
#          Body("x",2.0,[1,2],[2,3])
       # have to catch the exception

    def test_gfactor(self):
        b1 = Body("A",4.0,[1,1],[1,1]) 
        b2 = Body("B",4.0,[2,1],[2,1])
        res =Body.gfactor(b1,b2)
        self.assertEqual(res, 0.1496152) 

    """ Testing Gravitation.py """
    # You have to give the mass, distance and radius 
    # to the class Graviton

    def test_constructor3(self):
        g1 = Gravitation(6e12,3e25,9.6e7)
        self.assertEqual(g1.convert_m,40 )
        self.assertEqual(g1.convert_r,5.02209722780233)
        self.assertEqual(g1.convert_t,3.0864197530864197)

    def test_add_body(self):
        g2 = Gravitation(6e12,3e25,9.6e7)
        a2 = Gravitation.add_body(g2,"A",1,[3,2],[1.0,-1.0])              

    """ Testing Plot.py"""
#    def test_constructor4(self):
#        g3 = Gravitation(6e12,3e25,9.6e7)
#        g3.add_body("B",2,[5,2],[6.0,-1.0])       
#	m = make_plot(g3)
   



if __name__ == '__main__':
    doctest.testmod()
    unittest.main()
