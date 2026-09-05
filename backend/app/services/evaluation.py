def evaluate(records, truth, detected_exceptions=None):
    detected_ids = {
        item['transaction_id'] for item in (detected_exceptions or [])
    }
    truth_ids = {
        r['transaction_id'] for r in records
        if truth[r['transaction_id']]['has_exception']
    }
    total = len(records)
    true_positive = len(detected_ids & truth_ids)
    false_positive = len(detected_ids - truth_ids)
    false_negative = len(truth_ids - detected_ids)
    true_negative = total - true_positive - false_positive - false_negative
    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 1.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    matched = total - len(detected_ids)
    return {
        'total_records': total,
        'ground_truth_exceptions': len(truth_ids),
        'ground_truth_matches': total - len(truth_ids),
        'detected_exceptions': len(detected_ids),
        'match_rate': round(matched / total * 100, 2) if total else 0,
        'classification_accuracy': round((true_positive + true_negative) / total * 100, 2) if total else 0,
        'precision': round(precision * 100, 2),
        'recall': round(recall * 100, 2),
        'f1': round(f1 * 100, 2),
        'false_positives': false_positive,
        'false_negatives': false_negative,
        'financial_exposure': round(sum(
            abs(r['payment_amount'] - r['settlement_amount'])
            for r in records if r['transaction_id'] in truth_ids
        ), 2),
        'note': 'Metrics compare detected exceptions with the seeded synthetic ground truth.'
    }
