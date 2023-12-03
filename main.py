from engines.engines_chain import EnginesChain
from item import Item
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_data(item_id):
    item_info = Item(item_id)
    print(item_info)
    final_result = EnginesChain().validate_item(item_info)
    print(f'Result Score: {final_result}')
    return final_result, item_info


@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    try:
        result, item_info = get_data(item_id)
        return jsonify({'success': True, 'score': result[0], 'reasons': result[1], 'info': str(item_info)})
    except Exception as e:
        return jsonify({'success': False, 'message': f'{e}'})


if __name__ == '__main__':
    app.run(debug=True, port=8080)
