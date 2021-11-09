## INFO DO PROJETO
- Treinar com trainWithoutDev -> Testar com o dev
- Os testes seguem o formato LABEL^IQUESTION^IANSWER

- A prof depois liberta test pra a avaliação
- Segue o formato QUESTION^IANSWER

- Os modelos devem devolver um ficehiro txt com a categoria de cada linha

- Submeter com um dev_results.txt -> corresponde aos resultados do nosso melhor modelo quando testado com o dev.txt
- Mais tarde, submeter com um test_results.txt -> melhor modelo com test.txt -> dado pela prof

- Vao correr assim : python qc.py –test NAMEOFTESTFILE –train NAMEOFTHETRAINFILE > results.txt


#### Model1:

- Pre-processing:
    - For baseline it's enough having stemmatization, since , not complex
    - Porter-Stemmer for stemmatization. nltk lib has it implemented. 
        ACC: 0.694  TEMP: 38.389s

- Main algorithm:
    - Com Jaccard(Q1, Q2) + Jaccard(R1, R2)
        ACC: 0.694 TEMP: 38.389s
    - Com Jaccard(Q1 + R1, Q2 + R2)
        ACC: 0.588 TEMP: 52.036 


#### Model2:

- Pre-processing:
    - Removing stop-words, such as __, ", The, ..., etc.. and many more
    - Porter-Stemmer mais comum, n faz mt 
        ACC: 0.842 TEMP: 28.467s
    - EXP: LancasterStemmer is simple, but heavy stemming due to iterations and over-stemming may occur. Over-stemming causes the stems to be not linguistic, or they may have no meaning. -> reduzir mt a palavra pode anular diferenças
        ACC: 0. TEMP: 
    - EXP: Snowball, melhor que porter e mais rapido
        ACC: 0. TEMP:  

- Main algorithm:
    - Naive Bayes is very fast and requires low storage.
        ACC: 0.842 TEMP: 28.467s
    - EXP: SVM is better since we have tons of data and it pays attention for interactions between words, but requires data as int.
        ACC: 0. TEMP: 
    - EXP: Tf-idf uses several documents, which we lack on 
        ACC: 0. TEMP: 


#### qc:
- Recebe o txt treino com -train e txt teste com -test
- Treina o modelo em teste
- Cria um ficheiro results com a resposta do modelo em teste


#### NOS:
- Correr a shell pra executar o projeto e calcular a percentagem

