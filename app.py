from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = '69420'

@app.route('/')
def main():
    return redirect("/add_items")

@app.route('/add_items', methods=['GET', 'POST'])
def add_items():
    if request.method == 'POST':
        new_item = request.form.get("added_item")
        
        with sqlite3.connect('app.db') as conn:
            if new_item:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO items (item_name) VALUES (?)", (new_item,))
                conn.commit()
        
        return redirect('/add_items')
    
    if request.method == 'GET':
        with sqlite3.connect('app.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM items")
            items = cursor.fetchall()
        
        return render_template("app.html", items=items)

@app.route('/remove_items', methods=['POST'])
def remove_items():
    checked_items = request.form.getlist("items")
    print(checked_items)
    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        for item in checked_items:
            cursor.execute("DELETE FROM items WHERE item_name=?", (item,))
        conn.commit()
    return redirect('/add_items')

@app.route('/edit_item/<string:item_name>', methods=['POST'])
def edit_item(item_name):
    new_item_name = request.form.get("new_item_name")
    old_item_name = request.form.get("old_item_name")
    if not new_item_name:
        return redirect('/add_items')
    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET item_name = ? WHERE item_name = ?", (new_item_name, old_item_name))
        conn.commit()
        
            
    
    return redirect('/add_items')

if __name__ == '__main__':
    app.run(debug=True)
