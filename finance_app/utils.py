import csv
from django.http import HttpResponse

def generate_csv_report(expenses):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Category', 'Amount', 'Date'])
    for exp in expenses:
        writer.writerow([exp.title, exp.category.name if exp.category else '', exp.amount, exp.date])
    return response
