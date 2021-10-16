#!/bin/bash

# Clears terminal for improved reading

clear

# Elimina os ficheiros antigos

echo "Deleting images/*"
rm -r images/*
echo "Deleting compiled/*"
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

echo ""

# i)
# A -> R
echo "Composing compiled/sources/A2R.fst"
# invert( R -> A ) = A -> R
fstinvert compiled/sources/R2A.fst > compiled/sources/A2R.fst

echo "Creating file: compiled/tests/A2R"
mkdir -p compiled/tests/A2R

# j)
# R/R/R -> dd/dd/dddd
echo "Composing compiled/sources/birthR2A.fst"
# compose( R -> A, d -> dd ) = R -> dd
fstcompose compiled/sources/R2A.fst compiled/sources/d2dd.fst > compiled/sources/R2dd.fst
# compose( R -> A, d -> dddd ) = R -> dddd
fstcompose compiled/sources/R2A.fst compiled/sources/d2dddd.fst > compiled/sources/R2dddd.fst

# concat( R -> dd, copy ) = R/ -> dd/
fstconcat  compiled/sources/R2dd.fst compiled/sources/copy.fst > compiled/sources/first.fst
# concat( R/ -> dd/, R2dd ) = R/R -> dd/dd
fstconcat  compiled/sources/first.fst compiled/sources/R2dd.fst > compiled/sources/second.fst
# concat( R/dd -> dd/dd, copy ) = R/R/ -> dd/dd/
fstconcat  compiled/sources/second.fst compiled/sources/copy.fst > compiled/sources/third.fst
# concat( R/dd/ -> dd/dd/, R2dddd ) = R/R/R -> dd/dd/dddd
fstconcat  compiled/sources/third.fst compiled/sources/R2dddd.fst > compiled/sources/birthR2A.fst

rm -r compiled/sources/R2dd.fst
rm -r compiled/sources/R2dddd.fst

echo "Creating file: compiled/tests/birthR2A"
mkdir -p compiled/tests/birthR2A

#k)
# para dd/mm/dddd -> dd/mmm/dddd
echo "Composing compiled/sources/birthA2T.fst"
# concat( copy, copy ) = dd
fstconcat compiled/sources/copy.fst compiled/sources/copy.fst > compiled/sources/first.fst
# concat( dd, copy ) = dd/
fstconcat compiled/sources/first.fst compiled/sources/copy.fst > compiled/sources/second.fst
# concat( dd/, mm2mmm ) = dd/mmm
fstconcat compiled/sources/second.fst compiled/sources/mm2mmm.fst > compiled/sources/third.fst
# concat( dd/mmm, copy ) = dd/mmm/
fstconcat compiled/sources/third.fst compiled/sources/copy.fst > compiled/sources/fourth.fst
# concat( dd/mmm/, copy ) = dd/mmm/d
fstconcat compiled/sources/fourth.fst compiled/sources/copy.fst > compiled/sources/fifth.fst
# concat( dd/mmm/d, copy ) = dd/mmm/dd
fstconcat compiled/sources/fifth.fst compiled/sources/copy.fst > compiled/sources/sixth.fst
# concat( dd/mmm/dd, copy ) = dd/mmm/ddd
fstconcat compiled/sources/sixth.fst compiled/sources/copy.fst > compiled/sources/seventh.fst
# concat( dd/mmm/ddd, copy ) = dd/mmm/dddd
fstconcat compiled/sources/seventh.fst compiled/sources/copy.fst > compiled/sources/birthA2T.fst

rm -r compiled/sources/first.fst
rm -r compiled/sources/second.fst
rm -r compiled/sources/third.fst

echo "Creating file: compiled/tests/birthA2T"
mkdir -p compiled/tests/birthA2T

#l)
echo "Composing compiled/sources/sources/birthT2R.fst"
fstcompose compiled/sources/birthR2A.fst compiled/sources/birthA2T.fst > compiled/sources/birthR2T.fst

fstinvert compiled/sources/birthR2T.fst > compiled/sources/birthT2R.fst

echo "Creating file: compiled/tests/birthT2R"
mkdir -p compiled/tests/birthT2R

#m)
echo "Composing compiled/sources/sources/birthR2L.fst"
fstcompose compiled/sources/birthR2A.fst compiled/sources/date2year.fst > compiled/sources/a.fst
fstcompose compiled/sources/a.fst compiled/sources/leap.fst > compiled/sources/birthR2L.fst

rm -r compiled/sources/a.fst

echo "Creating file: compiled/tests/birthR2L"
mkdir -p compiled/tests/birthR2L


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
