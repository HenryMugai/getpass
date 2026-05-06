getpass_v2/
│
├── app.py                          # App entry point: creates Flask app, registers all blueprints, starts server
├── config.py                       # Configs: DB credentials, secret keys, payment API keys (M-Pesa, Instasend, Pesapal)
├── requirements.txt                # All dependencies (Flask, mysql-connector, qrcode, requests, etc.)
│
├── database/
│   ├── db.py                       # Handles MySQL connection + reusable query execution
│   └── schema.sql                  # Full database schema (your production-ready DB)
│
├── routes/
│   ├── __init__.py                 # Registers all route blueprints into the app
│   │
│   ├── public/
│   │   ├── __init__.py             # Public blueprint init
│   │   ├── index.py                # Landing page → show featured/upcoming events
│   │   ├── events.py               # Events listing → all published events, filters/search
│   │   ├── event_detail.py         # Single event → event info + ticket types + buy button
│   │   ├── checkout.py             # Checkout → collect buyer info + initiate payment (STK / API)
│   │   └── success.py              # Payment success → confirm payment + generate tickets + show QR/download
│   │
│   ├── admin/
│   │   ├── __init__.py             # Admin blueprint init
│   │   ├── dashboard.py            # Admin overview → total revenue, tickets sold, events count
│   │   ├── users.py                # Manage users → create organisers + agents, activate/deactivate users
│   │   ├── events.py               # Event control → create/edit events, assign organisers, create ticket types, publish/close
│   │   └── agents.py               # Agent assignment → link agents to events (agent_events table)
│   │
│   ├── organiser/
│   │   ├── __init__.py             # Organiser blueprint init
│   │   ├── dashboard.py            # Organiser overview → earnings, tickets sold, event stats
│   │   ├── events.py               # Organiser events → view assigned events + ticket breakdown
│   │   └── attendees.py            # Attendee list → view buyers, ticket status, export (future)
│   │
│   ├── agent/
│   │   ├── __init__.py             # Agent blueprint init
│   │   └── checkin.py              # Check-in system → scan/input QR, validate ticket, mark as checked-in, log agent
│   │
│   └── auth/
│       ├── __init__.py             # Auth blueprint init
│       └── login.py                # Login system → admin/organiser/agent login (no signup for organisers)
│
├── services/
│   ├── payment_service.py          # Handles payment logic → STK push, API calls, payment verification, callbacks
│   ├── ticket_service.py           # Ticket logic → create attendees, generate ticket codes, update ticket sold count
│   └── qr_service.py               # QR generation → create QR images from ticket_code
│
├── templates/
│   ├── base.html                   # Shared layout → navbar, footer, global styles/scripts
│   │
│   ├── public/
│   │   ├── index.html              # Landing page → hero section, featured events, CTA
│   │   ├── events.html             # Events page → grid/list of available events
│   │   ├── event_detail.html       # Event detail → description, ticket options, buy button
│   │   ├── checkout.html           # Checkout UI → form (name, phone, email) + payment trigger
│   │   └── success.html            # Success page → ticket display, QR code, print/download option
│   │
│   ├── admin/
│   │   ├── dashboard.html          # Admin dashboard → analytics cards + recent activity
│   │   ├── users.html              # User management → list/create organisers & agents
│   │   ├── events.html             # Event management → create/edit events + ticket setup
│   │   └── agents.html             # Agent assignment UI → assign agents to events
│   │
│   ├── organiser/
│   │   ├── dashboard.html          # Organiser dashboard → earnings + stats view
│   │   ├── events.html             # Organiser events → their assigned events
│   │   └── attendees.html          # Attendee list → all ticket buyers for their event
│   │
│   ├── agent/
│   │   └── checkin.html            # Check-in page → QR scanner UI + manual code entry
│   │
│   └── auth/
│       └── login.html              # Login page → email + password (role-based redirect)
│
├── static/
│   ├── css/
│   │   ├── base.css                # Global styles → typography, layout, navbar/footer
│   │   ├── public.css              # Public pages styling → landing, events, checkout
│   │   ├── admin.css               # Admin UI styling → dashboard tables, cards
│   │   ├── organiser.css           # Organiser dashboard styling
│   │   └── agent.css               # Agent UI styling → check-in interface
│   │
│   ├── js/
│   │   ├── main.js                 # Global JS → UI interactions, minor helpers
│   │   └── qr_scanner.js           # QR scanning logic → camera access, decode QR, send to backend
│   │
│   └── images/                    # Static images (logos, event placeholders, etc.)
│
└── utils/
    ├── decorators.py              # Access control → @admin_required, @organiser_required, @agent_required
    └── helpers.py                 # Helper functions → formatting, validation, reusable utilities