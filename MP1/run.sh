#!/bin/bash

# Cria pastas necessarias, caso ausentes

mkdir -p compiled images compiled/tests compiled/sources compiled/composed


# Compila todos os transducers contidos na pasta sources
# Cria uma pasta para os testes compilados do transducer

for transducer in sources/*.txt; do
	echo "Compiling: $transducer; Creating file: compiled/tests/$(basename $transducer ".txt")"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $transducer | fstarcsort > compiled/sources/$(basename $transducer ".txt").fst
    mkdir -p compiled/tests/$(basename $transducer ".txt")
done

# Compila todos os transducers contidos na pasta testes
# Todos os ficheiros tests tem que ser o nome do transducerXX, XX sao numeros

for transducer in tests/*.txt; do
	echo "Compiling: $transducer and storing it in compiled/${transducer::-6}/$(basename $transducer ".txt").fst"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $transducer | fstarcsort > compiled/${transducer::-6}/$(basename $transducer ".txt").fst
done

# Cria um transducer composed para verificar os inputs

for source in compiled/sources/*.fst; do
    for teste in compiled/tests/$(basename $source ".fst")/*fst; do
        echo "Testing the transducer $(basename $source) with the input $(basename $teste) (generating pdf)"
        fstcompose $teste $source | fstshortestpath > compiled/composed/$(basename $teste ".fst")R.fst
        fstcompose $teste $source | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
    done
done

# Cria a imagem em pdf dos transducers source e composed compilados

for transducer in compiled/sources/*.fst compiled/composed/*.fst; do
	echo "Creating image from transducer $transducer"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $transducer | dot -Tpdf > images/$(basename $transducer '.fst').pdf
done

# Cria a imagem em pdf dos transducers test compilados

for pastaDeTestes in compiled/tests/*; do
    for teste in $pastaDeTestes/*.fst; do
        echo "Creating image from transducer: $teste"
        fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $teste | dot -Tpdf > images/$(basename $teste '.fst').pdf
    done
done
