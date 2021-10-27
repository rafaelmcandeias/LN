--------------INFO DO PROJ------------------------
- Treinar com trainWithoutDev -> Testar com o dev
- Os testes seguem o formato LABEL^IQUESTION^IANSWER

- A prof depois liberta test pra a avaliação
- segue o formato QUESTION^IANSWER

- Os modelos devem devolver um ficehiro txt com a categoria de cada linha

- Submeter com um dev_results.txt -> corresponde aos resultados do nosso melhor modelo quando testado com o dev.txt
- Mais tarde, submeter com um test_results.txt -> melhor modelo com test.txt -> dado pela prof

- vao correr assim : python qc.py –test NAMEOFTESTFILE –train NAMEOFTHETRAINFILE > results.txt

--------------IDEIAS PRA RESOLUÇÃO------------------------

- semi-generalizar + semi-casos individuais
- Há erros nos ficheiros. ex: 1ª linha do train tem " erradas
- ALgumas respostas no training set tb nao fazem sentido...

Model1:
- Pre-processing, ter cuidado com stomp words

Model2:
- Pre-processing, ter cuidado com stomp words

qc:

Avaliação:
- F-measure (Contador de TP, FP, FN e beta=1)
    - usar grep e wc -l no final para realizar as contas. comandos de maquina sao os mais otimizados
- MRR não?
    - o MRR é utilizado quando o sistema devolve varias possibilidades,
    - o nosso seleciona uma só categoria. A mais provavel

