# Pharmacy Management System (Flask + MySQL + AI Automation)

A full-featured pharmacy management platform built with **Python Flask**, **MySQL**, and **AI-powered automation**.  
Includes POS, inventory tracking, purchases, sales, returns, expiry alerts, AI reports, and multilingual support.

---

## 🚀 Features

- 🔐 User authentication & role-based access
- 💊 Medicine and batch management
- 📦 Purchase orders + supplier management
- 🧾 POS sales, invoices, returns
- 📉 Stock movements & low-stock alerts
- 💰 Expenses management
- 📊 Advanced reports (daily, monthly, profit/loss)
- 🤖 AI Automations  
  - Expiry predictions  
  - Auto reorder suggestions  
  - AI-generated PDF reports  
  - ChatGPT-powered inventory analysis  
- 🌍 Multi-language (Somali, English, Arabic)
- 📱 REST API for mobile apps

---

## 📁 Folder Structure (Skeleton)

pharmacy_mgmt/
│
├── run.py
├── requirements.txt
├── .env
├── README.md
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py               # global shared models
│   ├── utils.py
│   ├── filters.py
│
│   ├── ai/                     # AI MODULE
│   │   ├── __init__.py
│   │   ├── ai_core.py
│   │   ├── ai_routes.py
│   │   ├── ai_tasks.py         # auto reorder detection, expiry alerts
│   │   └── ai_reports.py       # AI-generated PDF reports
│
│   ├── auth/                   # USER & ROLE SYSTEM
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/auth/
│   │       ├── login.html
│   │       ├── register.html
│   │       └── reset_password.html
│
│   ├── medicines/
│   │   ├── __init__.py
│   │   ├── routes.py           # CRUD: Add, Edit meds
│   │   ├── forms.py
│   │   ├── services.py         # expiry management, stock tracking
│   │   └── templates/medicines/
│   │       ├── list.html
│   │       ├── add.html
│   │       ├── edit.html
│   │       ├── batches.html
│   │       └── expiry_alerts.html
│
│   ├── suppliers/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/suppliers/
│   │       ├── list.html
│   │       ├── add.html
│   │       └── edit.html
│
│   ├── customers/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/customers/
│   │       ├── list.html
│   │       ├── add.html
│   │       └── edit.html
│
│   ├── purchases/              # PURCHASE ORDER MODULE
│   │   ├── __init__.py
│   │   ├── routes.py           # create PO, view PO, receive items
│   │   ├── forms.py
│   │   ├── services.py
│   │   └── templates/purchases/
│   │       ├── list.html
│   │       ├── add.html
│   │       ├── edit.html
│   │       └── receive_stock.html
│
│   ├── purchase_returns/       # RETURN TO SUPPLIER
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/purchase_returns/
│   │       ├── list.html
│   │       └── return.html
│
│   ├── sales/                  # POS + SALES
│   │   ├── __init__.py
│   │   ├── routes.py           # POS interface
│   │   ├── forms.py
│   │   ├── services.py         # invoice creation, payments
│   │   └── templates/sales/
│   │       ├── pos.html        # main POS screen
│   │       ├── invoice.html
│   │       ├── invoice_print.html
│   │       └── list.html
│
│   ├── sales_returns/          
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/sales_returns/
│   │       ├── list.html
│   │       └── return.html
│
│   ├── stock/                  # STOCK MODULE
│   │   ├── __init__.py
│   │   ├── routes.py           # view stock, stock movements
│   │   ├── services.py
│   │   └── templates/stock/
│   │       ├── summary.html
│   │       ├── movement.html
│   │       └── low_stock_alerts.html
│
│   ├── expenses/               # EXPENSE TRACKING
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/expenses/
│   │       ├── list.html
│   │       ├── add.html
│   │       └── edit.html
│
│   ├── reports/                # ADVANCED REPORTING
│   │   ├── __init__.py
│   │   ├── daily_sales.py
│   │   ├── monthly_sales.py
│   │   ├── inventory_report.py
│   │   ├── profit_loss.py
│   │   └── templates/reports/
│   │       ├── daily_sales.html
│   │       ├── monthly_sales.html
│   │       ├── inventory.html
│   │       └── profit_loss.html
│
│   ├── payroll/                # for employees
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/payroll/
│   │       ├── list.html
│   │       ├── pay.html
│   │       └── slip.html
│
│   ├── api/                    # REST API for mobile app
│   │   ├── __init__.py
│   │   ├── routes_sales.py
│   │   ├── routes_stock.py
│   │   ├── routes_medicines.py
│   │   ├── routes_ai.py
│   │   └── routes_reports.py
│
│   ├── templates/              # shared
│   │   ├── base.html
│   │   ├── navbar.html
│   │   ├── sidebar.html
│   │   └── dashboard.html
│
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│
│   ├── translations/
│   │   ├── en/LC_MESSAGES/messages.po
│   │   ├── so/LC_MESSAGES/messages.po
│   │   └── ar/LC_MESSAGES/messages.po
│
│   └── i18n/
│       ├── __init__.py
│       └── routes.py
│
├── migrations/
│
└── logs/
    ├── app.log
    └── errors.log
