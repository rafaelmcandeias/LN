
###### Relatório do 2º mini projeto de Língua Natural
- Rafael Candeias, 93748
- Vasco Piussa, 93762

#### BREVE INTRODUÇÃO
- Para a resolução do projeto que nos foi apresentado, após muita pesquisa e planeamento, criámos dois modelos diferentes, o M1 e o M2. Ambos possuem o mesmo ficheiro de treino e de teste, trainWithoutDev.txt e dev.txt, respetivamente, têm um funcionamento geral similar, e apresentam linha a linha no ficheiro results.txt a categoria que calcularam para cada par pegunta resposta do ficheiro input. 
- No que toca a avaliação, foi criado um ficheiro python que calcula a accuracy de cada modelo, comparando linha a linha a categoria no ficheiro de resultados com a do ficheiro de teste.

#### MODELS
- Tal como foi mencionado anteriormente, ambos os modelos funcionam superficialmente da mesma maneira.
    - Para cada linha do ficheiro de teste, aplicam um pre-processing para criar uma simplificação da string que retiram, e passam-na para o algoritmo que implementam. Ambos os algoritmos exercem cálculos entre a simplificação que recebem e as strings também simplificadas de todas as linhas do ficheiro de treino. 
    - Por fim, é posta a categoria calculada no ficheiro de respostas (results.txt).
- Pondo as suas semelhanças de parte, revelamos agora onde se diferem.
- O modelo M1 contém os seguintes atributos e métodos: uma lista para cada categoria, pergunta e resposta, um ficheiro de treino, um ficheiro de teste, um objeto que suporta o algoritmo Porter-Stemmer, um threshold, um método stem que aplica o algoritmo Porter-Stemmer a uma frase e devolve a sua simplificação, 1 método jaccard que calcula a distância entre duas frases, e por fim um método compute que executa o modelo. A sua execução segue os seguintes passos:
    - Em primeiro lugar, dividimos cada linha do ficheiro de treino em três segmentos: categoria, pergunta e resposta. 
    - A categoria é adicionada a uma lista de categorias. Por outro lado, tanto a pergunta como a resposta são separadas palavra a palavra (tokenization). A cada palavra aplica-se o algoritmo Porter-Stemmer que a reduz à sua raíz (stemming), tal como demonstrado no seguinte exemplo: Porter-Stemmer("Programmers") = "program". Terminado o pre-processing, ambos os segmentos são adicionadas à sua lista.
    - De seguida, cada linha do ficheiro de teste também é dividida em 3 segmentos (categoria, pergunta e resposta). Ignorando o primeiro segmento, aplicamos o mesmo pre-processing aos restantes, (à pergunta e à resposta). Posteriormente, calculamos o jaccard da pergunta da atual linha do ficheiro de teste com todas as perguntas guardadas no atributo lista de perguntas. Qualquer valor que seja igual ou inferior ao threshold selecionado é discartado, porém aos que obtiveram um resultado superior calculamos o jaccard da resposta da linha com a resposta 

#### EXPERIMENTAL SETUP

#### RESULTS
- Apesar das suas semelhanças, enquanto que o M1 alcança apenas uma precisão de 69.4% em 27.649 segundos, o M2 atinge uma precisão de 84.2% em 21.725 segundos.

#### ERROR ANALYSIS

#### FUTURE WORK

#### BIBLIOGRAPHY
