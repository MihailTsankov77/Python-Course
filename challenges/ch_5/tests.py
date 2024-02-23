from Ho_Ho_Ho import *
import unittest



class Ho_Ho_Ho_Tests(unittest.TestCase):

    def test_default(self):
        data = '''(3.14) Иван Иванов [10 г.]

 - Плейстейшан
 - Количка с дистанционо
 * Братче

(1.94)   Georgi "Jorkata" Georgiev  [43] 

 - Novo BMW (3-ka ili 5-ca)
 - 
  - Vancheto ot tretiq etaj

 - Pleistei6an'''


        self.assertEqual(parse_wishlist(data), [(3.14, 'Иван Иванов', 10, ('Плейстейшан', 'Количка с дистанционо', 'Братче')), (1.94, 'Georgi "Jorkata" Georgiev', 43, ('Novo BMW (3-ka ili 5-ca)', 'Vancheto ot tretiq etaj', 'Pleistei6an'))])
    

    def test_spacess(self):
        example = '''(    3.14    )        Иван Иванов         [10 г.]

 -        3453Плейстейшан               
 - Количка с дистанционо
 * Братче

(  -1.94)   Georgi "Jorkata" Georgiev  [43] 

 - Novo BMW (3-ka ili 5-ca)
 -   
 -
 -   
  - Vancheto ot tretiq etaj

 - Pleistei6an

 


(1.94  )   papa john  [  43       asdsafsdfsdfsa] 
 




 - adssadsads asddsads asdass 2331231 sasd!!!!
 -   


 -





 -   dsa

-                                           
  - B@@BS 

 - Pleistei6an
'''


        self.assertEqual(parse_wishlist(example), [(3.14, 'Иван Иванов', 10, ('3453Плейстейшан', 'Количка с дистанционо', 'Братче')), (-1.94, 'Georgi "Jorkata" Georgiev', 43, ('Novo BMW (3-ka ili 5-ca)', 'Vancheto ot tretiq etaj', 'Pleistei6an')), (1.94, 'papa john', 43, ('adssadsads asddsads asdass 2331231 sasd!!!!', 'dsa', 'B@@BS', 'Pleistei6an'))])

    def test_minuses(self):
        example = '''(    3.14    )        Иван Иванов         [10 г.]

 -        !3453Плейстейшан               
 - Количка с дистанционо
 * Братче

(1.94)   Georgi "Jorkata" Georgiev  [43] 

 - Novo BMW (3-ka ili 5-ca)
 -   
 -
 -   
  - Vancheto ot tretiq etaj

 - Pleistei6an

 


(    -1.94  )   papa john  [  43       asdsafsdfsdfsa] 
 




 - adssadsads asddsads asdass 2331231 sasd!!!!
 -   

                         - 
 - ---------------- -- - - wishing for sleep - - - ----------------
 -   dsa
-
-
-                                           
  - uuuuuuu B@@BS 

 - (Pleistei6an
'''


        self.assertEqual(parse_wishlist(example), [(3.14, 'Иван Иванов', 10, ('!3453Плейстейшан', 'Количка с дистанционо', 'Братче')), (1.94, 'Georgi "Jorkata" Georgiev', 43, ('Novo BMW (3-ka ili 5-ca)', 'Vancheto ot tretiq etaj', 'Pleistei6an')), (-1.94, 'papa john', 43, ('adssadsads asddsads asdass 2331231 sasd!!!!', '---------------- -- - - wishing for sleep - - - ----------------', 'dsa', 'uuuuuuu B@@BS', '(Pleistei6an'))])