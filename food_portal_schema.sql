-- ============================================================
--  INTERNATIONAL RESTAURANT — MySQL Schema + Seed Data
--  Tables: item, orders, feedback
-- ============================================================

DROP DATABASE IF EXISTS food;
CREATE DATABASE food CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE food;

-- ------------------------------------------------------------
-- 1. MENU TABLE
-- ------------------------------------------------------------
CREATE TABLE item (
    S_no        INT             NOT NULL AUTO_INCREMENT,
    Name        VARCHAR(100)    NOT NULL,
    Category    VARCHAR(60)     NOT NULL,   -- cuisine / type
    Price       DECIMAL(8,2)    NOT NULL,
    Description VARCHAR(255),
    Is_Veg      TINYINT(1)      NOT NULL DEFAULT 0,  -- 1 = veg, 0 = non-veg
    PRIMARY KEY (S_no)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 2. ORDERS TABLE
-- ------------------------------------------------------------
CREATE TABLE orders (
    O_id        INT             NOT NULL AUTO_INCREMENT,
    S_no        INT             NOT NULL,
    F_name      VARCHAR(100)    NOT NULL,
    Quantity    INT             NOT NULL DEFAULT 1,
    Unit_price  DECIMAL(8,2)    NOT NULL,
    Total       DECIMAL(10,2)   NOT NULL,
    P_no        VARCHAR(15)     NOT NULL,
    Address     VARCHAR(255)    NOT NULL,
    Order_time  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (O_id),
    INDEX idx_orders_phone (P_no),
    FOREIGN KEY (S_no) REFERENCES item(S_no) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 3. FEEDBACK TABLE
-- ------------------------------------------------------------
CREATE TABLE feedback (
    F_id        INT             NOT NULL AUTO_INCREMENT,
    P_no        VARCHAR(15)     NOT NULL,
    Comments    TEXT,
    Rating      TINYINT         CHECK (Rating BETWEEN 1 AND 5),
    Fb_time     DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (F_id),
    INDEX idx_feedback_phone (P_no)
) ENGINE=InnoDB;

-- ============================================================
--  SEED DATA — 60 dishes across 12 world cuisines
-- ============================================================
INSERT INTO item (Name, Category, Price, Description, Is_Veg) VALUES

-- ── INDIAN ──────────────────────────────────────────────────
('Butter Chicken',          'Indian',       320.00, 'Tender chicken in rich tomato-cream sauce, served with naan',          0),
('Paneer Tikka Masala',     'Indian',       280.00, 'Grilled cottage cheese cubes in spiced onion-tomato gravy',            1),
('Biryani (Chicken)',       'Indian',       350.00, 'Aromatic basmati rice layered with spiced chicken and caramelised onions', 0),
('Daal Makhani',             'Indian',       220.00, 'Slow-cooked black lentils in butter and cream',                        1),
('Masala Dosa',             'Indian',       160.00, 'Crispy rice crepe stuffed with spiced potato, served with chutneys',   1),
('Lamb Rogan Josh',         'Indian',       380.00, 'Kashmiri slow-braised lamb in aromatic red gravy',                     0),
('Chhole Bhature',           'Indian',       180.00, 'Spiced chickpea curry with deep-fried fluffy bread',                   1),
('Fish Amritsari',          'Indian',       340.00, 'Crispy batter-fried fish fillets with chaat masala',                   0),

-- ── ITALIAN ─────────────────────────────────────────────────
('Margherita Pizza',        'Italian',      450.00, 'San Marzano tomato, fresh mozzarella, basil on wood-fired crust',      1),
('Spaghetti Carbonara',     'Italian',      520.00, 'Pasta with pancetta, egg yolk, Pecorino Romano, black pepper',         0),
('Penne Arrabbiata',        'Italian',      420.00, 'Penne in fiery tomato-garlic sauce with fresh parsley',                1),
('Risotto ai Funghi',       'Italian',      490.00, 'Creamy Arborio rice with wild porcini and Parmesan',                   1),
('Osso Buco',               'Italian',      720.00, 'Braised veal shank with gremolata, served with saffron risotto',       0),
('Tiramisu',                'Italian',      220.00, 'Classic espresso-soaked ladyfinger dessert with mascarpone',           1),

-- ── JAPANESE ────────────────────────────────────────────────
('Salmon Nigiri (6 pcs)',   'Japanese',     480.00, 'Hand-pressed vinegared rice topped with fresh Atlantic salmon',        0),
('Chicken Ramen',           'Japanese',     420.00, 'Rich tonkotsu broth, chashu pork, soft egg, nori, bamboo shoots',      0),
('Vegetable Gyoza (8 pcs)', 'Japanese',     320.00, 'Pan-fried dumplings stuffed with cabbage, mushroom, ginger',           1),
('Tempura Udon',            'Japanese',     460.00, 'Thick wheat noodles in dashi broth with crispy vegetable tempura',     1),
('Beef Teriyaki',           'Japanese',     580.00, 'Grilled ribeye glazed with teriyaki sauce, served with steamed rice',  0),
('Miso Soup',               'Japanese',     120.00, 'Traditional dashi-based soup with tofu, wakame, spring onion',         1),

-- ── CHINESE ─────────────────────────────────────────────────
('Peking Duck',             'Chinese',      850.00, 'Whole roasted duck with crispy skin, hoisin sauce, pancakes',          0),
('Kung Pao Chicken',        'Chinese',      380.00, 'Stir-fried chicken with peanuts, dried chillies, Sichuan pepper',      0),
('Dim Sum Basket (6 pcs)',  'Chinese',      360.00, 'Assorted steamed har gow and siu mai dumplings',                       0),
('Mapo Tofu',               'Chinese',      280.00, 'Silken tofu in spicy bean-chilli sauce with minced pork',              0),
('Vegetable Fried Rice',    'Chinese',      220.00, 'Wok-tossed jasmine rice with seasonal vegetables and soy',             1),
('Hot & Sour Soup',         'Chinese',      180.00, 'Classic Shanghainese broth with tofu, bamboo, egg ribbons',            0),

-- ── MEXICAN ─────────────────────────────────────────────────
('Beef Tacos (3 pcs)',      'Mexican',      380.00, 'Corn tortillas with slow-braised beef, pico de gallo, guacamole',      0),
('Chicken Quesadilla',      'Mexican',      340.00, 'Flour tortilla with grilled chicken, peppers, Oaxaca cheese',          0),
('Veggie Burrito',          'Mexican',      320.00, 'Grilled flour wrap with black beans, roasted veggies, salsa, rice',    1),
('Nachos Grande',           'Mexican',      290.00, 'Tortilla chips with melted cheese, jalapeños, sour cream, guac',       1),
('Churros with Chocolate',  'Mexican',      180.00, 'Crispy fried dough sticks dusted with cinnamon sugar, dipping sauce',  1),

-- ── AMERICAN ────────────────────────────────────────────────
('Classic Beef Burger',     'American',     420.00, 'Angus beef patty, cheddar, lettuce, tomato, pickles, brioche bun',     0),
('BBQ Pork Ribs (half rack)','American',    680.00, 'Slow-smoked pork ribs glazed with smoky-sweet BBQ sauce',              0),
('Caesar Salad',            'American',     280.00, 'Romaine, house Caesar dressing, croutons, Parmesan shavings',          1),
('Clam Chowder',            'American',     320.00, 'New England cream-based chowder with clams, potato, bacon',            0),
('New York Cheesecake',     'American',     240.00, 'Dense baked cheesecake on graham cracker crust, berry compote',        1),

-- ── THAI ────────────────────────────────────────────────────
('Pad Thai (Chicken)',      'Thai',         380.00, 'Stir-fried rice noodles with egg, bean sprouts, peanuts, lime',        0),
('Green Curry (Tofu)',      'Thai',         340.00, 'Creamy coconut green curry with tofu, Thai basil, kaffir lime',        1),
('Tom Yum Soup',            'Thai',         260.00, 'Hot-sour lemongrass broth with prawns, galangal, mushrooms',           0),
('Mango Sticky Rice',       'Thai',         200.00, 'Glutinous rice with fresh Alphonso mango and coconut cream',           1),

-- ── FRENCH ──────────────────────────────────────────────────
('French Onion Soup',       'French',       360.00, 'Caramelised onion broth topped with Gruyère crouton',                  1),
('Coq au Vin',              'French',       620.00, 'Chicken braised in Burgundy wine with mushrooms and lardons',          0),
('Crêpes Suzette',          'French',       280.00, 'Thin crêpes in orange-butter sauce, flambéed with Grand Marnier',      1),
('Bouillabaisse',           'French',       740.00, 'Provençal seafood stew with rouille and toasted baguette',             0),

-- ── MEDITERRANEAN / MIDDLE EASTERN ──────────────────────────
('Mezze Platter',           'Mediterranean',390.00, 'Hummus, baba ganoush, falafel, pita, olives, pickled veg',             1),
('Chicken Shawarma Wrap',   'Middle Eastern',360.00,'Marinated chicken, garlic sauce, pickles, fries in lavash',            0),
('Lamb Kebab Platter',      'Middle Eastern',520.00,'Seekh lamb kebabs with rice, grilled veggies, tzatziki',               0),
('Shakshuka',               'Middle Eastern',280.00,'Eggs poached in spiced tomato-pepper sauce, served with pita',         1),

-- ── KOREAN ──────────────────────────────────────────────────
('Bibimbap',                'Korean',       420.00, 'Rice bowl with sautéed vegetables, gochujang, fried egg',              1),
('Korean Fried Chicken',    'Korean',       460.00, 'Double-fried crispy chicken glazed with sweet-spicy gochujang',        0),
('Japchae',                 'Korean',       380.00, 'Glass noodles stir-fried with vegetables and sesame oil',              1),
('Kimchi Jjigae',           'Korean',       340.00, 'Fermented kimchi stew with tofu and pork, served with rice',           0),

-- ── SPANISH ─────────────────────────────────────────────────
('Paella Valenciana',       'Spanish',      680.00, 'Saffron rice with chicken, rabbit, green beans, bomba rice',           0),
('Seafood Paella',          'Spanish',      720.00, 'Bomba rice with prawns, mussels, squid, saffron, smoked paprika',      0),
('Patatas Bravas',          'Spanish',      220.00, 'Crispy potato cubes with smoky tomato sauce and aioli',                1),
('Churros con Leche',       'Spanish',      190.00, 'Fried dough fingers with condensed milk dipping sauce',                1),

-- ── DESSERTS / BEVERAGES ────────────────────────────────────
('Gulab Jamun (4 pcs)',     'Dessert',      140.00, 'Soft milk-solid dumplings soaked in rose-cardamom sugar syrup',        1),
('Crème Brûlée',            'Dessert',      260.00, 'Vanilla custard with caramelised sugar crust',                         1),
('Mango Lassi',             'Beverage',      90.00, 'Chilled blended yoghurt drink with Alphonso mango pulp',               1),
('Masala Chai',             'Beverage',      60.00, 'Spiced milk tea with ginger, cardamom, cinnamon',                      1),
('Fresh Lime Soda',         'Beverage',      70.00, 'Chilled sparkling lime drink — sweet, salted, or mixed',               1),
('Espresso',                'Beverage',      80.00, 'Double-shot Italian espresso',                                         1);

-- ============================================================
--  QUICK SANITY CHECK (optional — remove before production)
-- ============================================================
-- SELECT Category, COUNT(*) AS Items, MIN(Price) AS Min_Price, MAX(Price) AS Max_Price
-- FROM item GROUP BY Category ORDER BY Category;
