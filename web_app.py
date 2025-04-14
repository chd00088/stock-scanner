from flask import Flask, request, jsonify, render_template
from stock_analyzer import StockAnalyzer
from 全部股票分析推荐1 import TopStockScanner  # 导入推荐的扫描器模块
import os

app = Flask(__name__)
analyzer = StockAnalyzer()
scanner = TopStockScanner(max_workers=20, min_score=85)  # 初始化扫描器

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        stock_code = data.get('stock_code')
        if not stock_code:
            return jsonify({'error': '请提供股票代码'}), 400

        result = analyzer.analyze_stock(stock_code)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    try:
        data = request.json
        stock_list = data.get('stock_list', [])
        if not stock_list:
            return jsonify({'error': '请提供股票代码列表'}), 400

        results = analyzer.scan_market(stock_list)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 新增的路由：全部股票分析
@app.route('/api/all-stocks-analysis', methods=['GET'])
def all_stocks_analysis():
    try:
        # 调用 TopStockScanner 的方法获取高评分股票分析结果
        results = scanner.get_high_score_stocks(batch_size=20)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
