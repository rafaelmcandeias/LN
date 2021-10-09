#!/bin/bash

# Clears terminal for improved reading

clear

# Elimina os ficheiros antigos

rm -r images/*
rm -r compiled/*

# Cria pastas necessarias

mkdir -p compiled images compiled/tests compiled/sources compiled/composed


# Converting all files from dos to unix

for file in sources/*.txt tests/*.txt; do
    dos2unix -q $file
done

# New line for cleaner reading

echo ""

# Compila todos os transducers contidos na pasta sources
# Cria uma pasta para os testes compilados do transducer

for transducer in sources/*.txt; do
	echo "Compiling $transducer into compiled/sources/$(basename $transducer ".txt").fst"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $transducer | fstarcsort > compiled/sources/$(basename $transducer ".txt").fst
    echo "Creating file: compiled/tests/$(basename $transducer ".txt")"
    mkdir -p compiled/tests/$(basename $transducer ".txt")
done

# Cria os transducers do exercicio 2

# i)
fstinvert compiled/sources/R2A.fst > compiled/sources/A2R.fst
echo "Creating file: compiled/tests/A2R"
mkdir -p compiled/tests/A2R

# New line for cleaner reading

echo ""

# Compila todos os transducers contidos na pasta testes
# Todos os ficheiros tests tem que ser o nome do transducerXX, XX sao numeros

for test in tests/*.txt; do
	echo "Compiling: $test into compiled/${test::-6}/$(basename $test ".txt").fst"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $test | fstarcsort > compiled/${test::-6}/$(basename $test ".txt").fst
done

# New line for cleaner reading

echo ""

# Cria um transducer composed para verificar os inputs

for source in compiled/sources/*.fst; do
    for teste in compiled/tests/$(basename $source ".fst")/*.fst; do
        echo "Composing the transducer $(basename $source) with the input $(basename $teste)"
        fstcompose $teste $source | fstshortestpath > compiled/composed/$(basename $teste ".fst")R.fst
        echo "(stdout) do composed"
        fstcompose $teste $source | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
    done
done

# New line for cleaner reading

echo ""

# Cria pdf dos transducers source e composed compilados

for transducer in compiled/sources/*.fst compiled/composed/*.fst; do
	echo "Creating image from transducer $transducer (generating pdf)"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $transducer | dot -Tpdf > images/$(basename $transducer '.fst').pdf
done

# New line for cleaner reading

echo ""

# Cria pdf dos transducers test compilados

for pastaDeTestes in compiled/tests/*; do
    for teste in $pastaDeTestes/*.fst; do
        echo "Creating image from transducer: $teste (generating pdf)"
        fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $teste | dot -Tpdf > images/$(basename $teste '.fst').pdf
    done
done
