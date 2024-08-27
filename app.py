from flask import Flask, render_template,request
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
    
    # Read the CSV file for percentage increments
    percentage_increments = {}
    with open('dataset/percentage_increments.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Store percentage increments for each item in a dictionary
        for row in reader:
            item_name = row['Item']
            increment = float(row['Percentage Increment'])
            percentage_increments[item_name] = increment

    # Render the HTML page with both processed items and percentage increments
    return render_template('index.html', items=processed_items, increments=percentage_increments)

@app.route('/item')
def item():
    raw_items = []
    processed_items = []

    # Reading data from the CSV file
    with open('dataset/100 raw food list.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            raw_items.append({"name": row['item_name'], "url": "/product/"+row['item_name']+"/Johor"})  # Assuming 'item_name' is the column storing item names

    # Reading data from the CSV file
    with open('dataset/52 processed food list.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            processed_items.append({"name": row['item']})  # Assuming 'item_name' is the column storing item names

    # Get 'show_all' parameters from the query string for both raw and processed items
    raw_food_list_show_all = request.args.get('raw_show_all', 'false') == 'true'
    processed_food_list_show_all = request.args.get('processed_show_all', 'false') == 'true'

    # Check if the raw food list should show all items or only the first 9
    if raw_food_list_show_all:
        limited_raw_items = raw_items  # Show all raw items
    else:
        limited_raw_items = raw_items[:9]  # Limit to the first 9 raw items

    # Check if the processed food list should show all items or only the first 9
    if processed_food_list_show_all:
        limited_processed_items = processed_items  # Show all processed items
    else:
        limited_processed_items = processed_items[:9]  # Limit to the first 9 processed items

    # Pass the relevant data to the template
    return render_template(
        'item.html',
        raw_items=limited_raw_items,
        processed_items=limited_processed_items,
        raw_show_all=raw_food_list_show_all,
        processed_show_all=processed_food_list_show_all
    )


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dataset')
def dataset():
    return render_template('dataset.html')

@app.route('/product/<food_item>/<state>')
def product_details(food_item, state):
    # Example data retrieval from database or API
    product_data = get_product_data(food_item, state)
    
    return render_template('product.html', product=product_data)
    
def get_product_data(food_item, state):
    # Example logic to retrieve product details for the selected item and state
    return {
        'name': food_item,
        'state': state,
        'price': 'RM 8.24',
        'price_change': '+12%',
        'highest_price': 'RM 11.64',
        'lowest_price': 'RM 6.61',
        'unusual_prices': [
            {'date': '10/01/2020', 'price': '50.32'},
            {'date': '15/01/2020', 'price': '48.89'},
        ],
        'future_trend_chart': f'predict_future_trend_{state.lower()}.png',
        'unusual_trend_chart1': f'detect_unusual_trend1_{state.lower()}.png',
        'unusual_trend_chart2': f'detect_unusual_trend2_{state.lower()}.png',
        'price_comparison_chart': f'price_comparison_across_states_{state.lower()}.png',
    }

if __name__ == "__main__":
    app.run(debug=True)
