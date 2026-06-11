import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
import pymysql.cursors

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_development_key')

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME", "food"),
        port=int(os.environ.get("DB_PORT", 4000)),
        ssl={'ssl': {}} 
    )

# ─────────────────────────── CUSTOMER CONTROLLERS ───────────────────────────

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT S_no, Name, Category, Price, Description, Is_Veg FROM item ORDER BY Category, Price")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('menu.html', items=items)

@app.route('/order/<int:item_id>', methods=['GET', 'POST'])
def place_order(item_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute("SELECT * FROM item WHERE S_no = %s", (item_id,))
    item = cursor.fetchone()
    
    if request.method == 'POST':
        qty = int(request.form['quantity'])
        phone = request.form['phone']
        address = request.form['address']
        total_price = float(item['Price']) * qty
        
        query = """INSERT INTO orders (S_no, F_name, Quantity, Unit_price, Total, P_no, Address) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (item['S_no'], item['Name'], qty, item['Price'], total_price, phone, address)
        
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        
        flash(f"Order Confirmed! Food: {item['Name']} | Total: ₹{total_price:.2f}", "success")
        return redirect(url_for('menu'))
        
    cursor.close()
    conn.close()
    return render_template('order.html', item=item)

@app.route('/status', methods=['GET', 'POST'])
def order_status():
    orders = None
    phone = None
    if request.method == 'POST':
        phone = request.form['phone']
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT F_name, Total, Address FROM orders WHERE P_no = %s", (phone,))
        orders = cursor.fetchall()
        cursor.close()
        conn.close()
        if not orders:
            flash("No orders found for this number.", "info")
            
    return render_template('status.html', orders=orders, phone=phone)

@app.route('/cancel', methods=['POST'])
def cancel_order():
    phone = request.form['phone']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM orders WHERE P_no = %s", (phone,))
    existing = cursor.fetchall()
    
    if existing:
        cursor.execute("DELETE FROM orders WHERE P_no = %s", (phone,))
        conn.commit()
        flash(f"Successfully cancelled {len(existing)} order(s).", "success")
    else:
        flash("No orders found to cancel.", "error")
        
    cursor.close()
    conn.close()
    return redirect(url_for('order_status'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        phone = request.form['phone']
        comments = request.form['comments']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback(P_no, Comments) VALUES(%s, %s)", (phone, comments))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash("Thank you for your valuable feedback!", "success")
        return redirect(url_for('home'))
        
    return render_template('feedback.html')

# ─────────────────────────── ADMIN CONTROLLERS ───────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        expected_user = os.environ.get('ADMIN_USERNAME', 'admin')
        expected_pass = os.environ.get('ADMIN_PASSWORD')
        
        if expected_pass and username == expected_user and password == expected_pass:
            session['admin_logged_in'] = True
            flash("Access granted. Welcome to Admin Panel.", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Wrong Username or Password! Access Denied.", "error")
            
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        flash("Please log in first.", "error")
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute("SELECT * FROM orders ORDER BY O_id DESC")
    orders = cursor.fetchall()
    
    cursor.execute("SELECT * FROM item ORDER BY Category, S_no")
    items = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('admin_dashboard.html', orders=orders, items=items)

@app.route('/admin/add', methods=['POST'])
def web_add_food():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    
    ser = int(request.form['s_no'])
    fi = request.form['name']
    fp = float(request.form['price'])
    ft = request.form['category']
    desc = request.form.get('description', '')
    is_veg = 1 if request.form.get('is_veg') else 0
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO item (S_no, Name, Price, Category, Description, Is_Veg) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (ser, fi, fp, ft, desc, is_veg))
        conn.commit()
        flash("NEW FOOD ITEM ADDED SUCCESSFULLY", "success")
    except Exception as err:
        flash(f"Error: {err}", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update/<int:item_id>', methods=['POST'])
def web_update_food(item_id):
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    
    name = request.form['name']
    price = float(request.form['price'])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE item SET Name = %s, Price = %s WHERE S_no = %s", (name, price, item_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("FOOD ITEM UPDATED SUCCESSFULLY", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<int:item_id>')
def web_delete_food(item_id):
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM item WHERE S_no = %s", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("FOOD ITEM DELETED SUCCESSFULLY", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/order/complete/<int:order_id>', methods=['POST'])
def complete_order(order_id):
    
    conn = get_db_connection() 
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM orders WHERE O_id = %s", (order_id,))
        conn.commit()
    except Exception as e:
        print(f"Error completing order: {e}")
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=8080)
