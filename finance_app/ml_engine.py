import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def analyze_user_finances(user):
    from .models import Expense
    expenses = Expense.objects.filter(user=user).select_related('category').order_by('date')
    if not expenses.exists():
        return {
            'status': 'insufficient_data',
            'message': 'Add at least 5 transactions to enable AI analytics.'
        }
    data = [{
        'title': e.title,
        'amount': float(e.amount),
        'category': e.category.name if e.category else 'Uncategorized',
        'date': pd.to_datetime(e.date)
    } for e in expenses]
    df = pd.DataFrame(data)
    cat_spend = df.groupby('category')['amount'].sum().reset_index()
    highest_cat = cat_spend.loc[cat_spend['amount'].idxmax()]['category'] if not cat_spend.empty else 'N/A'
    
    daily = df.groupby('date')['amount'].sum().reset_index()
    daily['day_index'] = (daily['date'] - daily['date'].min()).dt.days
    pred = float(df['amount'].sum() * 1.1)
    if len(daily) >= 3:
        model = LinearRegression()
        model.fit(daily[['day_index']], daily['amount'])
        future = np.arange(daily['day_index'].max() + 1, daily['day_index'].max() + 31).reshape(-1, 1)
        pred = float(np.maximum(model.predict(future), 0).sum())
        
    return {
        'status': 'success',
        'total_spent': float(df['amount'].sum()),
        'highest_category': highest_cat,
        'predicted_next_month': pred,
        'category_breakdown': cat_spend.to_dict(orient='records'),
        'suggestions': [
            f"Highest spending category is {highest_cat}.",
            f"Estimated next month expenditure: ₹{pred:.2f}."
        ]
    }
