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
    - Porter-Stemmer for stemmatization. nltk lib has it implemented.
    - LancasterStemmer is simple, but heavy stemming due to iterations and over-stemming may occur. Over-stemming causes the stems to be not linguistic, or they may have no meaning.
- Main algorithm:
    - Com Jaccard calcula a distancia da palavra à soluçao + treshold para respostas

#### Model2:
- Pre-processing:
    - Porter-Stemmer. 
    - LancasterStemmer is simple, but heavy stemming due to iterations and over-stemming may occur. Over-stemming causes the stems to be not linguistic, or they may have no meaning.
    - Removing stop-words, such as __, ", The, ..., etc.. and many more
- Main algorithm:
    - Naive Bayes is very fast and requires low storage.
    - SVM is better since we have tons of data and it pays attention for interactions between words, but requires data as int. 
    - Tf-idf uses several documents, which we lack on 

#### qc:
- Recebe o txt treino com -train e txt teste com -test
- Treina o modelo em teste
- Cria um ficheiro results com a resposta do modelo em teste

#### NOS:
- Correr a shell pra executar o projeto e calcular a percentagem

