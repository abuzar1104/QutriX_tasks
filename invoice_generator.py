from fpdf import FPDF
import datetime


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 24)
        self.cell(0, 10, "INVOICE", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


print("--- Please enter the invoice details ---")
client_name = input("Enter Client's Name: ")
client_address = input("Enter Client's Address: ")
invoice_number = input("Enter Invoice Number (e.g., INV-002): ")
current_date = datetime.date.today().strftime("%Y-%m-%d")

items = []
total_amount = 0.0

print("\n--- Enter Invoice Items (leave description blank to finish) ---")
while True:
    description = input("Enter item description: ")
    if not description:
        break
    try:
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price per item: "))
    except ValueError:
        print("Invalid input. Please enter numbers for quantity and price.")
        continue
    items.append({"description": description, "quantity": quantity, "price": price})
    total_amount += quantity * price
    print("--- Item added ---")

if not items:
    print("No items were added. Invoice not generated.")
else:
    pdf = PDF("P", "mm", "A4")
    pdf.add_page()

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Invoice #: {invoice_number}", 0, 1)
    pdf.cell(0, 10, f"Date: {current_date}", 0, 1)
    pdf.cell(0, 10, f"Bill To: {client_name}", 0, 1)
    pdf.cell(0, 10, f"Address: {client_address}", 0, 1)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, "Description", 1, 0, "C")
    pdf.cell(30, 10, "Quantity", 1, 0, "C")
    pdf.cell(50, 10, "Price (Rs.)", 1, 1, "C")

    pdf.set_font("Arial", "", 12)
    for item in items:
        pdf.cell(100, 10, item["description"], 1, 0)
        pdf.cell(30, 10, str(item["quantity"]), 1, 0, "C")
        pdf.cell(50, 10, f"{item['price']:.2f}", 1, 1, "R")ABUZAR

    pdf.set_font("Arial", "B", 12)
    pdf.cell(130, 10, "Total", 1, 0, "R")
    pdf.cell(50, 10, f"Rs.{total_amount:.2f}", 1, 1, "R")

    pdf_file_name = f"invoice_{invoice_number}.pdf"
    pdf.output(pdf_file_name)

    print(f"\n✅ Invoice '{pdf_file_name}' generated successfully (in Rupees)!")
