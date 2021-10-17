#!/bin/bash

# Clears terminal for improved reading

clear

# Elimina os ficheiros antigos

echo "Deleting images/*"
rm -r images/*
echo "Deleting compiled/*"
rm -r compiled/*

# Cria pastas necessarias

mkdir -p compiled images

# Converting all files from dos to unix

for file in sources/*.txt tests/*.txt; do
    dos2unix -q $file
done

# New line for cleaner reading

echo ""

# Compila todos os transducers contidos na pasta sources

for transducer in sources/*.txt; do
	echo "Compiling $transducer into compiled/$(basename $transducer ".txt").fst"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $transducer | fstarcsort > compiled/$(basename $transducer ".txt").fst
done

# Cria os transducers do exercicio 2

echo ""

# i)
# A -> R
echo "Composing compiled/A2R.fst"
# invert( R -> A ) = A -> R
fstinvert compiled/R2A.fst > compiled/A2R.fst

# j)
# R/R/R -> dd/dd/dddd
echo "Composing compiled/birthR2A.fst"
# compose( R -> A, d -> dd ) = R -> dd
fstcompose compiled/R2A.fst compiled/d2dd.fst > compiled/R2dd.fst
# compose( R -> A, d -> dddd ) = R -> dddd
fstcompose compiled/R2A.fst compiled/d2dddd.fst > compiled/R2dddd.fst

# concat( R -> dd, copy ) = R/ -> dd/
fstconcat  compiled/R2dd.fst compiled/copy.fst > compiled/first.fst
# concat( R/ -> dd/, R2dd ) = R/R -> dd/dd
fstconcat  compiled/first.fst compiled/R2dd.fst > compiled/second.fst
# concat( R/dd -> dd/dd, copy ) = R/R/ -> dd/dd/
fstconcat  compiled/second.fst compiled/copy.fst > compiled/third.fst
# concat( R/dd/ -> dd/dd/, R2dddd ) = R/R/R -> dd/dd/dddd
fstconcat  compiled/third.fst compiled/R2dddd.fst > compiled/birthR2A.fst

rm -r compiled/R2dd.fst
rm -r compiled/R2dddd.fst

#k)
# para dd/mm/dddd -> dd/mmm/dddd
echo "Composing compiled/birthA2T.fst"
# concat( copy, copy ) = dd
fstconcat compiled/copy.fst compiled/copy.fst > compiled/first.fst
# concat( dd, copy ) = dd/
fstconcat compiled/first.fst compiled/copy.fst > compiled/second.fst
# concat( dd/, mm2mmm ) = dd/mmm
fstconcat compiled/second.fst compiled/mm2mmm.fst > compiled/third.fst
# concat( dd/mmm, copy ) = dd/mmm/
fstconcat compiled/third.fst compiled/copy.fst > compiled/fourth.fst
# concat( dd/mmm/, copy ) = dd/mmm/d
fstconcat compiled/fourth.fst compiled/copy.fst > compiled/fifth.fst
# concat( dd/mmm/d, copy ) = dd/mmm/dd
fstconcat compiled/fifth.fst compiled/copy.fst > compiled/sixth.fst
# concat( dd/mmm/dd, copy ) = dd/mmm/ddd
fstconcat compiled/sixth.fst compiled/copy.fst > compiled/seventh.fst
# concat( dd/mmm/ddd, copy ) = dd/mmm/dddd
fstconcat compiled/seventh.fst compiled/copy.fst > compiled/birthA2T.fst

rm -r compiled/first.fst
rm -r compiled/second.fst
rm -r compiled/third.fst
rm -r compiled/fourth.fst
rm -r compiled/fifth.fst
rm -r compiled/sixth.fst
rm -r compiled/seventh.fst

#l)
# T -> R
echo "Composing compiled/birthT2R.fst"
# compose( R -> A, A -> T ) = R -> T
fstcompose compiled/birthR2A.fst compiled/birthA2T.fst > compiled/birthR2T.fst

#invert( R -> T ) = T -> R
fstinvert compiled/birthR2T.fst > compiled/birthT2R.fst

rm -r compiled/birthR2T.fst

#m)
echo "Composing compiled/birthR2L.fst"
fstcompose compiled/birthR2A.fst compiled/date2year.fst > compiled/a.fst
fstcompose compiled/a.fst compiled/leap.fst > compiled/birthR2L.fst

rm -r compiled/a.fst

# New line for cleaner reading

echo ""

# Compila todos os transducers contidos na pasta testes
# Todos os ficheiros tests tem que ser o nome do transducerXX, XX sao numeros

for test in tests/*.txt; do
	echo "Compiling: $test into compiled/$(basename $test ".txt").fst"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $test | fstarcsort > compiled/$(basename $test ".txt").fst
done

# New line for cleaner reading

echo ""

# Cria um transducer composed para verificar os inputs

for source in sources/*.txt; do
    sourceNoPrefix=${source#*/}
    sourceName=${sourceNoPrefix%.*}
    for compiled in compiled/*.fst; do
        compiledNoPrefix=${compiled#*/}
        compiledName=${compiledNoPrefix::-6}
        if [ $sourceName = $compiledName ]
        then
            echo "Composing the transducer $(basename $source ".txt").fst with the input $(basename $compiled)"
            fstcompose $compiled compiled/$(basename $source ".txt").fst | fstshortestpath > compiled$(basename $teste ".fst")R.fst
            echo "(stdout) do composed"
            fstcompose $compiled compiled/$(basename $source ".txt").fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
        fi
    done
done

# New line for cleaner reading

echo ""

# Cria pdf dos transducers source e composed compilados

for transducer in compiled/*.fst; do
	echo "Creating image from transducer $(basename $transducer) (generating pdf)"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $transducer | dot -Tpdf > images/$(basename $transducer '.fst').pdf
done

# New line for cleaner reading

echo ""