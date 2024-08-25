from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/index')
def index():
    # Read the CSV file and aggregate items
    aggregated_items = {}
    
    with open('dataset/latest_prices_by_item_and_state.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_name = row['item_name']
            state = row['state']
            price = float(row['latest_price'])
            
            if item_name not in aggregated_items:
                aggregated_items[item_name] = {'latest_price': price, 'States': {}}
            
            # Update the state price
            aggregated_items[item_name]['States'][state] = price

    # Convert aggregated items to a list of dictionaries with sorted states
    processed_items = [
    {
        'item_name': item_name,
        'latest_price': data['latest_price'],
        'state': sorted(data['States'].items(), key=lambda x: x[1])  # Sort states by price
    }
    for item_name, data in aggregated_items.items()
]
    return render_template('index.html', items=processed_items)

@app.route('/item')
def item():
    return render_template('item.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dataset')
def dataset():
    return render_template('dataset.html')

if __name__ == "__main__":
    app.run(debug=True)
