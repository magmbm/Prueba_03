def get_generos(genre):
    generos= ''
    cont= 0
    for i in range(0, len(genre)):
        if cont> 0:
            generos+= ', '

        generos+= genre[i].get('name')
        cont+= 1
    return generos