import yfinance as yf
import json
import time

STOCKS = [
    "4452.T",  # 花王
    "9432.T",  # NTT
    "9433.T",  # KDDI
    "8593.T",  # 三菱HCキャピタル
    "4063.T",  # 信越化学
    "7974.T",  # 任天堂
    "6758.T",  # ソニー
    "4502.T",  # 武田薬品
    "8306.T",  # 三菱UFJ
    "8316.T",  # 三井住友FG
    "7203.T",  # トヨタ
    "6861.T",  # キーエンス
    "4519.T",  # 中外製薬
    "8035.T",  # 東京エレクトロン
    "6367.T",  # ダイキン
    "9984.T",  # ソフトバンクG
    "6954.T",  # ファナック
    "4568.T",  # 第一三共
    "7751.T",  # キヤノン
    "8058.T",  # 三菱商事
]


def get_stock_data(ticker):
    """yfinanceから財務指標を取得"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        pbr = info.get("priceToBook", None)
        roe = info.get("returnOnEquity", None)
        div = info.get("dividendYield", None)
        debt_to_equity = info.get("debtToEquity", None)  # 負債資本比率(%)
        operating_margin = info.get("operatingMargins", None)  # 営業利益率
        revenue_growth = info.get("revenueGrowth", None)  # 売上成長率(前年比)
        current_ratio = info.get("currentRatio", None)  # 流動比率

        # 配当利回りの正規化（1超ならすでに%、それ以外は100倍）
        if div:
            div_pct = round(div, 2) if div > 1 else round(div * 100, 2)
        else:
            div_pct = None

        # 自己資本比率の簡易推定
        # debtToEquity(%) から逆算: 自己資本比率 ≈ 100 / (1 + D/E/100)
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
    """堅実配当型: 配当利回り3%以上・PBR1.5倍以下・ROE8%以上"""
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
    """財務優良型: 自己資本比率高め・ROE8%以上・営業利益率10%以上"""
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
    """成長×安定型: 売上成長・ROE10%以上・PBR1.5倍以下・自己資本比率40%以上"""
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
        # 後方互換のため従来形式も残す（堅実配当型のみ）
        "strategy": "堅実配当型",
        "count": len(dividend_results),
        "stocks": dividend_results,
    }

    output_path = "screening_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n結果を保存しました: {output_path}")


if __name__ == "__main__":
    main()
