import yfinance as yf
import json
import time

# 業種バランスを意識した75銘柄
STOCKS = [
    # 通信
    "9432.T",  # NTT
    "9433.T",  # KDDI
    "9434.T",  # ソフトバンク

    # 金融
    "8306.T",  # 三菱UFJ
    "8316.T",  # 三井住友FG
    "8411.T",  # みずほFG
    "8766.T",  # 東京海上HD
    "8591.T",  # オリックス
    "8593.T",  # 三菱HCキャピタル
    "8604.T",  # 野村HD
    "8630.T",  # SOMPOHD

    # 商社
    "8058.T",  # 三菱商事
    "8001.T",  # 伊藤忠商事
    "8031.T",  # 三井物産
    "8053.T",  # 住友商事
    "2768.T",  # 双日

    # 自動車・輸送機器
    "7203.T",  # トヨタ
    "7267.T",  # ホンダ
    "7201.T",  # 日産自動車
    "6902.T",  # デンソー
    "7211.T",  # 三菱自動車
    "7269.T",  # スズキ

    # 電機・精密機器
    "6758.T",  # ソニー
    "6861.T",  # キーエンス
    "6954.T",  # ファナック
    "7751.T",  # キヤノン
    "6981.T",  # 村田製作所
    "6594.T",  # ニデック
    "6503.T",  # 三菱電機
    "6501.T",  # 日立製作所

    # 化学・素材
    "4063.T",  # 信越化学
    "4452.T",  # 花王
    "3407.T",  # 旭化成
    "4901.T",  # 富士フイルム
    "4188.T",  # 三菱ケミカルグループ
    "5713.T",  # 住友金属鉱山

    # 医薬品
    "4502.T",  # 武田薬品
    "4519.T",  # 中外製薬
    "4568.T",  # 第一三共
    "4523.T",  # エーザイ
    "4151.T",  # 協和キリン

    # 半導体・電子部品
    "8035.T",  # 東京エレクトロン
    "6723.T",  # ルネサスエレクトロニクス
    "6857.T",  # アドバンテスト
    "6920.T",  # レーザーテック

    # 小売・サービス
    "9983.T",  # ファーストリテイリング
    "3382.T",  # セブン&アイHD
    "9984.T",  # ソフトバンクG
    "8267.T",  # イオン
    "9843.T",  # ニトリHD

    # 食品
    "2502.T",  # アサヒグループHD
    "2914.T",  # JT
    "2503.T",  # キリンHD
    "2801.T",  # キッコーマン

    # 不動産
    "8801.T",  # 三井不動産
    "8802.T",  # 三菱地所
    "8830.T",  # 住友不動産

    # 鉄道・運輸
    "9020.T",  # JR東日本
    "9022.T",  # JR東海
    "9021.T",  # JR西日本
    "9201.T",  # 日本航空

    # 機械・空調
    "6367.T",  # ダイキン
    "6301.T",  # コマツ
    "6326.T",  # クボタ

    # ゲーム・エンタメ
    "7974.T",  # 任天堂
    "9697.T",  # カプコン
    "9602.T",  # 東宝

    # 建設
    "1801.T",  # 大成建設
    "1812.T",  # 鹿島建設

    # 電力・インフラ
    "9501.T",  # 東京電力HD
    "9503.T",  # 関西電力

    # 鉄鋼
    "5401.T",  # 日本製鉄
    "5411.T",  # JFEHD

    # 情報・通信サービス
    "4661.T",  # オリエンタルランド
    "4385.T",  # メルカリ
    "4307.T",  # ノムラシステムコーポレーション
]

def get_stock_data(ticker):
    """yfinanceから財務指標を取得"""
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

        if div:
            div_pct = round(div, 2) if div > 1 else round(div * 100, 2)
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
            "price": info.get("currentPrice", 0),
            "pbr": round(pbr, 2) if pbr else None,
            "roe": round(roe * 100, 2) if roe else None,
            "dividend_yield": div_pct,
            "equity_ratio": equity_ratio,
            "operating_margin": round(operating_margin * 100, 2) if operating_margin else None,
            "revenue_growth": round(revenue_growth * 100, 2) if revenue_growth else None,
            "current_ratio": round(current_ratio, 2) if current_ratio else None,
            "market_cap": info.get("marketCap", 0),
        }
        return data
    except Exception as e:
        print(f"エラー: {ticker} - {e}")
        return None


def screen_dividend(stock):
    pbr_ok = bool(stock["pbr"] and stock["pbr"] <= 2.0)
    roe_ok = bool(stock["roe"] and stock["roe"] >= 8.0)
    div_ok = bool(stock["dividend_yield"] and stock["dividend_yield"] >= 2.0)

    score = 0
    if pbr_ok:
        score += 30
        if stock["pbr"] <= 1.5:
            score += 10
    if roe_ok:
        score += 30
        if stock["roe"] >= 12:
            score += 10
    if div_ok:
        score += 30
        if stock["dividend_yield"] >= 3.0:
            score += 10

    qualifies = sum([pbr_ok, roe_ok, div_ok]) >= 2
    return qualifies, score


def screen_solid(stock):
    equity_ok = bool(stock["equity_ratio"] and stock["equity_ratio"] >= 40.0)
    roe_ok = bool(stock["roe"] and stock["roe"] >= 8.0)
    margin_ok = bool(stock["operating_margin"] and stock["operating_margin"] >= 10.0)
    current_ok = bool(stock["current_ratio"] and stock["current_ratio"] >= 1.2)

    score = 0
    if equity_ok:
        score += 25
        if stock["equity_ratio"] >= 55:
            score += 10
    if roe_ok:
        score += 25
        if stock["roe"] >= 12:
            score += 10
    if margin_ok:
        score += 25
        if stock["operating_margin"] >= 15:
            score += 5
    if current_ok:
        score += 25

    qualifies = sum([equity_ok, roe_ok, margin_ok]) >= 2
    return qualifies, score


def screen_growth(stock):
    growth_ok = bool(stock["revenue_growth"] and stock["revenue_growth"] > 0)
    roe_ok = bool(stock["roe"] and stock["roe"] >= 10.0)
    pbr_ok = bool(stock["pbr"] and stock["pbr"] <= 3.0)
    equity_ok = bool(stock["equity_ratio"] and stock["equity_ratio"] >= 40.0)

    score = 0
    if growth_ok:
        score += 25
        if stock["revenue_growth"] >= 10:
            score += 10
    if roe_ok:
        score += 25
        if stock["roe"] >= 15:
            score += 10
    if pbr_ok:
        score += 25
    if equity_ok:
        score += 25

    qualifies = sum([growth_ok, roe_ok, equity_ok]) >= 2
    return qualifies, score


def run_screening(stocks_data, screen_func):
    results = []
    for stock in stocks_data:
        if not stock:
            continue
        qualifies, score = screen_func(stock)
        if qualifies:
            entry = dict(stock)
            entry["score"] = score
            results.append(entry)
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


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
        time.sleep(0.5)

    print("-" * 50)
    print("3戦略でスクリーニング中...")

    dividend_results = run_screening(stocks_data, screen_dividend)
    solid_results = run_screening(stocks_data, screen_solid)
    growth_results = run_screening(stocks_data, screen_growth)

    print(f"堅実配当型: {len(dividend_results)}銘柄")
    print(f"財務優良型: {len(solid_results)}銘柄")
    print(f"成長×安定型: {len(growth_results)}銘柄")

    output = {
        "updated": time.strftime("%Y-%m-%d %H:%M"),
        "total_stocks_scanned": len(stocks_data),
        "strategies": {
            "dividend": {
                "name": "堅実配当型",
                "count": len(dividend_results),
                "stocks": dividend_results,
            },
            "solid": {
                "name": "財務優良型",
                "count": len(solid_results),
                "stocks": solid_results,
            },
            "growth": {
                "name": "成長×安定型",
                "count": len(growth_results),
                "stocks": growth_results,
            },
        },
        "strategy": "堅実配当型",
        "count": len(dividend_results),
        "stocks": dividend_results,
    }

    output_path = "screening_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n結果を保存しました: {output_path}")
    print(f"スキャン対象: {len(STOCKS)}銘柄 / 取得成功: {len(stocks_data)}銘柄")


if __name__ == "__main__":
    main()
