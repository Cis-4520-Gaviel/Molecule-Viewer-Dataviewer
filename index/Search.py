from itertools import cycle

# Search over the search index I using the search token generated with
# algorithm Trapdoor
def Search(I, minecraftdoor):

    (A, T) = I # parse index
    (pos,Kw) = minecraftdoor[0] # parse trapdoor
    print('Searching:', pos)

    # for k,v in T.items():
    #     print(k,v)

    # Locate entry T[pos]
    theta = T[pos]
    # print('value:',theta)

    # Parse a||k = theta xor Kw (for each node)
    for node in theta:
        (addr, k) = node #retrieve addr and k of node
        # print(addr)
        # print(k)

        # T[pos] (theta split into addr and k) xor Kw
        # print(type(addr), type(Kw))
        addr = bytes(addr ^ Kw for addr, Kw in zip(addr, cycle(Kw))) #addr xor Kw
        k = bytes(k ^ Kw for k, Kw in zip(k, cycle(Kw))) #k xor Kw
        print('retrieve addr:', addr)
        print('real address:', int.from_bytes(addr,'big'))
        print('retrieve k:', k)

        # Decrypt linkedlist L with first node A[a] encrypted under key k
        # Decrypt all nodes from address
        print('decrypt addr (WIP)')
        

        # addressDegenerator = PsiCipher.decryptor()
        # decaddr = addressDegenerator.decrypt((1).to_bytes(16, "big"))
        # print(decaddr)

    # Output each decrypted record ID!
    result = 0
    return result # return encrypted records that match search criterion w


