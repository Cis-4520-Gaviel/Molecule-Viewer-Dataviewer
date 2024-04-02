

from pypbc import Parameters, Pairing, Element, G1, G2, GT, Zr
from inspect import signature
print()

import pymcl



"""
Functions available
['Element', 'G1', 'G2', 'GT', 'PBC_EC_Compressed',
 'Pairing', 'Parameters', 'Zr', '__doc__', '__file__',
 '__loader__', '__name__', '__package__', '__spec__',
 'get_random', 'get_random_prime', 'set_point_format_compressed',
 'set_point_format_uncompressed']
"""
"""
Element - Class
Pairing - Class
Parameters - Class
Zr - int??
get_random_prime - Function, parameters : int (most likely the no.of bits)
set_point_format_compressed - Function, parameters : None
set_point_format_uncompressed - Function, parameters : None
"""



def setup(k):

    # Initialize a set of parameters from a string 
    # check the PBC documentation (http://crypto.stanford.edu/pbc/manual/) for more information

# Initialize a set of parameters from a string 
# check the PBC documentation (http://crypto.stanford.edu/pbc/manual/) for more information
    params = Parameters(
        "type a\n",
        "q 8780710799663312522437781984754049815806883199414208211028653399266475630880222957078625179422662221423155858769582317459277713367317481324925129998224791\n",
        "h 12016012264891146079388821366740534204802954401251311822919615131047207289359704531102844802183906537786776\n",
        "r 730750818665451621361119245571504901405976559617\n",
        "exp2 159\n",
        "exp1 107\n",
        "sign1 1\n",
        "sign0 1\n",
    )

    # Initialize the pairing
    pairing = Pairing(params)

    # show the order of the pairing
    print(pairing.order())

    # Generate random elements
    g1 = Element.random(pairing, G1)
    g2 = Element.random(pairing, G2)
    z1 = Element.random(pairing, Zr)
    z2 = Element.random(pairing, Zr)

# Check the properties of the pairing
    assert pairing.apply(g1 ** z1, g2 ** z2) == pairing.apply(g1, g2) ** (z1 * z2)

def test_bls():
    stored_params = """type a
    q 8780710799663312522437781984754049815806883199414208211028653399266475630880222957078625179422662221423155858769582317459277713367317481324925129998224791
    h 12016012264891146079388821366740534204802954401251311822919615131047207289359704531102844802183906537786776
    r 730750818665451621361119245571504901405976559617
    exp2 159
    exp1 107
    sign1 1
    sign0 1
    """

    # this is a test for the BLS short signature system
    params = Parameters(stored_params)
    pairing = Pairing(params)

    # build the common parameter g
    g = Element.random(pairing, G2)
    # print("g =", g)

    # build the public and private keys
    private_key = Element.random(pairing, Zr)
    public_key = Element(pairing, G2, value=g**private_key)
    print("public_key =", public_key)
    print("private_key =", private_key)

    # # set the magic hash value
    hash_value = Element.from_hash(pairing, G1, "message")
    print("hash_value =", hash_value)

    # # create the signature
    # signature = hash_value**private_key

    # # build the temps
    # temp1 = Element(pairing, GT)
    # temp2 = Element(pairing, GT) 

    # # fill temp1
    # temp1 = pairing.apply(signature, g)

    # #fill temp2
    # temp2 = pairing.apply(hash_value, public_key)

    # # and again...
    # temp1 = pairing.apply(signature, g)

    # # compare
    # self.assertEqual(temp1 == temp2, True)

    # # compare to random signature
    # rnd = Element.random(pairing, G1)
    # temp1 = pairing.apply(rnd, g)

    # # compare
    # self.assertEqual(temp1 == temp2, False)

def main():
    g1 = pymcl.g1 # generator of G1
    g2 = pymcl.g2 # generator of G2
    x1 = pymcl.Fr.random() # random element in Fr
    x2 = pymcl.Fr.random() # random element in Fr

# check the correctness of the pairing
    assert pymcl.pairing(g1 * x1, g2 * x2) == pymcl.pairing(g1, g2) ** (x1 * x2)
    print(pymcl.pairing(g1 * x1, g2 * x2))
    # setup(4)
    # test_bls()

def TestAuthorizationSystem():
    frTest = pymcl.Fr('4956860243094490671591998352430815023460385533631324063655048520527491662930')
    x1 = frTest.random()
    g1 = pymcl.g1
    g2 = pymcl.g2

    keyword = g1.hash(bytes("test", 'utf-8'))
    searchQuery = g1.hash(bytes("test", 'utf-8'))

    writerSecretKey = pymcl.Fr.random()
    privateKey = pymcl.Fr.random()
    public = g2 * ~privateKey

    authorization = public * writerSecretKey
    indexHash = pymcl.pairing(keyword, g2 * writerSecretKey)

    transformation = pymcl.pairing(searchQuery * privateKey, authorization)
    print(indexHash,"\n\n", transformation)
    print("Keys Match: ",indexHash == transformation)
    

    # print(dir(pymcl.r))

if __name__ == '__main__':
    # main()
    TestAuthorizationSystem()