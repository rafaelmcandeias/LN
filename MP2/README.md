## INFO DO PROJETO
- Treinar com trainWithoutDev -> Testar com o dev
- Os testes seguem o formato LABEL^IQUESTION^IANSWER

- A prof depois liberta test pra a avaliação
- Segue o formato QUESTION^IANSWER

- Os modelos devem devolver um ficehiro txt com a categoria de cada linha

- Submeter com um dev_results.txt -> corresponde aos resultados do nosso melhor modelo quando testado com o dev.txt
- Mais tarde, submeter com um test_results.txt -> melhor modelo com test.txt -> dado pela prof

- Vao correr assim : python qc.py –test NAMEOFTESTFILE –train NAMEOFTHETRAINFILE > results.txt

## IDEIAS PARA A RESOLUÇÃO

- Semi-generalizar + semi-casos individuais
- Há erros nos ficheiros. ex: 1ª linha do train tem " erradas
- Algumas respostas no training set tb nao fazem sentido...

#### Model1:
- Pre-processing, ter cuidado com stomp words

#### Model2:
- Pre-processing, ter cuidado com stomp words

#### qc:
- Recebe o txt treino com -train e txt teste com -test
- Aplica os 
- Avalia Model1 e Model2

#### Avaliação:
- F-measure (Contador de TP, FP, FN e beta=1)
    - Usar grep e wc -l no final para realizar as contas. comandos de maquina sao os mais otimizados
    - 
- MRR não!
    - O MRR é utilizado quando o sistema devolve varias possibilidades,
    - O nosso seleciona uma só categoria. A mais provavel

