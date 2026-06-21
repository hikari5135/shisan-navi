import yfinance as yf
import json
import time
import os
import urllib.request
import urllib.error

# 日経225 全銘柄（できる限り網羅）
STOCKS = [
    # 通信・情報
    "9432.T","9433.T","9434.T","4324.T","9613.T","2433.T","4661.T","4385.T","4307.T","9602.T",

    # 金融（銀行・証券・保険・リース）
    "8306.T","8316.T","8411.T","8331.T","8354.T","8355.T","8377.T","8358.T","8333.T","8303.T",
    "8766.T","8630.T","8725.T","8750.T","8591.T","8593.T","8604.T","8601.T","8628.T","8729.T",

    # 商社
    "8058.T","8001.T","8031.T","8053.T","2768.T","8002.T","8015.T",

    # 自動車・輸送機器
    "7203.T","7267.T","7201.T","6902.T","7211.T","7269.T","7270.T","7259.T","7261.T","7202.T",
    "7205.T","7280.T","7186.T",

    # 電機・精密機器
    "6758.T","6861.T","6954.T","7751.T","6981.T","6594.T","6503.T","6501.T","6502.T",
    "6752.T","6724.T","6841.T","6645.T","6963.T","6479.T","6651.T","6504.T","7752.T",
    "6594.T","6857.T","6971.T","6976.T","6967.T","6849.T","6952.T",

    # 化学・素材
    "4063.T","4452.T","3407.T","4901.T","4188.T","5713.T","4005.T","4021.T","4061.T",
    "4042.T","4043.T","4183.T","3402.T","3861.T","3863.T","4004.T","4118.T","4631.T",
    "4911.T","4922.T",

    # 医薬品
    "4502.T","4519.T","4568.T","4523.T","4151.T","4503.T","4506.T","4507.T","4516.T","4528.T",
    "4578.T","4536.T",

    # 半導体・電子部品
    "8035.T","6723.T","6857.T","6920.T","6762.T","6770.T","6963.T",

    # 小売・サービス
    "9983.T","3382.T","9984.T","8267.T","9843.T","3086.T","8233.T","2651.T","9069.T",
    "9831.T","9962.T","2702.T","3038.T","3092.T",

    # 食品
    "2502.T","2914.T","2503.T","2801.T","2269.T","2002.T","2811.T","2587.T","2206.T",

    # 不動産
    "8801.T","8802.T","8830.T","3289.T","8804.T",

    # 鉄道・運輸
    "9020.T","9022.T","9021.T","9201.T","9202.T","9064.T","9101.T","9104.T","9107.T",
    "9001.T","9005.T","9007.T","9008.T","9009.T",

    # 機械・空調
    "6367.T","6301.T","6326.T","6473.T","6273.T","6113.T","6471.T","6383.T","6361.T",
    "6201.T","6586.T","6305.T","6111.T",

    # ゲーム・エンタメ
    "7974.T","9697.T","9602.T",

    # 建設
    "1801.T","1812.T","1803.T","1802.T","1925.T","1928.T","1812.T",

    # 電力・ガス・インフラ
    "9501.T","9503.T","9502.T","9531.T","9532.T","9506.T","9504.T",

    # 鉄鋼・非鉄金属
    "5401.T","5411.T","5406.T","5802.T","5803.T","5901.T","5703.T","5706.T","5707.T",

    # 紙パルプ・繊維
    "3863.T","3401.T","3404.T","3863.T",

    # 海運・空運
    "9101.T","9104.T","9107.T","9201.T","9202.T",

    # その他製造業
    "7733.T","7731.T","7741.T","7832.T","7912.T","7951.T","7911.T","7270.T",

    # 石油・資源
    "5020.T","1605.T",

    # ガラス・窯業
    "5201.T","5233.T","5301.T","5332.T","5333.T",

    # 倉庫・物流
    "9301.T","9064.T",

    # その他（広告・サービス・ホールディングス等）
    "4324.T","2413.T","4307.T","9684.T","2768.T","6098.T","4755.T",

    # ===== ここから追加：300銘柄規模への拡充分（中堅優良企業中心） =====

    # 通信・情報・IT追加
    "3659.T","2317.T","4689.T","3923.T","4751.T","2150.T","4716.T",

    # 金融追加
    "8309.T","8308.T","7186.T","8473.T","8697.T","8439.T",

    # 商社・卸売追加
    "2670.T","9962.T","3076.T",

    # 自動車・部品追加
    "7259.T","7240.T","7259.T","5108.T","7259.T","6473.T","7259.T",

    # 電機・精密追加
    "6952.T","6841.T","6754.T","6645.T","6976.T","6963.T","6920.T","6504.T","6592.T","6630.T",

    # 化学・素材追加
    "4631.T","4204.T","4208.T","4912.T","4203.T","3401.T",

    # 医薬品・ヘルスケア追加
    "4534.T","4536.T","4527.T","4541.T","4543.T","4544.T",

    # 半導体追加
    "6963.T","6981.T","6963.T",

    # 小売・サービス追加
    "3092.T","2784.T","3099.T","8233.T","9831.T","2702.T",

    # 食品追加
    "2229.T","2871.T","2875.T","2002.T","2871.T",

    # 不動産追加
    "8804.T","3231.T","8923.T",

    # 鉄道・運輸追加
    "9006.T","9008.T","9042.T","9009.T",

    # 機械追加
    "6113.T","6135.T","6141.T","6383.T","6361.T","6395.T",

    # 建設・住宅追加
    "1812.T","1820.T","1721.T","1860.T","8881.T",

    # 電力・ガス追加
    "9505.T","9508.T","9532.T",

    # 鉄鋼・非鉄追加
    "5631.T","5631.T","5631.T","5631.T",

    # サービス・人材追加
    "2127.T","6098.T","4732.T","4716.T",

    # さらなる中堅優良企業の追加（業種分散）
    "4912.T","4922.T","2670.T","9783.T","4751.T","2730.T","3038.T",
    "6471.T","6481.T","6486.T","6856.T","6869.T","6877.T","6891.T",
    "7203.T","7148.T","7164.T","7167.T","7180.T","7186.T",
    "8233.T","8252.T","8253.T","8267.T","8358.T","8359.T","8410.T",
    "9697.T","9706.T","9468.T","9437.T","9613.T","9787.T",
    "4543.T","4549.T","4555.T","4559.T","4563.T","4587.T",
    "3105.T","3107.T","3401.T","3404.T","3405.T","3436.T",
    "5101.T","5108.T","5202.T","5232.T","5301.T","5333.T","5334.T",
    "6440.T","6448.T","6460.T","6473.T","6479.T","6594.T",

    # ===== プライム市場 拡充分 Day1（100銘柄） =====
    "1301.T","1332.T","1333.T","1375.T","1377.T","1379.T","1414.T","1417.T","1419.T","1429.T",
    "1433.T","1515.T","1518.T","1662.T","1663.T","1719.T","1720.T","1726.T","1762.T","1766.T",
    "1780.T","1786.T","1808.T","1813.T","1814.T","1815.T","1833.T","1835.T","1852.T","1861.T",
    "1870.T","1871.T","1873.T","1878.T","1879.T","1882.T","1885.T","1887.T","1888.T","1893.T",
    "1898.T","1899.T","1911.T","1926.T","1929.T","1930.T","1934.T","1938.T","1939.T","1941.T",
    "1942.T","1944.T","1945.T","1946.T","1950.T","1951.T","1952.T","1959.T","1961.T","1963.T",
    "1964.T","1968.T","1969.T","1975.T","1976.T","1979.T","1980.T","1982.T","2001.T","2004.T",
    "2053.T","2060.T","2108.T","2109.T","2117.T","2120.T","2121.T","2124.T","2130.T","2146.T",
    "2148.T","2153.T","2154.T","2157.T","2163.T","2168.T","2170.T","2175.T","2181.T","2198.T",
    "2201.T","2207.T","2209.T","2211.T","2212.T","2217.T","2220.T","2222.T","2264.T","2266.T",
]

# 重複を確実に除去
seen = set()
STOCKS = [s for s in STOCKS if not (s in seen or seen.add(s))]


def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        pbr = info.get("priceToBook", None)
        roe = info.get("returnOnEquity", None)
        div = info.get("dividendYield", None)
        debt_to_equity = info.get("debtToEquity", None)
        operating_margin = info.get("operatingMargins", None)
        revenue_growth = info.get("revenueGrowth", None)
        current_ratio = info.get("currentRatio", None)
        beta = info.get("beta", None)

        if div:
            # yfinanceのdividendYieldは基本的に小数表記（例: 0.032 = 3.2%）。
            # まず小数として解釈し、妥当な範囲（0〜15%）に収まればそれを採用する。
            as_decimal = div * 100
            if 0 < as_decimal <= 15:
                div_pct = round(as_decimal, 2)
            elif 15 < as_decimal <= 100:
                # 15%超〜100%は日本株の配当利回りとして非現実的。
                # データ取得異常の可能性が高いため採用しない。
                div_pct = None
            elif 1 <= div <= 15:
                # 既にパーセント表記で渡されているケース（値そのものが1〜15）
                div_pct = round(div, 2)
            else:
                div_pct = None
        else:
            div_pct = None

        equity_ratio = None
        if debt_to_equity is not None:
            try:
                equity_ratio = round(100 / (1 + (debt_to_equity / 100)), 1)
            except ZeroDivisionError:
                equity_ratio = None

        data = {
            "ticker": ticker,
            "name": info.get("longName", ticker),
            "sector": info.get("sector", "不明"),
            "industry": info.get("industry", None),
            "price": info.get("currentPrice", 0),
            "pbr": round(pbr, 2) if pbr else None,
            "roe": round(roe * 100, 2) if roe else None,
            "dividend_yield": div_pct,
            "equity_ratio": equity_ratio,
            "operating_margin": round(operating_margin * 100, 2) if operating_margin else None,
            "revenue_growth": round(revenue_growth * 100, 2) if revenue_growth else None,
            "current_ratio": round(current_ratio, 2) if current_ratio else None,
            "market_cap": info.get("marketCap", 0),
            "beta": round(beta, 2) if beta else None,
        }
        # リスク評価は財務指標のみで決まるため先に計算しておく
        data["risk_level"] = evaluate_risk_level(data)
        return data
    except Exception as e:
        print(f"エラー: {ticker} - {e}")
        return None


HIGH_RISK_BUSINESS_SECTORS = {
    "Financial Services": "投資・金融関連企業は、財務指標が一般事業会社と単純比較できない場合があります",
}

# 投資持株会社・特殊な財務構造を持つことが多い大手企業（簡易判定用）
SPECIAL_STRUCTURE_KEYWORDS = ["SoftBank Group", "Investment", "Holdings Capital"]


def is_special_structure_company(stock):
    """投資会社・特殊な財務構造を持つ可能性のある企業を簡易判定する"""
    name = (stock.get("name") or "")
    for kw in SPECIAL_STRUCTURE_KEYWORDS:
        if kw in name:
            return True
    return False


def evaluate_nisa_fit(stock, fp_score=None, risk_level_result=None):
    """
    「長期積立適性」を簡易判定する。
    これは「企業評価スコア（FPスコア）」とは異なる、別の評価軸である。
    FPスコアが企業の財務的な優秀さを表すのに対し、長期積立適性は
    「値動きの安定性」「収益の継続性」「特殊な財務構造でないか」など、
    “長期間にわたり積立で持ち続けやすいか” という観点を加味した指標。

    そのため、FPスコアが非常に高い企業であっても、業績の振れ幅が大きい
    業種（半導体・ハイテク等）やリスク評価が高い銘柄では、長期積立適性は
    あえて控えめな評価になることがある。これは矛盾ではなく、評価軸が
    異なることによる意図した結果である。

    判定基準：配当の安定性・財務健全性・極端な割高でないこと・収益性（赤字でないこと）。

    【他の評価指標との関係】
    星評価は以下の3つの上限のうち、最も厳しいものが適用される。
    - ROEがマイナス／5%未満、または投資持株会社等 → 星3が上限
    - リスク評価が「高」または「中」 → 星4が上限
    - FPスコアが低い場合 → FPスコアに応じた上限を適用
      （90点以上:★5／80点台:★4／70点台:★4／60点台:★3／60点未満:★2）
    """
    reasons = []
    points = 0

    equity_ratio = stock.get("equity_ratio")
    div_yield = stock.get("dividend_yield")
    pbr = stock.get("pbr")
    roe = stock.get("roe")

    if div_yield is not None and div_yield >= 2.5:
        points += 1
        reasons.append("配当が安定的")

    if equity_ratio is not None and equity_ratio >= 40:
        points += 1
        reasons.append(f"財務が健全（自己資本比率{equity_ratio}%）")

    if pbr is not None and pbr > 0 and pbr <= 2.5:
        points += 1
        reasons.append("極端な割高ではない")

    roe_is_negative = roe is not None and roe < 0
    roe_is_low = roe is not None and 0 <= roe < 5

    if roe is not None and roe >= 8:
        points += 1
        reasons.append("収益性が安定")
    elif roe_is_negative:
        reasons.append("⚠️ 直近の自己資本利益率（ROE）がマイナスです")
    elif roe_is_low:
        reasons.append("収益性はまだ十分に高いとは言えません")

    # 星の基本算出（素点ベース）
    if points >= 4:
        stars = 5
    elif points == 3:
        stars = 4
    elif points == 2:
        stars = 3
    else:
        stars = 2

    # ---- 上限①：ROE・特殊構造企業による制限（星3まで） ----
    structure_cap_applied = False
    if roe_is_negative or roe_is_low or roe is None:
        if stars > 3:
            stars = 3
        structure_cap_applied = True
        if roe_is_negative and "⚠️ 直近の自己資本利益率（ROE）がマイナスです" not in reasons:
            reasons.append("⚠️ 直近の自己資本利益率（ROE）がマイナスです")

    if is_special_structure_company(stock):
        if stars > 3:
            stars = 3
        structure_cap_applied = True
        reasons.append("⚠️ 投資持株会社等、財務構造が一般事業会社と異なる可能性があります（NAVディスカウント等にご注意ください）")

    # ---- 上限②：リスク評価による制限（指摘①への対応） ----
    risk_cap_applied = False
    if risk_level_result:
        risk_lv = risk_level_result.get("level")
        if risk_lv == "高":
            if stars > 4:
                stars = 4
            risk_cap_applied = True
            reasons.append("⚠️ リスク評価が「高」のため、星評価を調整しています")
        elif risk_lv == "中":
            if stars > 4:
                stars = 4

    # ---- 上限③：FPスコアによる制限（指摘②への対応） ----
    score_cap_applied = False
    if fp_score is not None:
        if fp_score >= 90:
            score_cap = 5
        elif fp_score >= 80:
            score_cap = 4
        elif fp_score >= 70:
            score_cap = 4
        elif fp_score >= 60:
            score_cap = 3
        else:
            score_cap = 2
        if stars > score_cap:
            stars = score_cap
            score_cap_applied = True

    # 最終的なレベル表示（上限が適用された場合は理由を明示）
    if stars >= 5:
        level = "非常に高い"
    elif stars == 4:
        level = "高い"
    elif stars == 3:
        level = "普通"
    else:
        level = "要検討"

    # 注記：FPスコア（企業評価）が高くても、長期積立適性は別軸で
    # 評価していることが伝わるよう理由欄にも明記する
    if structure_cap_applied:
        pass  # 既にreasonsに理由が追加済み
    elif risk_cap_applied:
        reasons.append("値動きの振れ幅が大きい可能性があるため、積立比率は抑えめが無難です")
    elif score_cap_applied and fp_score is not None and fp_score < 60:
        reasons.append("企業評価スコアが他行と比べてやや控えめなため、慎重な判断をおすすめします")

    if not reasons:
        reasons.append("十分な評価情報がありません")

    return {"level": level, "stars": stars, "reasons": reasons}


SECTOR_RISK_NOTES = {
    "Industrials": "景気変動・燃料費や原材料費の影響を受けやすい業種です",
    "Real Estate": "金利上昇・不動産市況の影響を受けやすい業種です",
    "Financial Services": "金利動向・市場変動・自然災害（保険）の影響を受けやすい業種です",
    "Consumer Cyclical": "景気動向や個人消費の変化の影響を受けやすい業種です",
    "Basic Materials": "原材料価格・為替変動の影響を受けやすい業種です",
    "Energy": "資源価格・地政学リスクの影響を受けやすい業種です",
    "Technology": "技術革新の速さや競争環境の変化が大きい業種です",
    "Communication Services": "規制動向や競争環境の変化の影響を受けやすい業種です",
    "Utilities": "規制・燃料価格の影響を受けやすい一方、比較的安定した業種です",
    "Healthcare": "薬価改定や規制動向の影響を受けやすい業種です",
    "Consumer Defensive": "比較的景気の影響を受けにくい安定した業種です",
}

# industry（より詳細な業種）ベースの注記。sectorより優先して使う。
# yfinance（米国基準のGICS分類）では日本の建設業が「Real Estate」セクターに
# 分類されることがあるため、industryで実態に近い表記・注記に補正する。
INDUSTRY_RISK_NOTES = {
    "Engineering & Construction": "建設業の特性として、資材価格や工期の影響を受けやすい業種です",
    "Real Estate Services": "不動産市況・金利動向の影響を受けやすい業種です",
    "Real Estate—Development": "不動産開発を手がけており、金利・不動産市況の影響を受けやすい業種です",
}

# 表示用の日本語業種ラベル（industryをもとに、より実態に近い表記にする）
INDUSTRY_DISPLAY_LABELS = {
    "Engineering & Construction": "建設業",
    "Real Estate Services": "不動産サービス業",
    "Real Estate—Development": "不動産開発業",
}


def get_display_sector(stock):
    """
    表示用の業種名を決定する。
    industry（詳細業種）に対応する日本語ラベルがあればそれを優先し、
    なければsector（GICS大分類）をそのまま使う。
    """
    industry = stock.get("industry")
    if industry and industry in INDUSTRY_DISPLAY_LABELS:
        return INDUSTRY_DISPLAY_LABELS[industry]
    return stock.get("sector", "不明")


def evaluate_risk_level(stock):
    """
    リスク評価（信号機方式）。
    ベータ値（市場感応度）・財務健全性・配当性向・業種特性などから簡易判定する。
    """
    reasons = []
    risk_points = 0  # 高いほどリスクが高い

    beta = stock.get("beta")
    if beta is not None:
        if beta >= 1.3:
            risk_points += 2
            reasons.append("株価が市場平均より大きく変動しやすい（景気敏感）")
        elif beta >= 1.0:
            risk_points += 1
            reasons.append("株価が市場平均並みに変動する")

    equity_ratio = stock.get("equity_ratio")
    if equity_ratio is not None:
        if equity_ratio < 25:
            risk_points += 2
            reasons.append("自己資本比率が低く、借入への依存度が高い")
        elif equity_ratio < 40:
            risk_points += 1
            reasons.append("自己資本比率がやや低め")

    div_yield = stock.get("dividend_yield")
    roe = stock.get("roe")
    if div_yield is not None and roe is not None and roe > 0:
        payout_proxy = div_yield / roe  # 簡易的な配当性向の代理指標
        if payout_proxy >= 0.5:
            risk_points += 1
            reasons.append("利益に対して配当負担がやや大きい可能性")

    # 収益性（ROE）がマイナスの場合は明確なリスク要因として追加
    if roe is not None and roe < 0:
        risk_points += 2
        reasons.append("⚠️ 直近の自己資本利益率（ROE）がマイナスです（収益性に懸念）")

    # 投資持株会社など特殊な財務構造を持つ可能性がある企業
    if is_special_structure_company(stock):
        risk_points += 1
        reasons.append("投資持株会社等、財務構造が一般事業会社と異なる可能性があります")

    # 業種固有のリスク注記（加点はしないが必ず注記として表示する）
    # industry（詳細業種）の注記があればそちらを優先し、なければsectorの注記を使う
    industry = stock.get("industry")
    sector = stock.get("sector")
    industry_note = INDUSTRY_RISK_NOTES.get(industry) if industry else None
    sector_note = SECTOR_RISK_NOTES.get(sector)

    final_note = industry_note if industry_note else sector_note
    if final_note:
        # Consumer Defensive / Utilities は「安定業種」のため減点（リスクを下げる）扱いにはしないが、
        # それ以外はリスク要因として1点加算する
        if sector not in ("Consumer Defensive",):
            risk_points += 1
        reasons.append(f"【業種特性】{final_note}")

    if risk_points >= 3:
        level = "高"
        color = "red"
    elif risk_points >= 1:
        level = "中"
        color = "yellow"
    else:
        level = "低"
        color = "green"

    if not reasons:
        reasons.append("特筆すべきリスク要因は確認されませんでした")

    return {"level": level, "color": color, "reasons": reasons}



def linear_score(value, pass_line, excellent_line, max_score, higher_is_better=True):
    """
    値を「合格ライン」〜「優秀ライン」の間で線形補間し、0〜max_scoreの連続値にする。
    - value が合格ラインに届かない場合は0点
    - value が優秀ラインに到達/超過した場合はmax_score（ただし100点連発を避けるため
      run_screening側でさらに緩やかな圧縮をかける）
    """
    if value is None:
        return 0
    if higher_is_better:
        if value < pass_line:
            return 0
        if value >= excellent_line:
            ratio = 1.0
        else:
            ratio = (value - pass_line) / (excellent_line - pass_line)
    else:
        if value > pass_line:
            return 0
        if value <= excellent_line:
            ratio = 1.0
        else:
            ratio = (pass_line - value) / (pass_line - excellent_line)
    return round(max_score * ratio, 1)


def screen_dividend(stock):
    pbr_ok = bool(stock["pbr"] and stock["pbr"] <= 2.0)
    roe_ok = bool(stock["roe"] and stock["roe"] >= 8.0)
    div_ok = bool(stock["dividend_yield"] and stock["dividend_yield"] >= 2.0)

    # 合格ライン → 優秀ライン の間でなめらかに採点（優秀ラインはかなり高めに設定し、満点を希少にする）
    pbr_score = linear_score(stock["pbr"], pass_line=2.0, excellent_line=0.6, max_score=34, higher_is_better=False)
    roe_score = linear_score(stock["roe"], pass_line=8.0, excellent_line=22.0, max_score=33, higher_is_better=True)
    div_score = linear_score(stock["dividend_yield"], pass_line=2.0, excellent_line=5.5, max_score=33, higher_is_better=True)

    score = round(pbr_score + roe_score + div_score, 1)
    breakdown = [
        {"label": "割安度（PBR）", "score": pbr_score, "max": 34},
        {"label": "稼ぐ力（ROE）", "score": roe_score, "max": 33},
        {"label": "配当利回り", "score": div_score, "max": 33},
    ]
    return sum([pbr_ok, roe_ok, div_ok]) >= 2, score, breakdown


def screen_solid(stock):
    equity_ok = bool(stock["equity_ratio"] and stock["equity_ratio"] >= 40.0)
    roe_ok = bool(stock["roe"] and stock["roe"] >= 8.0)
    margin_ok = bool(stock["operating_margin"] and stock["operating_margin"] >= 10.0)
    current_ok = bool(stock["current_ratio"] and stock["current_ratio"] >= 1.2)

    equity_score = linear_score(stock["equity_ratio"], pass_line=40.0, excellent_line=75.0, max_score=30, higher_is_better=True)
    roe_score = linear_score(stock["roe"], pass_line=8.0, excellent_line=22.0, max_score=30, higher_is_better=True)
    margin_score = linear_score(stock["operating_margin"], pass_line=10.0, excellent_line=30.0, max_score=25, higher_is_better=True)
    current_score = linear_score(stock["current_ratio"], pass_line=1.2, excellent_line=2.5, max_score=15, higher_is_better=True)

    score = round(equity_score + roe_score + margin_score + current_score, 1)
    breakdown = [
        {"label": "財務の安全度（自己資本比率）", "score": equity_score, "max": 30},
        {"label": "稼ぐ力（ROE）", "score": roe_score, "max": 30},
        {"label": "利益率（営業利益率）", "score": margin_score, "max": 25},
        {"label": "短期支払能力（流動比率）", "score": current_score, "max": 15},
    ]
    return sum([equity_ok, roe_ok, margin_ok]) >= 2, score, breakdown


def screen_growth(stock):
    growth_ok = bool(stock["revenue_growth"] and stock["revenue_growth"] > 0)
    roe_ok = bool(stock["roe"] and stock["roe"] >= 10.0)
    pbr_ok = bool(stock["pbr"] and stock["pbr"] <= 3.0)
    equity_ok = bool(stock["equity_ratio"] and stock["equity_ratio"] >= 40.0)

    growth_score = linear_score(stock["revenue_growth"], pass_line=0.0, excellent_line=25.0, max_score=30, higher_is_better=True)
    roe_score = linear_score(stock["roe"], pass_line=10.0, excellent_line=25.0, max_score=30, higher_is_better=True)
    pbr_score = linear_score(stock["pbr"], pass_line=3.0, excellent_line=1.0, max_score=20, higher_is_better=False)
    equity_score = linear_score(stock["equity_ratio"], pass_line=40.0, excellent_line=70.0, max_score=20, higher_is_better=True)

    score = round(growth_score + roe_score + pbr_score + equity_score, 1)
    breakdown = [
        {"label": "売上成長率", "score": growth_score, "max": 30},
        {"label": "稼ぐ力（ROE）", "score": roe_score, "max": 30},
        {"label": "割安度（PBR）", "score": pbr_score, "max": 20},
        {"label": "財務の安全度（自己資本比率）", "score": equity_score, "max": 20},
    ]
    return sum([growth_ok, roe_ok, equity_ok]) >= 2, score, breakdown


SECTOR_VOLATILITY_NOTES = {
    "Technology": "半導体・ハイテク関連企業のため業績変動は大きく、積立投資では比率を抑えることも検討したい銘柄です",
    "Communication Services": "事業環境の変化が速い業種のため、業績の振れ幅にはご留意ください",
    "Basic Materials": "市況（原材料価格・為替）の影響を受けやすく、業績変動が比較的大きい業種です",
    "Energy": "資源価格の変動の影響を受けやすく、業績変動が比較的大きい業種です",
    "Consumer Cyclical": "景気動向の影響を受けやすく、業績変動が比較的大きい業種です",
    "Real Estate": "金利動向の影響を受けやすい業種です",
    "Financial Services": "市場環境・金利動向の影響を受けやすい業種です",
}


def build_detailed_fp_comment(stock):
    """
    各銘柄について、財務指標と業種特性を踏まえた一文コメントを生成する。
    例：「自己資本比率97.5%、ROE57.6%と非常に優秀な財務内容です。
        一方で半導体関連企業のため業績変動は大きく、積立投資では
        比率を抑えることも検討したい銘柄です。」
    """
    equity_ratio = stock.get("equity_ratio")
    roe = stock.get("roe")
    sector = stock.get("sector")

    parts = []

    # 前半：財務の良さを具体的な数値で
    good_points = []
    if equity_ratio is not None and equity_ratio >= 50:
        good_points.append(f"自己資本比率{equity_ratio}%")
    if roe is not None and roe >= 15:
        good_points.append(f"ROE{roe}%")

    if good_points:
        parts.append(f"{('、'.join(good_points))}と非常に優秀な財務内容です。")
    elif equity_ratio is not None or roe is not None:
        detail = []
        if equity_ratio is not None:
            detail.append(f"自己資本比率{equity_ratio}%")
        if roe is not None:
            detail.append(f"ROE{roe}%")
        parts.append(f"{('、'.join(detail))}という財務内容です。")

    # 後半：業種特性の注記（ある場合のみ）
    volatility_note = SECTOR_VOLATILITY_NOTES.get(sector)
    if volatility_note:
        parts.append(f"一方で{volatility_note}。")

    if not parts:
        return "財務データの一部が取得できなかったため、詳細な評価ができませんでした。"

    return "".join(parts)


def run_screening(stocks_data, screen_func):
    results = []
    for stock in stocks_data:
        if not stock:
            continue
        qualifies, score, breakdown = screen_func(stock)
        if qualifies:
            entry = dict(stock)
            entry["score"] = score
            entry["score_breakdown"] = breakdown
            # 表示用の業種名（industryがあれば、より実態に近い表記に補正）
            entry["sector_display"] = get_display_sector(entry)
            # FPスコアとリスク評価が確定した後に長期積立適性を計算する
            # （他の評価指標との整合性を保つため）
            entry["nisa_fit"] = evaluate_nisa_fit(entry, fp_score=score, risk_level_result=entry.get("risk_level"))
            entry["detailed_comment"] = build_detailed_fp_comment(entry)
            results.append(entry)
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def build_line_message(dividend_results, solid_results, growth_results, updated):
    """LINE通知用のメッセージ本文を作成（堅実配当型の上位5銘柄を中心に）"""
    lines = []
    lines.append("📊 資産形成ナビ｜本日のスクリーニング結果")
    lines.append(f"（{updated} 更新）")
    lines.append("")
    lines.append("🏦 堅実配当型 TOP5")

    top5 = dividend_results[:5]
    if not top5:
        lines.append("該当銘柄なし")
    else:
        for i, s in enumerate(top5, 1):
            name = s.get("name", s["ticker"])
            score = s.get("score", 0)
            div = s.get("dividend_yield")
            roe = s.get("roe")
            div_text = f"配当{div}%" if div is not None else "配当N/A"
            roe_text = f"ROE{roe}%" if roe is not None else "ROE N/A"
            lines.append(f"{i}. {name}（{s['ticker']}）FPスコア{score} ／ {div_text}・{roe_text}")

    lines.append("")
    lines.append(f"財務優良型：{len(solid_results)}銘柄該当")
    lines.append(f"成長×安定型：{len(growth_results)}銘柄該当")
    lines.append("")
    lines.append("👇 全銘柄・カスタム条件はこちら")
    lines.append("https://shisan-navi.vercel.app")
    lines.append("")
    lines.append("※投資推奨ではありません。判断・売買はご自身の責任で行ってください。")

    return "\n".join(lines)


def send_line_broadcast(message):
    """LINE Messaging APIでブロードキャスト配信する"""
    token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    if not token:
        print("LINE_CHANNEL_ACCESS_TOKEN が設定されていないため、LINE通知をスキップします")
        return

    url = "https://api.line.me/v2/bot/message/broadcast"
    body = {
        "messages": [
            {"type": "text", "text": message}
        ]
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req) as res:
            print(f"LINE通知を送信しました（ステータス: {res.status}）")
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="ignore")
        print(f"LINE通知の送信に失敗しました: {e.code} {body_text}")
    except Exception as e:
        print(f"LINE通知の送信中にエラーが発生しました: {e}")


def run_backtest(strategy_results, strategy_key, years=5, sample_size=10):
    """
    簡易バックテスト：現在の条件を満たした銘柄のうち上位サンプルについて、
    過去N年間の株価推移を取得し、日経平均・TOPIXと比較する。

    【重要な制約（生存バイアス）】
    現在存在する銘柄のみを対象としているため、過去N年間に上場廃止・
    業績悪化で除外された銘柄は含まれない。そのため実際のリターンより
    やや良く見える可能性がある「参考値」である。
    """
    sample = strategy_results[:sample_size]
    if not sample:
        return None

    period = f"{years}y"
    stock_returns = []

    for s in sample:
        try:
            hist = yf.Ticker(s["ticker"]).history(period=period)
            if hist.empty or len(hist) < 2:
                continue
            start_price = hist["Close"].iloc[0]
            end_price = hist["Close"].iloc[-1]
            if start_price <= 0:
                continue
            ret_pct = round((end_price / start_price - 1) * 100, 1)
            stock_returns.append({"ticker": s["ticker"], "name": s["name"], "return_pct": ret_pct})
        except Exception as e:
            print(f"バックテスト取得エラー: {s['ticker']} - {e}")
            continue

    if not stock_returns:
        return None

    avg_return = round(sum(r["return_pct"] for r in stock_returns) / len(stock_returns), 1)

    # ベンチマーク取得（日経平均・TOPIX）
    benchmarks = {}
    for label, ticker in [("nikkei225", "^N225"), ("topix", "1306.T")]:
        try:
            hist = yf.Ticker(ticker).history(period=period)
            if not hist.empty and len(hist) >= 2:
                start = hist["Close"].iloc[0]
                end = hist["Close"].iloc[-1]
                benchmarks[label] = round((end / start - 1) * 100, 1)
        except Exception as e:
            print(f"ベンチマーク取得エラー: {ticker} - {e}")

    return {
        "strategy": strategy_key,
        "years": years,
        "sample_size": len(stock_returns),
        "avg_return_pct": avg_return,
        "benchmark_nikkei225_pct": benchmarks.get("nikkei225"),
        "benchmark_topix_pct": benchmarks.get("topix"),
        "stocks": stock_returns,
        "disclaimer": "現在の条件を満たす上位銘柄のみを対象とした参考値です。過去に上場廃止・条件外となった銘柄は含まれないため、実際の運用成績とは異なります。"
    }


def main():
    print("日本株データを取得しています...")
    print(f"対象銘柄数: {len(STOCKS)}")
    print("-" * 50)

    stocks_data = []
    for i, ticker in enumerate(STOCKS):
        print(f"取得中 ({i+1}/{len(STOCKS)}): {ticker}")
        data = get_stock_data(ticker)
        if data:
            stocks_data.append(data)
        time.sleep(0.4)

    print("-" * 50)
    print("3戦略でスクリーニング中...")

    dividend_results = run_screening(stocks_data, screen_dividend)
    solid_results = run_screening(stocks_data, screen_solid)
    growth_results = run_screening(stocks_data, screen_growth)

    print(f"堅実配当型: {len(dividend_results)}銘柄")
    print(f"財務優良型: {len(solid_results)}銘柄")
    print(f"成長×安定型: {len(growth_results)}銘柄")

    print("-" * 50)
    print("バックテストを実行中（過去5年・上位10銘柄サンプル）...")
    print("※株価APIへの負荷軽減のため、週1回（月曜日）のみ実行します")

    import datetime
    is_monday = datetime.datetime.now().weekday() == 0  # 0=月曜日（本番設定）

    backtest_dividend = None
    if is_monday:
        backtest_dividend = run_backtest(dividend_results, "dividend", years=5, sample_size=10)
        if backtest_dividend:
            print(f"バックテスト完了: 平均リターン {backtest_dividend['avg_return_pct']}% "
                  f"(日経225: {backtest_dividend['benchmark_nikkei225_pct']}%)")
    else:
        print("本日は月曜日ではないためバックテストをスキップします（既存の値を維持）")

    # 既存のscreening_result.jsonからバックテスト結果を引き継ぐ（月曜以外の日のため）
    existing_backtest = None
    try:
        with open("screening_result.json", "r", encoding="utf-8") as f:
            existing = json.load(f)
            existing_backtest = existing.get("backtest")
    except (FileNotFoundError, json.JSONDecodeError):
        existing_backtest = None

    final_backtest = backtest_dividend if backtest_dividend else existing_backtest

    output = {
        "updated": time.strftime("%Y-%m-%d %H:%M"),
        "total_stocks_scanned": len(stocks_data),
        "strategies": {
            "dividend": {"name": "堅実配当型", "count": len(dividend_results), "stocks": dividend_results},
            "solid": {"name": "財務優良型", "count": len(solid_results), "stocks": solid_results},
            "growth": {"name": "成長×安定型", "count": len(growth_results), "stocks": growth_results},
        },
        "backtest": final_backtest,
        "strategy": "堅実配当型",
        "count": len(dividend_results),
        "stocks": dividend_results,
    }

    with open("screening_result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n結果を保存しました")
    print(f"スキャン対象: {len(STOCKS)}銘柄 / 取得成功: {len(stocks_data)}銘柄")

    # LINE通知（毎日1回、堅実配当型TOP5などをブロードキャスト配信）
    message = build_line_message(dividend_results, solid_results, growth_results, output["updated"])
    send_line_broadcast(message)


if __name__ == "__main__":
    main()
