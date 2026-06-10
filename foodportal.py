import mysql.connector as sqlconnector
import mysql.connector 

# --- DB Connection ---
try:
    d = sqlconnector.connect(
        host="localhost",
        user="fooduser",
        password="food123",
        database="food"
    )
    e = d.cursor()
except mysql.connector.Error as err:  
    print(f"Error: {err}")
    exit()                            

# ─────────────────────────── HELPERS ────────────────────────────────────────
 
def print_line(char="─", width=72):
    print(char * width)
 
def print_menu_table(rows):
    """Pretty-print the item table with aligned columns."""
    # Column widths
    W = {"id": 4, "name": 32, "category": 16, "price": 8, "veg": 5}
    sep = (f"┌{'─'*(W['id']+2)}┬{'─'*(W['name']+2)}┬"
           f"{'─'*(W['category']+2)}┬{'─'*(W['price']+2)}┬{'─'*(W['veg']+2)}┐")
    mid = sep.replace("┌","├").replace("┐","┤").replace("─","─")
    bot = sep.replace("┌","└").replace("┐","┘")
 
    header = (f"│ {'ID':<{W['id']}} │ {'Name':<{W['name']}} │"
              f" {'Cuisine':<{W['category']}} │ {'Price':>{W['price']}} │"
              f" {'Veg?':<{W['veg']}} │")
 
    print(sep)
    print(header)
    print(mid)
 
    last_cat = None
    for row in rows:
        s_no, name, category, price, desc, is_veg = row
        # Print a subtle divider between cuisines
        if last_cat and category != last_cat:
            print(mid)
        last_cat = category
 
        veg_tag  = " ✓   " if is_veg else "     "
        name_str = name[:W['name']]          # truncate if too long
        cat_str  = category[:W['category']]
        price_str = f"₹{price:.0f}"
 
        print(f"│ {s_no:<{W['id']}} │ {name_str:<{W['name']}} │"
              f" {cat_str:<{W['category']}} │ {price_str:>{W['price']}} │"
              f" {veg_tag:<{W['veg']}} │")
 
    print(bot)
 

# ─────────────────────────── ADMIN FUNCTIONS ────────────────────────────────

def add_food():
    try:
        ser = int(input("Enter the Food ID: "))
        fi  = input("Enter the Food name: ")
        fp  = int(input("Enter the Price of Food: "))
        ft  = input("Enter the Food Type: ")

        query = "INSERT INTO item (S_no, Name, Price, Category) VALUES (%s, %s, %s, %s)"
        e.execute(query, (ser, fi, fp, ft))
        d.commit()
        print("NEW FOOD ADDED SUCCESSFULLY")
    except Exception as err:
        print(f"Error adding food: {err}")


def update_food():
    print("\n1. Update food name")
    print("2. Update food price")
    try:
        us = int(input("Enter your choice: "))
        if us == 1:
            fnid = int(input("Enter the Food ID to update: "))
            fna  = input("Enter the updated Food Name: ")
            e.execute("UPDATE item SET Name = %s WHERE S_no = %s", (fna, fnid))
        elif us == 2:
            fnic = int(input("Enter the Food ID to update: "))
            fnf  = int(input("Enter the updated Food Price: "))
            e.execute("UPDATE item SET Price = %s WHERE S_no = %s", (fnf, fnic))
        else:
            print("Invalid choice.")
            return
        d.commit()
        print("UPDATED SUCCESSFULLY")
    except Exception as err:
        print(f"Error updating: {err}")


def delete_food():
    try:
        fidd = int(input("Enter the Food ID you want to delete: "))
        e.execute("DELETE FROM item WHERE S_no = %s", (fidd,))
        d.commit()
        print("FOOD ITEM DELETED SUCCESSFULLY")
    except Exception as err:
        print(f"Error: {err}")


def view_orders():
    print("\nDetails of all orders are:")
    e.execute("SELECT * FROM orders")
    rtt = e.fetchall()
    if not rtt:
        print("No orders found.")
        return
    for i in rtt:
        print("*" * 30)
        print(f"Order ID : {i[0]}")
        print(f"Food     : {i[2]}")
        print(f"Qty      : {i[3]}")
        print(f"Unit Price: ₹{i[4]}")
        print(f"Total    : {i[5]}")
        print(f"Phone    : {i[6]}")
        print(f"Address  : {i[7]}")
    print("*" * 30)


def ad_login():
    while True:
        print("\n--- ADMIN PANEL ---")
        print("1. Add food\n2. Update food\n3. Delete food\n4. View orders\n5. Logout")
        try:
            ask = int(input("Enter choice: "))
            if   ask == 1: add_food()
            elif ask == 2: update_food()
            elif ask == 3: delete_food()
            elif ask == 4: view_orders()
            elif ask == 5: break
            else: print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")


def ad_panel():
    pas = input("Enter Admin Password: ")
    if pas == 'FoodieIsGreat':
        print("Access granted")
        ad_login()
    else:
        print("Wrong Password! Access Denied.")


# ─────────────────────────── CUSTOMER FUNCTIONS ─────────────────────────────

def show_menu():
    e.execute("SELECT S_no, Name, Category, Price, Description, Is_Veg FROM item ORDER BY Category, Price")
    w = e.fetchall()
    if not w:
        print("Menu is currently empty.")
        return
    print("\n" + "=" * 72)
    print("        INTERNATIONAL RESTAURANT — TODAY'S MENU")
    print("=" * 72)
    print_menu_table(w)
    print("  [v] = Vegetarian\n")

    ui = input("\nDo you want to order food (Yes/No)? ")
    if ui.lower() == "yes":
        F_order()


def F_order():
    try:
        io  = int(input("Enter the Food ID: "))
        e.execute("SELECT Name, Price FROM item WHERE S_no = %s", (io,))
        item = e.fetchone()

        if item:
            iname, iprice = item[0], item[1]
            qty = int(input("Enter Quantity: "))
            phn = input("Enter Phone No: ")
            adr = input("Enter Address: ")

            oprice = iprice * qty
            query  = ("INSERT INTO orders(S_no, F_name, Quantity, Unit_price, Total, P_no, Address) "
                      "VALUES(%s, %s, %s, %s, %s, %s, %s)")
            e.execute(query, (io, iname, qty, float(iprice), float(oprice), phn, adr))
            d.commit()

            print("\n******** BILL ********")
            print(f"Food       : {iname}")
            print(f"Unit Price : ₹{iprice}")
            print(f"Qty        : {qty}")
            print(f"Total      : ₹{oprice}")
            print(f"Address    : {adr}")
            print("********************\nOrder Confirmed!")
        else:
            print("Item not found in menu.")
    except ValueError:
        print("Invalid input. Please enter numeric values where required.")
    except Exception as err:
        print(f"Order failed: {err}")


def F_View():
    yno = input("Enter your registered phone No: ")
    e.execute("SELECT F_name, Total, Address FROM orders WHERE P_no = %s", (yno,))
    rt = e.fetchall()
    if rt:
        print("\n--- YOUR RECENT ORDERS ---")
        for i in rt:
            print(f"Food: {i[0]} | Total: ₹{i[1]} | Address: {i[2]}")
    else:
        print("No orders found for this number.")


def F_Cancel():
    cor = input("Enter phone No to cancel order: ")
    e.execute("SELECT * FROM orders WHERE P_no = %s", (cor,))
    existing = e.fetchall()           
    if not existing:
        print("No orders found for that number.")
        return
    confirm = input(f"Found {len(existing)} order(s). Confirm cancel? (yes/no): ")
    if confirm.lower() == "yes":
        e.execute("DELETE FROM orders WHERE P_no = %s", (cor,))
        d.commit()
        print("Order(s) cancelled successfully.")
    else:
        print("Cancellation aborted.")


def F_feedb():
    fdb = input("Enter Phone No: ")
    fdc = input("Give us Feedback: ")
    e.execute("INSERT INTO feedback(P_no, Comments) VALUES(%s, %s)", (fdb, fdc))
    d.commit()
    print("THANKS FOR YOUR FEEDBACK")


# ─────────────────────────── MENUS ──────────────────────────────────────────

def main_menu():
    while True:
        print("\n--- CUSTOMER PORTAL ---")
        print("1. View Menu\n2. Place Order\n3. View Order Status\n4. Cancel Order\n5. Feedback\n6. Back to Home")
        try:
            a = int(input("Enter choice: "))
            if   a == 1: show_menu()
            elif a == 2: F_order()
            elif a == 3: F_View()
            elif a == 4: F_Cancel()
            elif a == 5: F_feedb()
            elif a == 6: break
            else: print("Enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input.")


def homepage():
    while True:
        print("\n" + "=" * 30)
        print("   WELCOME TO FOOD PORTAL")
        print("=" * 30)
        print("1. Admin Login\n2. Customer Portal\n3. EXIT")
        try:
            op = int(input("Enter option: "))
            if   op == 1: ad_panel()
            elif op == 2: main_menu()
            elif op == 3:
                print("Exiting... Goodbye!")
                d.close()            
                break
            else: print("Select 1, 2, or 3.")
        except ValueError:
            print("Select 1, 2, or 3.")


if __name__ == "__main__":
    homepage()
