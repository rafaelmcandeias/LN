
##### TODO RELATORIO
- Os testes seguem o formato LABEL^IQUESTION^IANSWER


### Pre-Processing:
- Porter's Stemmer:
    - remove common suffixes from sentences
    - text normalization:
        porter.stem('amazement') returns ‘amaz’
        porter.stem('amaze') returns ‘amaz’
        porter.stem('amazed') returns ‘amaz’
    
- Snowball Stemmer:
    - is widely accepted as an improved version from Porter’s Stemmer.
    - much better on normalizing:
        porter.stem('fairly')   -> fairli
        snowball.stem('fairly') -> fair
    - prevent some overstemming ex:
        porter.stem('generically')   -> gener;     porter.stem('generous')   -> gener
        snowball.stem('generically') -> generical; snowball.stem('generous') -> generous
    
- Lancaster Stemmer:
    - Its rules are more agressive than Porter and Snowball and it is one of the most agressive stemmers as it tends to overstem a lot of words.
        snowball.stem('sales') -> 'sale'; snowball.stem('salty') -> 'salti'
        lanc.stem('sales')     -> 'sal';  lanc.stem('salty')     -> 'sal'
    
- Stop words:
    - The stopwords are a list of words that are very very common but don’t provide useful information for most text analysis procedures. We save space and time just by removing them.
        removingStopwords("This is a sample sentence, showing off the stop words filtration.") -> 
        -> "This sample sentence, showing stop words filtration." 

- Stop chars:
    - The corpus contains a ton of rubbish: "Bix Biederbecke's bio: ""Young Man With A ____"""
    - Removing all the unecessary chars will clean the corpus
        "Bix Biederbecke's bio: ""Young Man With A ____""" -> Bix Biederbecke's bio Young Man With A


### Algorithms:
- Jaccard:
    - proximity measurement used to compute the similarity between two objects
- Naive bayes:
    - applying Bayes’ theorem with the “naive” assumption of conditional independence between every pair of features given the value of the class variable
    - fast, easy to implement
    - corpus is imbalanced
    - TOTAL = 9500 (wc -l trainWithoutDev.txt)
    - (grep -E "CATEGORY" trainWithoutDev.txt | wc -l):
        - SCIENCE: 1479 -> 15.57% 
        - HISTORY: 2598 -> 27.35%
        - LITERATURE: 2240 -> 23.58%
        - GEOGRAPHY: 1013 -> 10.66%
        - MUSIC: 2203 -> 23.19%
- Complement Naive bayes:
    - CNB is an adaptation of the standard multinomial naive Bayes (MNB) algorithm that is particularly suited for imbalanced data sets
    - Calcula a probabilidade de nao pertencer às outras classes
- SVM:


#### Model1:
- Pre-processing:
    - Porter's Stemmer:
        ACC: 0.694  TEMP: 32.526s
    - Snowball:
        ACC: 0.706 TEMP: 29.707s
    - Lancaster Stemmer:
        ACC: 0.704 TEMP: 31.446s

- Algorithm:
    - Jaccard é facil de implemetar, nao requer muita complexidade
        - Com Jaccard(Q1, Q2) + Jaccard(R1, R2)
            ACC: 0.706 TEMP: 29.707s
        - Com Jaccard(Q1 + R1, Q2 + R2)
            ACC: 0.608 TEMP: 44.045s


#### Model2:
- Pre-processing:
    - Removing stop-words, such as {‘ourselves’, ‘hers’, ‘between’, ‘yourself’, ‘but’, ‘again’, ‘there’, ‘about’, ‘once’, ...}
    - Removing stop-chars to clean the corpus:
        - Chars a remover comparando com todos os previamente selecionados REMOVER OU NAO DA PALAVRA?
            TUDO -> ACC: 0.842 TEMP: 23.579s
            _ -> corpus tem 63, 56 sao de MUSIC -> se nao remover o char da w, ACC: 0.842 -> NAO
            : -> corpus tem 280                 -> se nao remover o char da w, ACC: 0.842 -> NAO
            ? -> corpus tem 72                  -> se nao remover o char da w, ACC: 0.842 -> NAO
            ! -> corpus tem 143                 -> se nao remover o char da w, ACC: 0.84  -> SIM
            ; -> corpus tem 347                 -> se nao remover o char da w, ACC: 0.844 -> NAO 
            " -> corpus tem 3540                -> se nao remover o char da w, ACC: 0.834 -> SIM
            & -> corpus tem 2081                -> se nao remover o char da w, ACC: 0.84  -> SIM
            ' -> corpus tem 2835                -> se nao remover o char da w, ACC: 0.848 -> NAO
            ( -> corpus tem 611                 -> se nao remover o char da w, ACC: 0.842 -> NAO
            ) -> corpus tem 611                 -> se nao remover o char da w, ACC: 0.842 -> NAO
            [ -> corpus tem 16                  -> se nao remover o char da w, ACC: 0.842 -> NAO
            ] -> corpus tem 16                  -> se nao remover o char da w, ACC: 0.842 -> NAO
            \--> corpus tem 1179                -> se nao remover o char da w, ACC: 0.84  -> SIM
            => REMOVER APENAS {!, ", &, -}
            
    - Porter's Stemmer:
        ACC: 0.848 TEMP: 18.929s
    - Snowball:
        ACC: 0.838 TEMP: 24.574s
    - LancasterStemmer:
        ACC: 0.834 TEMP: 22.575s

- Algorithm:
    - Naive Bayes:
        ACC: 0.844 TEMP: 18.929s
    - Complement Naive Bayes:
        ACC: 0.848 TEMP: 40.496s
    - EXP: SVM:
        ACC: 0. TEMP: 
    - EXP: Tf-idf: 
        ACC: 0. TEMP: 

