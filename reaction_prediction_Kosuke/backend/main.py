from predict_utils import load_prediction_model, predict_product

# 1) モデル＆語彙をロード (同一フォルダにあれば "./")
model, vocab_data = load_prediction_model("./")

# 2) 推論したい入力
test_input = "C O . Cl C c 1 c n 2 c c c c c 2 n 1"

# 3) 推論実行
result = predict_product(test_input, model, vocab_data)

print("✅ 入力:", test_input)
print("🧠 出力:", result)




