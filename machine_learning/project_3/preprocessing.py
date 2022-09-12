import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import nltk
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import auc
from nltk.corpus import stopwords
from laserembeddings import Laser
import matplotlib.pyplot as plt

"""### Preproccesing"""

def preprocessing_tf_idf_vectorizer_standard_scaler_pca(train, val):
    train_sn, val_sn = sin_nulos(train, val)
    
    train_tf_idf, val_tf_idf = aplicar_tf_idf(train_sn, val_sn)
    
    train_reducido, val_reducido = aplicar_pca(train_tf_idf, val_tf_idf)
    
    return aplicar_standard_scaler(train_reducido, val_reducido)

def obtener_embeddings(train, val, test):
    train_sn, val_sn, test_sn = sin_nulos(train['Tweet-Content'], val['Tweet-Content'], test['Tweet-Content'], True)
    
    lista_tweets_train = train_sn.to_list()
    lista_idiomas_train = train.Lang

    lista_tweets_val = val_sn.to_list()
    lista_idiomas_val = val.Lang
    
    lista_tweets_test = test_sn.to_list()
    lista_idiomas_test = test.Lang
    
    laser = Laser()
    
    embeddings_train = laser.embed_sentences(lista_tweets_train, lang=lista_idiomas_train)
    embeddings_val = laser.embed_sentences(lista_tweets_val, lang=lista_idiomas_val)
    embeddings_test = laser.embed_sentences(lista_tweets_test, lang=lista_idiomas_test)
    
    return embeddings_train, embeddings_val, embeddings_test

def sin_nulos(train, val, test=None, hay_test=False):
    if hay_test:
        return train.fillna("Without data"), val.fillna("Without data"), test.fillna("Without data")
    
    return train.fillna("Without data"), val.fillna("Without data")

def aplicar_tf_idf(train, val):
    stops_ingles = list(stopwords.words('english'))
    stops_portuges = list(stopwords.words('portuguese'))
    stops = stops_ingles + stops_portuges
    
    vectorizer = TfidfVectorizer(lowercase=True, stop_words=stops, max_features=2000)
    
    return vectorizer.fit_transform(train).toarray(), vectorizer.transform(val).toarray()

def aplicar_pca(train, val):
    pca = PCA(n_components=100)
    
    return pca.fit_transform(train), pca.transform(val)

def aplicar_standard_scaler(train, val):
    scaler = StandardScaler()
    
    return scaler.fit_transform(train), scaler.transform(val)


"""### Funciones utiles"""

def obtener_data_frames_ingles(obtener_test=False):
    test = None
    weak = pd.read_csv('English-Weakly-labeled-Tweets.csv', names=['Tweet-Content', 'Class'], sep='\t')
    train = pd.read_csv('Training_1.csv', names=['Tweet-Content', 'Class'], sep='\t')
    
    if obtener_test:
        test = pd.read_csv('Test_1.csv', names=['Tweet-Content', 'Class'], sep='\t')
    
    return weak, train, test

def obtener_data_frames_portugues(obtener_test=False):
    test = None
    weak = pd.read_csv('Portuguese-Weakly-Labeled-Tweets.csv', sep='\t')
    train = pd.read_csv('Training_3.csv', usecols=['text', 'politico'])
    
    if obtener_test:
        test = pd.read_csv('Test_3.csv', usecols=['text', 'politico'])
    
    return weak, train, test

def obtener_data_frames_ingles_portugues_y_target(df_ing, df_por, incluir_leng=False):
    df_ing_ = df_ing.copy()
    df_por_ = df_por.copy()
    
    df_ing_['Class'] = df_ing_.Class.map({'NOT':0, 'POLIT':1})
    
    df_por_.columns = ['Tweet-Content','Class']
    
    if incluir_leng:
        df_ing_['Lang'] = 'en'
        df_por_['Lang'] = 'pt'
    
    tw_ingles_portuges = pd.concat([df_ing_, df_por_])
    
    if incluir_leng:
        return tw_ingles_portuges[['Tweet-Content', 'Lang']], tw_ingles_portuges.Class
    
    return tw_ingles_portuges['Tweet-Content'], tw_ingles_portuges.Class
    
def obtener_data_frames_ingles_portugues_y_target_weak(df_ing_weak, df_por_weak, df_ing_por, df_ing_por_target, incluir_leng=False):
    df_ing_weak_ = df_ing_weak.copy()
    df_por_weak_ = df_por_weak.copy()
    
    df_ing_weak_['Class'] = df_ing_weak_.Class.map({'NOT':0, 'POLIT':1})
    df_por_weak_['Class'] = df_por_weak_.Class.map({'NOT':0, 'POLIT':1})
    
    if incluir_leng:
        df_ing_weak_['Lang'] = 'en'
        df_por_weak_['Lang'] = 'pt'
        tw_ingles_portuges_weak = pd.concat([df_ing_weak_[['Tweet-Content', 'Lang']], df_por_weak_[['Tweet-Content', 'Lang']], df_ing_por])
        tw_ingles_portuges_weak_target = pd.concat([df_ing_weak_.Class, df_por_weak_.Class, df_ing_por_target])
        return tw_ingles_portuges_weak, tw_ingles_portuges_weak_target
    
    tw_ingles_portuges_weak_train_df = pd.concat([df_ing_weak_['Tweet-Content'], df_por_weak_['Tweet-Content'], df_ing_por])
    tw_ingles_portuges_weak_train_target_df = pd.concat([df_ing_weak_.Class, df_por_weak_.Class, df_ing_por_target])
    return tw_ingles_portuges_weak_train_df, tw_ingles_portuges_weak_train_target_df

def plot_roc(_fpr, _tpr, x, titulo):
  roc_auc = auc(_fpr, _tpr)

  plt.figure(figsize=(12, 6), dpi=100)
  plt.plot(
      _fpr, _tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.4f})'
  )
  plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
  plt.xlim([0.0, 1.0])
  plt.ylim([0.0, 1.05])
  plt.xlabel('False Positive Rate')
  plt.ylabel('True Positive Rate')
  plt.title(titulo)
  plt.legend(loc="lower right")
  plt.show()