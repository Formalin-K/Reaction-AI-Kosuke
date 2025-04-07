import pickle
import numpy as np
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.models import load_model

def custom_softmax(x, axis=1):
    ndim = K.ndim(x)
    if ndim == 2:
        return K.softmax(x, axis=axis)
    elif ndim > 2:
        e = K.exp(x - K.max(x, axis=axis, keepdims=True))
        s = K.sum(e, axis=axis, keepdims=True)
        return e / s
    else:
        raise ValueError('1Dテンソルには適用できません')

def load_prediction_model(folder_path):
    # 学習済みモデルを読み込み
    model = load_model(
        f"{folder_path}/model_with_embedding.h5",
        custom_objects={"custom_softmax": custom_softmax}
    )
    # vocab_data を読み込み
    with open(f"{folder_path}/vocab_data.pkl", "rb") as f:
        vocab_data = pickle.load(f)
    return model, vocab_data

def string_to_int(string_tokens, length, vocab):
    unk_idx = vocab["<unk>"]
    pad_idx = vocab["<pad>"]
    if len(string_tokens) > length:
        string_tokens = string_tokens[:length]
    rep = [vocab.get(tok, unk_idx) for tok in string_tokens]
    if len(rep) < length:
        rep += [pad_idx] * (length - len(rep))
    return rep

def int_to_string(id_list, inv_vocab):
    return [inv_vocab[i] for i in id_list]

def predict_product(input_smiles_str, model, vocab_data):
    tokens = input_smiles_str.split()
    X_ids = string_to_int(tokens, vocab_data["Tx"], vocab_data["reactants_vocab"])
    X_ids = np.array([X_ids])  # shape: (1, Tx)

    s0 = np.zeros((1, vocab_data["n_s"]))
    c0 = np.zeros((1, vocab_data["n_s"]))

    # model.predict は出力が [ (1, vocab), (1, vocab), ... ] (Ty個)
    predictions = model.predict([X_ids, s0, c0]) 

    # 各タイムステップの argmax をとる
    pred_ids = [np.argmax(step_pred[0]) for step_pred in predictions]
    pred_tokens = [vocab_data["inv_products_vocab"][idx] for idx in pred_ids]

    # <pad> は削除
    pred_tokens = [t for t in pred_tokens if t != "<pad>"]

    # トークンを結合して出力文字列に
    return "".join(pred_tokens)


