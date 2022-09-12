import pandas as pd
import numpy as np
import warnings
import category_encoders as ce

from sklearn.impute import KNNImputer
from sklearn.feature_extraction import FeatureHasher
from sklearn.preprocessing import (
    RobustScaler, 
    StandardScaler,
    OneHotEncoder)
from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    CountVectorizer)

#filtrado de warnings
warnings.filterwarnings('ignore')

# suprimimos la notacion cientifica en los outputs en pandas
pd.options.display.float_format = '{:20,.2f}'.format

#defino unas constantes
KNN = 'knn'
MEAN = 'mean'
MEAN_SMOOTH = 'mean_smooth'
STANDARD = 'standard'
ROBUST = 'robust'
COUNT = 'count'
TF_IDF = 'tf_idf'

"""### Preproccesings"""
        
def preprocessing_knn_imputer_robust_escaler_one_hot_encoding_hashing_encoding(X_train, X_val_dev, dataset_test=None, test=False):
  X_train_sn, X_val_dev_sn, test_sn = aplicar_imputer(X_train, X_val_dev, KNN, dataset_test, test)

  X_train_sin_content_surprise2, X_val_dev_sin_content_surprise2, test_sin_content_surprise2 = hashing_encoding(X_train_sn, X_val_dev_sn, test_sn, test)
  
  X_train_sin_cat, X_val_dev_sin_cat, test_sin_cat = one_hot_encoding(X_train_sin_content_surprise2, X_val_dev_sin_content_surprise2, test_sin_content_surprise2, test)

  return aplicar_sacaler(X_train_sin_cat, X_val_dev_sin_cat, ROBUST, test_sin_cat, test) 

def preprocessing_knn_imputer_standar_escaler_one_hot_encoding_mean_encoding_count_vectorizer(X_train, X_val_dev, target, dataset_test=None, test=False):
  X_train_sn, X_val_dev_sn, test_sn = aplicar_imputer(X_train, X_val_dev, KNN, dataset_test, test)

  X_train_sin_content, X_val_dev_sin_content, test_sin_content = aplicar_vectorizer_encoding(X_train_sn, X_val_dev_sn, COUNT, test_sn, test)
  
  aux = X_train_sin_content.join(target.to_frame())
  X_train_sin_surprise2, X_val_dev_sin_surprise2, test_sin_surprise2 = aplicar_mean_encoding(aux, X_val_dev_sin_content, target.name, MEAN, test_sin_content, test)

  X_train_sin_cat, X_val_dev_sin_cat, test_sin_cat = one_hot_encoding(X_train_sin_surprise2, X_val_dev_sin_surprise2, test_sin_surprise2, test)

  return aplicar_sacaler(X_train_sin_cat, X_val_dev_sin_cat, STANDARD, test_sin_cat, test)

def preprocessing_mean_imputer_robust_escaler_one_hot_encoding_mean_encoding_smooth_tf_idf_vectorizer(X_train, X_val_dev, target, dataset_test=None, test=False):
  X_train_sn, X_val_dev_sn, test_sn = aplicar_imputer(X_train, X_val_dev, MEAN, dataset_test, test)

  X_train_sin_content, X_val_dev_sin_content, test_sin_content = aplicar_vectorizer_encoding(X_train_sn, X_val_dev_sn, TF_IDF, test_sn, test)
  
  aux = X_train_sin_content.join(target.to_frame())
  X_train_sin_surprise2, X_val_dev_sin_surprise2, test_sin_surprise2 = aplicar_mean_encoding(aux, X_val_dev_sin_content, target.name, MEAN_SMOOTH, test_sin_content, test, 100)

  X_train_sin_cat, X_val_dev_sin_cat, test_sin_cat = one_hot_encoding(X_train_sin_surprise2, X_val_dev_sin_surprise2, test_sin_surprise2, test)
    
  return aplicar_sacaler(X_train_sin_cat, X_val_dev_sin_cat, ROBUST, test_sin_cat, test)

def preprocessing_mean_imputer_standar_escaler_one_hot_encoding_binary_encoding(X_train, X_val_dev, dataset_test=None, test=False):
  X_train_sn, X_val_dev_sn, test_sn = aplicar_imputer(X_train, X_val_dev, MEAN, dataset_test, test)

  X_train_sin_content_surprise2, X_val_dev_sin_content_surprise2, test_sin_content_surprise2 = binary_encoding(X_train_sn, X_val_dev_sn, test_sn, test)
    
  X_train_sin_cat, X_val_dev_sin_cat, test_sin_cat = one_hot_encoding(X_train_sin_content_surprise2, X_val_dev_sin_content_surprise2, test_sin_content_surprise2, test)

  return aplicar_sacaler(X_train_sin_cat, X_val_dev_sin_cat, STANDARD, test_sin_cat, test) 

"""### Encoders"""

def one_hot_encoding(X_train, X_val_dev, dataset_test, test):
  encoder = OneHotEncoder()
  test_sin_categoricas = None
    
  features_categoricos = obtener_features_categoricos(X_train)
  train_categoricos = X_train[features_categoricos]
  val_dev_catecoricos = X_val_dev[features_categoricos]

  X_train_resultado = encoder.fit_transform(train_categoricos).toarray()
  X_val_dev_resultado = encoder.transform(val_dev_catecoricos).toarray()

  aux_train = pd.DataFrame(X_train_resultado, columns=encoder.get_feature_names())
  aux_val_dev = pd.DataFrame(X_val_dev_resultado, columns=encoder.get_feature_names())

  train_sin_categoricas = X_train.drop(columns=features_categoricos).reset_index()
  val_dev_sin_categoricas = X_val_dev.drop(columns=features_categoricos).reset_index()

  train_sin_categoricas[aux_train.columns] = aux_train
  val_dev_sin_categoricas[aux_val_dev.columns] = aux_val_dev

  if test:
    test_categoricos = dataset_test[features_categoricos]
    test_resultado = encoder.transform(test_categoricos).toarray()

    aux_test = pd.DataFrame(test_resultado, columns=encoder.get_feature_names())

    test_sin_categoricas = dataset_test.drop(columns=features_categoricos).reset_index()

    test_sin_categoricas[aux_test.columns] = aux_test
    test_sin_categoricas = test_sin_categoricas.set_index('url')

  return train_sin_categoricas.set_index('url'), val_dev_sin_categoricas.set_index('url'), test_sin_categoricas

def binary_encoding(X_train, X_val_dev, dataset_test, test):
  encoder = ce.BinaryEncoder(cols=['content', 'surprise2'])
  test_sin_contenido = None

  contenido = X_train[['content', 'surprise2']]
  contenido_val = X_val_dev[['content', 'surprise2']]

  contenido_ = contenido.copy()
  contenido_val_ = contenido_val.copy()
    
  df_binario_train = encoder.fit_transform(contenido_)
  df_binario_val = encoder.transform(contenido_val_)

  dataset_sin_contenido = X_train.drop(columns=['content', 'surprise2'])
  val_sin_contenido = X_val_dev.drop(columns=['content', 'surprise2'])
  
  dataset_sin_contenido[df_binario_train.columns] = df_binario_train
  val_sin_contenido[df_binario_val.columns] = df_binario_val

  if test:
    contenido_test = dataset_test[['content', 'surprise2']]
    contenido_test_ = contenido_test.copy()

    df_binario_test = encoder.transform(contenido_test_)

    test_sin_contenido = dataset_test.drop(columns=['content', 'surprise2'])

    test_sin_contenido[df_binario_test.columns] = df_binario_test


  return dataset_sin_contenido, val_sin_contenido, test_sin_contenido

def hashing_encoding(X_train, X_val_dev, dataset_test, test):
  encoder = ce.HashingEncoder(hash_method='sha256', n_components=7)
  test_sin_contenido = None

  contenido = X_train[['content', 'surprise2']]
  contenido_val = X_val_dev[['content', 'surprise2']]
  
  contenido_ = contenido.copy()
  contenido_val_ = contenido_val.copy()
    
  df_hash_train = encoder.fit_transform(contenido_)
  df_hash_val = encoder.transform(contenido_val_)

  dataset_sin_contenido = X_train.drop(columns=['content', 'surprise2'])
  val_sin_contenido = X_val_dev.drop(columns=['content', 'surprise2'])
  
  dataset_sin_contenido[df_hash_train.columns] = df_hash_train
  val_sin_contenido[df_hash_val.columns] = df_hash_val

  if test:
    contenido_test = dataset_test[['content', 'surprise2']]
    contenido_test_ = contenido_test.copy()
    
    df_hash_test = encoder.transform(contenido_test_)

    test_sin_contenido = dataset_test.drop(columns=['content', 'surprise2'])

    test_sin_contenido[df_hash_test.columns] = df_hash_test

  return dataset_sin_contenido, val_sin_contenido, test_sin_contenido

def aplicar_vectorizer_encoding(X_train, X_val_dev, tipo_vectorizer, dataset_test, test):
    vectorizers = {COUNT: CountVectorizer,
                    TF_IDF: TfidfVectorizer} 

    vectorizer = vectorizers[tipo_vectorizer](lowercase=True, stop_words='english', max_features=10)
    df_test = None
    
    X_train_ = X_train.copy()
    X_val_dev_ = X_val_dev.copy()
    
    X_train_['content'] = X_train_.content.fillna("Without data")
    X_val_dev_['content'] = X_val_dev_.content.fillna("Without data")
    
    X_train_resultado = vectorizer.fit_transform(X_train_.content).toarray()
    X_val_dev_resultado = vectorizer.transform(X_val_dev_.content).toarray()
    
    aux_train = pd.DataFrame(X_train_resultado, columns=vectorizer.get_feature_names())
    aux_val_dev = pd.DataFrame(X_val_dev_resultado, columns=vectorizer.get_feature_names())
    
    df_X_train = pd.concat([X_train_.drop(columns='content').reset_index(), aux_train], axis=1).set_index('url')
    df_X_val_dev = pd.concat([X_val_dev_.drop(columns='content').reset_index(), aux_val_dev], axis=1).set_index('url')

    if test:
      dataset_test_ = dataset_test.copy()

      dataset_test_['content'] = dataset_test_.content.fillna("Without data")

      test_resultado = vectorizer.transform(dataset_test_.content).toarray()

      aux_test = pd.DataFrame(test_resultado, columns=vectorizer.get_feature_names())

      df_test = pd.concat([dataset_test_.drop(columns='content').reset_index(), aux_test], axis=1).set_index('url')
    
    return df_X_train, df_X_val_dev, df_test

def aplicar_mean_encoding(X_train_con_target, X_val_dev, target, tipo_mean, dataset_test, test, alfa=None):
    test_target = None

    train_target = X_train_con_target.copy()
    val_dev_target = X_val_dev.copy()
    
    promedio_label = X_train_con_target.groupby('surprise2')[target].mean()
    prom_global = X_train_con_target[target].mean()
    
    if tipo_mean == MEAN_SMOOTH:
        cant_filas = X_train_con_target['surprise2'].value_counts()
        promedio_smoothed = (cant_filas * promedio_label + alfa * prom_global) / (cant_filas + alfa)
        
        train_target.loc[:, 'surprise2'] = train_target['surprise2'].map(promedio_smoothed)
        val_dev_target.loc[:, 'surprise2'] = val_dev_target['surprise2'].map(promedio_smoothed)

        if test:
          test_target = dataset_test.copy()
          test_target.loc[:, 'surprise2'] = test_target['surprise2'].map(promedio_smoothed)
          test_target.fillna(prom_global, inplace=True)

    else:
        train_target.loc[:, 'surprise2'] = train_target['surprise2'].map(promedio_label)
        val_dev_target.loc[:, 'surprise2'] = val_dev_target['surprise2'].map(promedio_label)

        if test:
          test_target = dataset_test.copy()
          test_target.loc[:, 'surprise2'] = test_target['surprise2'].map(promedio_label)
          test_target.fillna(prom_global, inplace=True)
    
    return train_target.drop(columns=target), val_dev_target.fillna(prom_global), test_target
 
"""### Imputers"""

def aplicar_imputer(X_train, X_val_dev, imputer,  dataset_test, test):
  imputers = {
    KNN: knn_imputer,
    MEAN: mean_imputer
  }
  return imputers[imputer](
    X_train, 
    X_val_dev,
    dataset_test,
    test
    )

def knn_imputer(X_train, X_val_dev, dataset_test, test):
  # defino un n arbitrario
  imputer = KNNImputer(n_neighbors=2, weights="uniform")
  df_test = None

  columnas_sin_nulls = obtener_features_categoricos(X_train) #los tres tienen las mismas columnas
    
  # Elimino los features sobre los cuales no hay que imputar nada.
  df_X_train = X_train.drop(columns=columnas_sin_nulls)
  df_X_val_dev = X_val_dev.drop(columns=columnas_sin_nulls)
  if test:
    df_test = dataset_test.drop(columns=columnas_sin_nulls)

  for feature in df_X_train.columns:
    imputer.fit(df_X_train[feature].values.reshape(-1, 1))
    df_X_train[feature] = imputer.transform(df_X_train[feature].values.reshape(-1, 1))
    df_X_val_dev[feature] = imputer.transform(df_X_val_dev[feature].values.reshape(-1, 1))
    if test:
      df_test[feature] = imputer.transform(df_test[feature].values.reshape(-1, 1))

  df_X_train[columnas_sin_nulls] = X_train[columnas_sin_nulls]
    
  df_X_val_dev[columnas_sin_nulls] = X_val_dev[columnas_sin_nulls]
  if test:
    df_test[columnas_sin_nulls] = dataset_test[columnas_sin_nulls]

  return df_X_train, df_X_val_dev, df_test

def mean_imputer(X_train, X_val_dev, dataset_test, test):
  df_test = None
  
  columnas_sin_nulls = obtener_features_categoricos(X_train)

  df_X_train = X_train.drop(columns=columnas_sin_nulls)
  df_X_val_dev = X_val_dev.drop(columns=columnas_sin_nulls)
  if test:
    df_test = dataset_test.drop(columns=columnas_sin_nulls)

  for feature in df_X_train.columns:
    df_X_train[feature].fillna((df_X_train[feature].mean()), inplace=True)
    df_X_val_dev[feature].fillna((df_X_train[feature].mean()), inplace=True)
    if test:
      df_test[feature].fillna((df_X_train[feature].mean()), inplace=True)
        
  df_X_train[columnas_sin_nulls] = X_train[columnas_sin_nulls]

  df_X_val_dev[columnas_sin_nulls] = X_val_dev[columnas_sin_nulls]
  if test:
    df_test[columnas_sin_nulls] = dataset_test[columnas_sin_nulls]

  return df_X_train, df_X_val_dev, df_test

"""### Scalers"""

def aplicar_sacaler(X_train, X_val_dev, tipo_scaler, dataset_test, test):
  scalers = {STANDARD:StandardScaler,
            ROBUST:RobustScaler} 

  scaler = scalers[tipo_scaler]()
  sacled_dataset_test = None

  no_categoricos = obtener_features_no_categoricos(X_train)
  categoricos = obtener_features_categoricos(X_train)

  df_X_train = X_train[no_categoricos]
  df_X_val_dev = X_val_dev[no_categoricos]
  aux_X_train_ = df_X_train.reset_index()
  aux_X_val_dev_ = df_X_val_dev.reset_index()
  aux_X_train = aux_X_train_.drop(labels='url', axis=1)
  aux_X_val_dev = aux_X_val_dev_.drop(labels='url', axis=1)
  if test:
    df_test = dataset_test[no_categoricos]
    aux_test_ = df_test.reset_index()
    aux_test = aux_test_.drop(labels='url', axis=1)

  scaler.fit(aux_X_train)
  scaled_dataset_X_train = scaler.transform(aux_X_train)
  scaled_dataset_X_val_dev = scaler.transform(aux_X_val_dev)
  if test:
    scaled_dataset_test = scaler.transform(aux_test)

  nombres = aux_X_train.columns
  scaled_dataset_X_train =  pd.DataFrame(scaled_dataset_X_train, columns=nombres)
  scaled_dataset_X_val_dev = pd.DataFrame(scaled_dataset_X_val_dev, columns=nombres)
  scaled_dataset_X_train['url'] = aux_X_train_['url']
  scaled_dataset_X_val_dev['url'] = aux_X_val_dev_['url']
  scaled_dataset_X_train.set_index('url', inplace=True)
  scaled_dataset_X_val_dev.set_index('url', inplace=True)
  scaled_dataset_X_train[categoricos] = X_train[categoricos]
  scaled_dataset_X_val_dev[categoricos] = X_val_dev[categoricos]
  if test:
    sacled_dataset_test = pd.DataFrame(scaled_dataset_test, columns=nombres)
    sacled_dataset_test['url'] = aux_test_['url']
    sacled_dataset_test.set_index('url', inplace=True)
    sacled_dataset_test[categoricos] = dataset_test[categoricos]

  return scaled_dataset_X_train, scaled_dataset_X_val_dev, sacled_dataset_test

"""### Funciones útiles"""

def obtener_features_categoricos(dataset):
  features_categoricos = []

  for columna in dataset.columns:
    if dataset[columna].dtype == np.object: 
      features_categoricos.append(columna)
  
  return features_categoricos

def obtener_features_no_categoricos(dataset):
  features_no_categoricos = []
  features_categoricos = obtener_features_categoricos(dataset)

  for columna in dataset.columns:
    if columna not in features_categoricos:
      features_no_categoricos.append(columna)
  
  return features_no_categoricos

def train_test_split(train, target, test_size):
    tamanio_train_y_target = len(train) #tienen la misma cantidad de columnas
    cantidad_target = round(tamanio_train_y_target * test_size, 1)
    numero_para_redondear = int(str(cantidad_target).split('.')[1])
    
    if numero_para_redondear > 4:
        cantidad_target = int(cantidad_target) + 1 #siempre redondea para abajo
    
    else:
        cantidad_target = int(cantidad_target)
    
    cantidad_train = tamanio_train_y_target - cantidad_target
    
    X_train = train[:cantidad_train]
    X_test = train[cantidad_train:]
    Y_train = target[:cantidad_train]
    Y_test = target[cantidad_train:]
    
    return X_train, X_test, Y_train, Y_test

def obtener_dataset_predicciones(test, target_test, predicciones):
    test_df = test.copy()
    test_df['popular'] = target_test
    auxiliar = test_df.reset_index()[['popular', 'url']]
    auxiliar = auxiliar.set_index('url')
    
    mi_prediccion = pd.DataFrame(data=predicciones, columns=auxiliar.columns, index=auxiliar.index)
    
    return mi_prediccion
