

# Global Palate Engine 🌍

A high-performance, scalable Restaurant Management System designed for multi-cuisine environments. This application provides an end-to-end solution for both customers (browsing and ordering) and administrators (inventory and order fulfillment), powered by Python Flask and TiDB Cloud.

## 🚀 Overview

The Global Palate Engine is built to handle the complexities of a 60+ dish menu across 12 unique cuisines. It leverages ACID-compliant database transactions to ensure order integrity and a responsive, Tailwind-CSS-driven dashboard for real-time administrative operations.

---

## 🛠 Tech Stack

* **Backend:** Python (Flask)
* **Database:** TiDB (Distributed SQL, MySQL-compatible)
* **Frontend:** HTML5, Tailwind CSS
* **Deployment:** Vercel (Serverless Functions)

---

## 📂 Project Architecture

### Backend (`app.py`)

The central controller managing all routing and data operations.

* **Customer Controllers:** Handles `/menu` retrieval, `/order` creation, and `/feedback` submission.
* **Admin Controllers:** Secure management routes (`/admin/dashboard`) including `web_add_food`, `web_update_food`, and `web_delete_food` to maintain the menu catalog.
* **Order Fulfillment:** Logic for real-time order tracking and the `complete_order` function to update the fulfillment queue.

### Frontend (`/templates`)

* **`admin_dashboard.html`:** The core control center. Features a reactive search bar for catalog filtering and administrative CRUD controls.
* **`menu.html`:** Optimized for customer interaction with intuitive browsing.

---

## 🗄 Database Schema

The system utilizes a relational model to ensure data consistency.

| Table | Purpose |
| --- | --- |
| `item` | Master catalog of dishes (Price, Category, Description, Is_Veg). |
| `orders` | Transactional data linking customers (Phone) to items via Foreign Key (`S_no`). |
| `feedback` | Customer sentiment tracking and rating system. |

---

## ⚙️ Key Features

* **Dynamic Inventory:** Admin tools to add/edit/delete dishes in real-time.
* **Searchable Catalog:** Client-side JS implementation for sub-millisecond filtering of the menu catalog.
* **Fulfillment System:** "Mark as Done" functionality that triggers atomic database deletions, ensuring the order queue remains accurate.
* **Scalability:** Built on TiDB, ensuring that as your restaurant data grows, your query performance remains stable and consistent.

---

## 🚀 Setup & Installation

### Environment Variables

To secure your production build, ensure the following variables are configured in your environment:

* `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`: Your TiDB cloud credentials.
* `ADMIN_USERNAME`, `ADMIN_PASSWORD`: Credentials for the Admin Workspace.
* `SECRET_KEY`: For Flask session management.

### Deployment

This repository is optimized for Vercel. Ensure your `vercel.json` is configured to route traffic to `api/index.py` for optimal performance.



---

**Does this structure work for you? If you need me to adjust the "Why" section or add a specific section about scaling, just let me know!**
