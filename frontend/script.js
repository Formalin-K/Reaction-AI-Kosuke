async function drawPredictedSmiles() {
  // ★ 入力テキストを取得
  const rawInput = document.getElementById('smiles-input').value.trim();
  const tokens = rawInput.split(" ");  // ["C", "O", ".", "Cl", "C", ...]
  
  // ★ '.' の位置を探す（無い場合は-1）
  const dotIndex = tokens.indexOf('.');
  
  // 分子A用、分子B用のトークン配列
  let tokensA = [];
  let tokensB = [];
  
  if (dotIndex !== -1) {
    // '.' が見つかった場合 → 2つの分子に分割
    tokensA = tokens.slice(0, dotIndex);        // ピリオド前
    tokensB = tokens.slice(dotIndex + 1);       // ピリオド後
  } else {
    // '.' が無い場合は全部Aとみなす
    tokensA = tokens;
    tokensB = [];
  }
  
  // ★ SMILES に結合
  //   A分子
  const smilesA = tokensA.join("");  // ex: ["C","O"] => "CO"
  //   B分子
  const smilesB = tokensB.join("");  // ex: ["Cl","C","c","1",...] => "ClCc1..."

  // ★ 分子A・Bを描画
  drawMolecule(smilesA, "input-molA");
  drawMolecule(smilesB, "input-molB");
  
  // ★ 予測実行
  try {
    // fetchでAPIにPOST
    const res = await fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input: rawInput })
    });
    if (!res.ok) {
      throw new Error(`API Error: ${res.status}`);
    }
    const data = await res.json();  // ex: { "output": "CNc1ccc(Cl)cc1" }
    
    // ★ 出力SMILESを表示
    const predictedSmiles = data.output;
    document.getElementById('predicted-text').textContent 
      = `推論結果: ${predictedSmiles}`;
    
    // ★ 出力の構造を描画
    drawMolecule(predictedSmiles, "output-canvas");
    
  } catch (err) {
    alert("API通信エラー: " + err.message);
  }
}

/**
 * SmilesDrawerを使って SMILES文字列 を canvas に描画するヘルパー関数
 */
function drawMolecule(smiles, canvasId) {
  const canvas = document.getElementById(canvasId);
  const drawer = new SmilesDrawer.Drawer({ width: canvas.width, height: canvas.height });

  // canvasクリア
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // 空文字や undefined の場合、そのまま return
  if (!smiles) {
    return;
  }

  // parse → draw
  SmilesDrawer.parse(smiles, (tree) => {
    drawer.draw(tree, canvas, 'light', false);
  }, (err) => {
    alert(`'${smiles}' のパースに失敗: ${err}`);
  });
}



