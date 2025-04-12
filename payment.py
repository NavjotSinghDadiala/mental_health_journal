import tkinter as tk
import webbrowser

# Replace with actual Razorpay checkout links
RAZORPAY_MONTHLY_URL = "https://rzp.io/l/YOUR_MONTHLY_PLAN"
RAZORPAY_QUARTERLY_URL = "https://rzp.io/l/YOUR_QUARTERLY_PLAN"
RAZORPAY_YEARLY_URL = "https://rzp.io/l/YOUR_YEARLY_PLAN"

def open_payment_link(link):
    webbrowser.open(link)

# Initialize app
app = tk.Tk()
app.title("💳 Premium Subscription Plans")
app.geometry("600x600")
app.configure(bg='#E0F7FA')

# Title
tk.Label(app, text="Upgrade to Premium 🪙", font=("Helvetica", 20, "bold"),
         fg="#00796B", bg="#E0F7FA").pack(pady=20)

# Subtitle
tk.Label(app, text="Choose a plan that suits you", font=("Helvetica", 14),
         fg="#004D40", bg="#E0F7FA").pack(pady=5)

# Plan Card Template
def create_plan(title, price, benefits, url):
    frame = tk.Frame(app, bg='white', bd=2, relief="groove")
    frame.pack(pady=15, padx=20, fill="x")

    tk.Label(frame, text=title, font=("Helvetica", 16, "bold"), fg="#00796B", bg="white").pack(pady=(10, 0))
    tk.Label(frame, text=price, font=("Helvetica", 14), fg="#004D40", bg="white").pack()

    for b in benefits:
        tk.Label(frame, text="• " + b, font=("Helvetica", 11), bg="white", anchor="w", justify="left").pack(padx=10, anchor='w')

    tk.Button(frame, text="Pay Now", font=("Helvetica", 12), bg="#00BCD4", fg="white",
              command=lambda: open_payment_link(url)).pack(pady=10)

# Define each plan
create_plan(
    "Monthly Plan",
    "₹99 / month",
    ["Access to journal features", "Advanced analytics", "Priority support"],
    RAZORPAY_MONTHLY_URL
)

create_plan(
    "Quarterly Plan",
    "₹249 / 3 months",
    ["All monthly features", "Bonus wellness exercises", "Early access to updates"],
    RAZORPAY_QUARTERLY_URL
)

create_plan(
    "Yearly Plan",
    "₹899 / year",
    ["All features unlocked", "1-on-1 consultation access", "Lifetime token vault"],
    RAZORPAY_YEARLY_URL
)

# Exit button
tk.Button(app, text="Back to App", font=("Helvetica", 12), bg="#B2DFDB", command=app.destroy).pack(pady=20)

app.mainloop()
