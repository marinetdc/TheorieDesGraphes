#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "31.10.19"
__usage__ = "Tests clients - vérification partielle"
__version__ = "0.1"
__update__ = "31.10.19"

"""
Outils de contrôle simplifié
> Vérifie si les méthodes/attributs demandés sont présents
> Vérifie qu'il n'y a aucune variable modifiable dans le code
"""

#-------------- import ----------------------#
import sys
import os
import copy
#============================================#

# fonctions de vérification
class Data:
    """ data collector for success/failure """
    def __init__(self):
        self.__yes = 0
        self.__no = 0
        self.__report = {}
        self.__subtests = []
        
    def ok(self): self.__yes += 1
    def nok(self): self.__no += 1
    def check(self, what:str): self.__subtests.append(what)
    def diagnostic(self, key:str, msg:str):
        _old = self.__report.get(key, "")
        self.__report[key] = _old + msg + '\n'
    @property
    def sum(self) -> int:
        return self.__yes + self.__no
    @property
    def report(self) -> str:
        _out = ""
        for key in self.__report:
            _out += ">>> '{}': {}".format(key, self.__report[key])
        return _out
    @property
    def subtests(self) -> tuple:
        return tuple(self.__subtests)
    @property
    def yes(self) -> int:
        return self.__yes
    @property
    def no(self) -> int:
        return self.__no

#===================== la propriété est-elle vérifiée =================#
def check_property(p:bool, msg:str='default', letter:str='E') -> str:
    """ 
        check if some property is True

        :param bolean p: property to verify
        :param str msg: message if failure
        :param char letter: the char if failure
        :return: letter or '.'
        :rtype: char

    """
    try:
        assert( p ), '>>> failure %s' % msg
        _ = '.'
    except Exception as _e:
        if sys.version_info[:2] >= (3, 3): print(_e, flush=True)
        else: print(_e)
        _ = letter
        
    return _

#====================== sz tests réussis ? =========================#
def has_failure(string:str, sz:int=1) -> bool:
    """ check if there are failures in the  last sz tests """
    sz = min(len(string), sz)
    return string[-sz:] != '.'*sz
    
#========================= attributs ro ? ===========================#
def subtest_readonly(obj:object, lattr:str) -> str:
    """ 
        check if all attributes are readonly

        :param obj: the instance to check
        :param lattr: the attributes to check
        :type lattr: can be str or any iterable
        :return: diagnostic message
        :rtype: str
    
        :note:
          try to modify the attribute with int, float, list, str
    """

    _s = '' ; _msg =''
    lattr = lattr.split() if isinstance(lattr, str) else lattr
    for att in lattr:
        _msg += "test attribut {}".format(att)
        try:
            oldv = copy.deepcopy(getattr(obj, att))
        except:
            continue

        try:
            _s += '.'
            setattr(obj, att, 421)
            if oldv != getattr(obj, att): _s += 'E'
        except Exception:
            _s += '.'
        if has_failure(_s, 2):
            _msg += '\n\tavant %s apres %s\n' % (oldv, getattr(obj, att))
            setattr(obj, att, oldv)

        try:
            _s += '.'
            setattr(obj, att, 42.24)
            if oldv != getattr(obj, att): _s += 'E'
        except Exception:
            _s += '.'
        if has_failure(_s, 2):
            _msg += '\n\tavant %s apres %s\n' % (oldv, getattr(obj, att))
            setattr(obj, att, oldv)
            
        try:
            _s += '.'
            setattr(obj, att, [-1, 0, 1, 'a'])
            if oldv != getattr(obj, att): _s += 'E'
        except Exception:
            _s += '.'
        if has_failure(_s, 2):
            _msg += '\n\tavant %s apres %s\n' % (oldv, getattr(obj, att))
            setattr(obj, att, oldv)
            
        try:
            _s += '.'
            setattr(obj, att, "gasp")
            if oldv != getattr(obj, att): _s += 'E'
        except Exception:
            _s += '.'
        if has_failure(_s, 2):
            _msg += '\n\tavant %s apres %s\n' % (oldv, getattr(obj, att))
            setattr(obj, att, oldv)
            
        _msg += _s+'\n'
        _s = ''
    return _msg

#=================== pas de variables publiques ni protégées ===============#
def check_validity(mymodule, klassname:str,
                   obj:any=None, lattr:list=[], zapit:list=None) -> tuple:
    """
        verify that there are no public nor protected attributes

        :param module mymodule: the module we are in
        :param str klassname: the class
        :param obj: an instance of klassname
        :type obj: None by default
        :param list lattr: the required attributes 
        :param zapit: name to ignore
        :type zapit: None or str
        :return: lenght and what are forbidden
        :rtype: tuple(int, set(str))

    """
    public = set([])
    protected = set([])
    private = set([])
    klass = getattr(mymodule, klassname)
    subKlass = None if zapit is None else getattr(mymodule, zapit)
    if obj is None:
        try:
            obj = klass()
        except:
            obj = klass
    allPref = []
    allPref.append('_'+klassname+'__')
    if zapit is not None: allPref.append('_'+zapit+'__')

    for x in dir(obj):
        #print("analyzing {} ... status ".format(x), end='')
        status = -1
        found = False
        if x.startswith('__'): status = 0 
        elif x in lattr: status = 1 
        elif x[0] == '_' and x[1].isalpha():
            for pref in allPref:
                if x.startswith(pref):
                    status = 3
                    private.add(x[len(pref):])
                    found = True
                    break
        else: status = 5 ; public.add(x)
        if not found and x in lattr: status = 4
        if status == -1: status = 2 ; protected.add(x)
        #print(status)

    for x in public.copy() :
        if hasattr(klass, x) and isinstance(getattr(klass, x), property):
            public.discard(x)
            continue
        if (zapit is not None and
            hasattr(subKlass, x) and
            isinstance(getattr(subKlass, x), property)):
            public.discard(x)
            continue
        
        try:
            if callable(getattr(obj, x)): public.discard(x)
        except AttributeError as _0:
            warnings.warn("Warning uninitialized attribute")
            print(_0)
            public.discard(x)
        except Exception as _e:
            print(_e)
            
    for x in protected.copy() :
        if hasattr(klass, x) and isinstance(getattr(klass, x), property):
            protected.discard(x)
            continue
        if (zapit is not None and
            hasattr(subKlass, x) and
            isinstance(getattr(subKlass, x), property)):
            protected.discard(x)
            continue
        try:
            if callable(getattr(obj, x)): public.discard(x)
        except AttributeError as _0:
            warnings.warn("Warning uninitialized attribute")
            print(_0)
            public.discard(x)
        except Exception as _e:
            print(_e)

    badV = set([])
    badV.update(protected, public)
    #print(badV)
    
    for val in badV.copy():
        _diagnostic = subtest_readonly(obj, val)
        if _diagnostic.count('E') - val.count('E') == 0: badV.discard(val)
    return len(badV), badV


def test_hasattr(klass:str, c:Data) -> str:
    """ contient la liste des attributs/méthodes attendus """
    latt = """
__init__ reset write_to read_from
nbVertices nbEdges dmin dmax edges weight
add_node add_edge 
del_nodes del_node
del_edges del_edge erase_edge
adj degre composante
estSimple estConnexe estComplet estEulerien estArbre
cconnexe minimal_subtree maximal_subtree minimisation maximisation
matrice_adjacence matrice_incidence
"""
    _out = ""
    _kl = getattr(dm, klass)
    for att in latt.split():
        if hasattr(_kl, att):
            c.check(att)
            c.ok()
            c.diagnostic(att, "exists")
        else:
            c.nok()
            c.diagnostic(att, "is missing")
        _out += '.'
    return _out

if __name__ == "__main__":
    if len(sys.argv) == 1:
        param = input("quel est le fichier à traiter ? ")
        if not os.path.isfile(param): ValueError("need a python file")
    else: param = sys.argv[1]

    etudiant = param.split('.')[0]

    out = check_property(etudiant != '','acces au fichier')
    print("tentative de lecture de {}".format(etudiant))
    try:
        dm = __import__(etudiant) # revient à faire import XXX as dm
    except Exception as _e:
        print(_e)
        sys.exit(-1)
        
    _todo = [] # les tests à réaliser

    for klass in "Reseau".split():
        out += check_property(hasattr(dm, klass),
                              "No class {} found".format(klass))
        if hasattr(dm, klass): _todo.append(klass)
    print(out)

    for klass in _todo:
        collect= Data()
        print(test_hasattr(klass, collect))
        badQte, badVal = check_validity(dm, klass, getattr(dm, klass)())
        if badQte > 0:
            _msg = "*** Classe {} ***\n".format(klass)
            _msg += ("Warning: Votre code contient {0} variable(s)"
                     " interdite(s)\n"
                     "=> Pénalité de 5*{0} points\n".format(badQte))
            _msg += ">>> {}\n".format(badVal)
            _msg += "="*17+"\n"
            collect.diagnostic(klass, _msg)

        print("="*13)
        print(collect.report)

        print("global {res.sum}, success {res.yes} fault {res.no}"
               "".format(res=collect), end=' ')
        if collect.sum != 0 :
            print("rate: {}%".format(round(100*collect.yes/collect.sum,2)))
        print("="*13)
        
