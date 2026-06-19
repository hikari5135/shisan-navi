import yfinance as yf
import json
import time
import os

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
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        pbr = info.get("priceToBook", None)
        roe = info.get("returnOnEquity", None)
        div = info.get("dividendYield", None)
        
        if div:
            if div > 1:
                div_pct = round(div, 2)
            else:
                div_pct = round(div * 100, 2)
        else:
            div_pct = None

        data = {
            "ticker": ticker,
            "name": info.get("longName", ticker),
            "sector": info.get("sector", "不明"),
            "price": info.get("currentPrice", 0),
            "pbr": round(pbr, 2) if pbr else None,
            "roe": round(roe * 100, 2) if roe else None,
            "dividend_yield": div_pct,
            "market_cap": info.get("marketCap", 0),
        }
        return data
    except Exception as e:
        print(f"エラー: {ticker} - {e}")
        return None

def screening(stocks_data):
    results = []
    
    for stock in stocks_data:
        if not stock:
            continue
        
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
        
        stock["score"] = score
        
        if sum([pbr_ok, roe_ok, div_ok]) >= 2:
            results.append(stock)
    
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def main():
    print("日本株スクリーニングを開始します...")
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
    print("スクリーニング実行中...")
    
    results = screening(stocks_data)
    
    print(f"\n【堅実配当型スクリーニング結果】")
    print(f"該当銘柄数: {len(results)}")
    print("-" * 50)
    
    for stock in results:
        print(f"\n{stock['name']} ({stock['ticker']})")
        print(f"  FPスコア: {stock['score']}/100")
        print(f"  PBR: {stock['pbr']}倍")
        print(f"  ROE: {stock['roe']}%")
        print(f"  配当利回り: {stock['dividend_yield']}%")
    
    output = {
        "updated": time.strftime("%Y-%m-%d %H:%M"),
        "strategy": "堅実配当型",
        "count": len(results),
        "stocks": results
    }
    
    output_path = "screening_result.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n結果を保存しました: {output_path}")

if __name__ == "__main__":
    main()