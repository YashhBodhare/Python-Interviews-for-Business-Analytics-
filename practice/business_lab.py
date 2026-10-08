"""Small fictional INR dataset with explicit business-result checks."""
import pandas as pd

def main():
    orders = pd.DataFrame([
        {"order_id": 101, "customer_id": 1, "month": "2026-01", "status": "paid", "amount": 1000},
        {"order_id": 102, "customer_id": 1, "month": "2026-01", "status": "paid", "amount": 500},
        {"order_id": 103, "customer_id": 2, "month": "2026-01", "status": "pending", "amount": 800},
        {"order_id": 104, "customer_id": 2, "month": "2026-02", "status": "paid", "amount": 1500},
        {"order_id": 105, "customer_id": 3, "month": "2026-02", "status": "cancelled", "amount": 300},
        {"order_id": 106, "customer_id": 3, "month": "2026-02", "status": "paid", "amount": 0},
        {"order_id": 107, "customer_id": 1, "month": "2026-02", "status": "paid", "amount": 700},
    ])
    customers = pd.DataFrame({"customer_id": [1, 2, 3, 4], "city": ["Thane", "Mumbai", "Thane", "Pune"]})
    # Grain: one row per order. Zero-value paid orders are included in AOV.
    assert orders['order_id'].is_unique
    paid = orders.loc[orders['status'].eq('paid')].copy()
    assert len(paid) == 5 and paid['amount'].sum() == 3700 and paid['amount'].mean() == 740
    print('PASS: paid revenue 3700, paid orders 5, AOV 740')

    enriched = paid.merge(customers, on='customer_id', how='left', validate='m:1', indicator=True)
    assert len(enriched) == len(paid) and enriched['amount'].sum() == 3700
    assert enriched['_merge'].eq('both').all()
    print('PASS: reference enrichment preserves grain and revenue')

    summary = enriched.groupby('city', as_index=False).agg(revenue=('amount', 'sum'), orders=('order_id', 'size'))
    assert summary.set_index('city')['revenue'].to_dict() == {'Mumbai': 1500, 'Thane': 2200}
    print('PASS: city totals reconcile to 3700')

    by_customer = paid.groupby('customer_id', as_index=False).agg(revenue=('amount', 'sum'), paid_orders=('order_id', 'size'))
    all_customers = customers.merge(by_customer, on='customer_id', how='left', validate='1:1')
    # Missing aggregates here mean no qualifying order, so zero is justified.
    all_customers[['revenue', 'paid_orders']] = all_customers[['revenue', 'paid_orders']].fillna(0)
    assert len(all_customers) == 4
    assert all_customers.loc[all_customers['customer_id'].eq(4), 'paid_orders'].item() == 0
    print('PASS: non-buyers are retained')

    monthly = paid.pivot_table(index='customer_id', columns='month', values='amount', aggfunc='sum', fill_value=0)
    assert monthly['2026-01'].sum() == 1500 and monthly['2026-02'].sum() == 2200
    print('PASS: monthly revenue January 1500, February 2200')

    # A duplicated reference key must fail rather than inflate sales.
    bad_reference = pd.concat([customers, customers.iloc[[0]]], ignore_index=True)
    try:
        paid.merge(bad_reference, on='customer_id', validate='m:1')
    except pd.errors.MergeError:
        print('PASS: duplicate customer reference rejected')
    else:
        raise AssertionError('Duplicate reference accepted')

    original = orders.copy(deep=True)
    orders.loc[orders['amount'].gt(1000), 'review'] = 'high value'
    assert orders['review'].eq('high value').sum() == 1 and 'review' not in original.columns
    print('PASS: intended assignment and retained source version')

    nullable = pd.Series([1, None, 0], dtype='Int64')
    assert nullable.isna().tolist() == [False, True, False]
    print('PASS: missing value is distinct from zero')
    print('All 8 business checks passed. pandas', pd.__version__)

if __name__ == '__main__':
    main()
