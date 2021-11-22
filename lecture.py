#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def read_validate(fname:str="",
                  vmin:int=-10, vmax:int=10, default:int=1) -> list:
    """
    read in a file
    input filename to read
    # starts a comment, ignored
    1st line cardV cardE dmin dmax
    others
    src goal [weight]
    if src > goal : ignore
    if src or goal not in 1..cardV ignore
    if weight missing 'default'
    if weight not in 'vmin' .. 'vmax': set 'default'
    if multiple edges with same weight: ignore but the 1st
    if after reading cardV or cardE or dmin or dmax is wrong: return []
    else [(src, goal, weight) ...]
    """

    if not os.path.isfile(fname): return []
    with open(fname, 'r') as f:
        lines = f.readlines()
        f.close()
    _flag = True
    _, _err = 0, 0
    _sol = set()
    for line in lines:
        # correction on the fly for each line
        try:
            if line.startswith('#') or len(line.strip()) == 0: continue
            _l = [x.strip() for x in line.split('#')[0].split()]
            if _flag:
                _params = [int(x) for x in _l]
                if len(_params) != 4:
                    print("missing values", _params)
                    return []
                # dmin <= dmax
                if _params[2] > _params[3]:
                    print("dmin={0[2]} > dmax={0[3]}".format(_params))
                    return []
                # dmin * carV <= 2 cardE <= dmax * cardV
                _m = _params[0]*_params[2] - 2*_params[1]
                if  _m > 0:
                    print("missing {} edges".format(_m))
                    return []
                _m = 2*_params[1] - _params[0]*_params[3] 
                if _m > 0:
                    print("exceeding {} edges".format(_m))
                    return []
                # basic checks are fine
                _flag = False
            else:
                src, goal = [int(_l[i]) for i in range(2)]
                if src not in range(1, _params[0]+1):
                    raise ValueError("vertex {} out of range".format(src))
                if goal not in range(1, _params[0]+1):
                    raise ValueError("vertex {} out of range".format(goal))
                if src > goal: raise ValueError("{} > {}".format(src, goal))
                weight = default if len(_l) == 2 else int(_l[2])
                weight = weight if vmin <= weight <= vmax else default
                _sol.add((src, goal, weight))
        except Exception as _e:
            _err += 1
            print("E{:02d}, msg >>".format(_err), _e)
            print("L{:02d} >> '{}'".format(_, ', '.join(_l)))
        finally:
            _ += 1

    # final check and decision
    _deg = [ 0 for x in range(_params[0]) ]
    _nbE = len(_sol)
    for x,y,_ in _sol: _deg[x-1]+=1 ; _deg[y-1]+=1
    _dmin, _dmax = min(_deg), max(_deg)
    if _nbE != _params[1]:
        print("expected {}, found {} edges".format(_params[1], _nbE))
        return []
    if _dmin != _params[2]:
        print("wrong dmin, expected {}, found {}".format(_params[2], _dmin))
        return []
    if _dmax != _params[3]:
        print("wrong dmax, expected {}, found {}".format(_params[3], _dmax))
        return []
    return list(_sol)

if __name__ == "__main__":
    _d={1:"good_file.txt",
        2:"bad_file.txt",
        3:"soso_file.txt"}

    print("""Pour tester la lecture choisissez

1/ fichier sans erreur
2/ fichier plein d'erreurs
3/ fichier avec quelques erreurs

""")
    try:
        choix = int(input("votre choix ? "))
        print("votre choix est {}".format(_d[choix]))
        print("Le résultat du traitement renvoie\n\t {}"
              .format(read_validate(_d[choix])))
    except Exception as _e:
        print(_e)
