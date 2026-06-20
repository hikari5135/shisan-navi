import yfinance as yf
import json
import time

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
]

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
        if stock["pbr"] <= 1.5: score += 10
    if roe_ok:
        score += 30
        if stock["roe"] >= 12: score += 10
    if div_ok:
        score += 30
        if stock["dividend_yield"] >= 3.0: score += 10
    return sum([pbr_ok, roe_ok, div_ok]) >= 2, score


def screen_solid(stock):
    equity_ok = bool(stock["equity_ratio"] and stock["equity_ratio"] >= 40.0)
    roe_ok = bool(stock["roe"] and stock["roe"] >= 8.0)
    margin_ok = bool(stock["operating_margin"] and stock["operating_margin"] >= 10.0)
    current_ok = bool(stock["current_ratio"] and stock["current_ratio"] >= 1.2)
    score = 0
    if equity_ok:
        score += 25
        if stock["equity_ratio"] >= 55: score += 10
    if roe_ok:
        score += 25
        if stock["roe"] >= 12: score += 10
    if margin_ok:
        score += 25
        if stock["operating_margin"] >= 15: score += 5
    if current_ok:
        score += 25
    return sum([equity_ok, roe_ok, margin_ok]) >= 2, score


def screen_growth(stock):
    growth_ok = bool(stock["revenue_growth"] and stock["revenue_growth"] > 0)
    roe_ok = bool(stock["roe"] and stock["roe"] >= 10.0)
    pbr_ok = bool(stock["pbr"] and stock["pbr"] <= 3.0)
    equity_ok = bool(stock["equity_ratio"] and stock["equity_ratio"] >= 40.0)
    score = 0
    if growth_ok:
        score += 25
        if stock["revenue_growth"] >= 10: score += 10
    if roe_ok:
        score += 25
        if stock["roe"] >= 15: score += 10
    if pbr_ok:
        score += 25
    if equity_ok:
        score += 25
    return sum([growth_ok, roe_ok, equity_ok]) >= 2, score


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
        time.sleep(0.4)

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
            "dividend": {"name": "堅実配当型", "count": len(dividend_results), "stocks": dividend_results},
            "solid": {"name": "財務優良型", "count": len(solid_results), "stocks": solid_results},
            "growth": {"name": "成長×安定型", "count": len(growth_results), "stocks": growth_results},
        },
        "strategy": "堅実配当型",
        "count": len(dividend_results),
        "stocks": dividend_results,
    }

    with open("screening_result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n結果を保存しました")
    print(f"スキャン対象: {len(STOCKS)}銘柄 / 取得成功: {len(stocks_data)}銘柄")


if __name__ == "__main__":
    main()
