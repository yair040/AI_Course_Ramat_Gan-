"""
Grocery Association Rules Mining
Author: Yair Levi
Date: October 15, 2025

Finds association rules where 3 items predict 2 items: {Item1, Item2, Item3} -> {Item4, Item5}
"""

import numpy as np
from itertools import combinations

# Configuration
DATASET_FILE = "grocery_dataset.txt"
MIN_SUPPORT = 0.003      # 0.3%
MIN_CONFIDENCE = 0.40    # 40%
MIN_LIFT = 1.0

print("=" * 80)
print("GROCERY ASSOCIATION RULES MINING")
print("Author: Yair Levi")
print("=" * 80)
print(f"\nDataset File: {DATASET_FILE}")
print(f"Rule Pattern: {{Item1, Item2, Item3}} -> {{Item4, Item5}}")
print(f"Minimum Support: {MIN_SUPPORT * 100:.1f}%")
print(f"Minimum Confidence: {MIN_CONFIDENCE * 100:.0f}%")
print(f"Minimum Lift: {MIN_LIFT}")
print("=" * 80)

# Read the dataset
try:
    with open(DATASET_FILE, 'r', encoding='utf-8') as f:
        transactions = []
        for line in f:
            # Remove whitespace and split by comma
            items = [item.strip() for item in line.strip().split(',') if item.strip()]
            if items:  # Only add non-empty transactions
                transactions.append(items)
    
    print(f"\n✓ Dataset loaded successfully!")
    print(f"  Total transactions: {len(transactions)}")
    
    # Get all unique items
    all_items = set()
    for transaction in transactions:
        all_items.update(transaction)
    
    print(f"  Unique items: {len(all_items)}")
    
    # Show sample items (first 15)
    sample_items = sorted(all_items)[:15]
    print(f"  Sample items: {', '.join(sample_items)}")
    if len(all_items) > 15:
        print(f"                ... and {len(all_items) - 15} more")
    
    # Transaction size statistics
    transaction_sizes = [len(t) for t in transactions]
    avg_size = np.mean(transaction_sizes)
    max_size = max(transaction_sizes)
    min_size = min(transaction_sizes)
    print(f"\n  Transaction sizes: min={min_size}, max={max_size}, avg={avg_size:.2f}")
    
except FileNotFoundError:
    print(f"\n✗ Error: File '{DATASET_FILE}' not found!")
    print("  Please ensure the file exists in the current directory.")
    print("\nExample file format:")
    print("  bread, milk, eggs, butter, cheese")
    print("  coffee, bread, cheese, yogurt")
    print("  milk, eggs, yogurt, butter, orange juice")
    exit(1)
except Exception as e:
    print(f"\n✗ Error reading file: {e}")
    exit(1)

# Convert items to indices for efficiency
item_to_idx = {item: idx for idx, item in enumerate(sorted(all_items))}
idx_to_item = {idx: item for item, idx in item_to_idx.items()}

# Convert transactions to index format (using sets for faster lookup)
indexed_transactions = []
for transaction in transactions:
    indexed_transactions.append(set([item_to_idx[item] for item in transaction]))

total_transactions = len(indexed_transactions)

print("\n" + "=" * 80)
print("CALCULATING SUPPORT FOR ITEMSETS")
print("=" * 80)

# Function to calculate support for an itemset
def calculate_support(transactions, itemset):
    """Calculate support for an itemset (set of item indices)."""
    count = 0
    itemset_set = set(itemset) if not isinstance(itemset, set) else itemset
    for transaction in transactions:
        if itemset_set.issubset(transaction):
            count += 1
    return count / len(transactions)

# Step 1: Find frequent 1-itemsets
print("\nStep 1: Finding frequent 1-itemsets (individual items)...")
item_support = {}
frequent_1_items = []

for item_idx in item_to_idx.values():
    support = calculate_support(indexed_transactions, {item_idx})
    item_support[item_idx] = support
    
    if support >= MIN_SUPPORT:
        frequent_1_items.append(item_idx)

print(f"✓ Found {len(frequent_1_items)} frequent 1-itemsets (support >= {MIN_SUPPORT * 100:.1f}%)")

# Step 2: Find frequent 2-itemsets
print("\nStep 2: Finding frequent 2-itemsets (pairs)...")
pair_support = {}
frequent_2_items = []

for item1, item2 in combinations(frequent_1_items, 2):
    itemset = frozenset([item1, item2])
    support = calculate_support(indexed_transactions, {item1, item2})
    pair_support[itemset] = support
    
    if support >= MIN_SUPPORT:
        frequent_2_items.append(tuple(sorted([item1, item2])))

print(f"✓ Found {len(frequent_2_items)} frequent 2-itemsets (support >= {MIN_SUPPORT * 100:.1f}%)")

# Step 3: Find frequent 3-itemsets
print("\nStep 3: Finding frequent 3-itemsets (triples)...")
triple_support = {}
frequent_3_items = []

# Generate candidates from frequent 2-itemsets
candidates = set()
for pair1 in frequent_2_items:
    for pair2 in frequent_2_items:
        combined = tuple(sorted(set(pair1) | set(pair2)))
        if len(combined) == 3:
            candidates.add(combined)

for itemset in candidates:
    support = calculate_support(indexed_transactions, set(itemset))
    triple_support[frozenset(itemset)] = support
    
    if support >= MIN_SUPPORT:
        frequent_3_items.append(itemset)

print(f"✓ Found {len(frequent_3_items)} frequent 3-itemsets (support >= {MIN_SUPPORT * 100:.1f}%)")

# Step 4: Find frequent 5-itemsets
print("\nStep 4: Finding frequent 5-itemsets (5 items together)...")
five_support = {}
frequent_5_items = []

# Generate candidates from frequent 3-itemsets
candidates = set()
for triple1 in frequent_3_items:
    for triple2 in frequent_3_items:
        combined = tuple(sorted(set(triple1) | set(triple2)))
        if len(combined) == 5:
            candidates.add(combined)

print(f"  Checking {len(candidates)} candidate 5-itemsets...")

for itemset in candidates:
    support = calculate_support(indexed_transactions, set(itemset))
    five_support[frozenset(itemset)] = support
    
    if support >= MIN_SUPPORT:
        frequent_5_items.append(itemset)

print(f"✓ Found {len(frequent_5_items)} frequent 5-itemsets (support >= {MIN_SUPPORT * 100:.1f}%)")

print("\n" + "=" * 80)
print("GENERATING ASSOCIATION RULES: {3 items} -> {2 items}")
print("=" * 80)

# Generate rules: {3 items} -> {2 items}
rules = []

print(f"\nGenerating rules from {len(frequent_5_items)} frequent 5-itemsets...")

for itemset in frequent_5_items:
    items = list(itemset)
    
    # For each 5-itemset, generate all possible 3->2 rules
    # Choose 3 items for antecedent, remaining 2 for consequent
    for antecedent_items in combinations(items, 3):
        antecedent = tuple(sorted(antecedent_items))
        consequent = tuple(sorted([item for item in items if item not in antecedent]))
        
        # Calculate metrics
        support_union = five_support[frozenset(itemset)]
        support_antecedent = triple_support.get(frozenset(antecedent), 0)
        support_consequent = pair_support.get(frozenset(consequent), 0)
        
        if support_antecedent > 0 and support_consequent > 0:
            confidence = support_union / support_antecedent
            lift = support_union / (support_antecedent * support_consequent)
            
            # Check if rule meets criteria
            if confidence >= MIN_CONFIDENCE and lift > MIN_LIFT:
                rules.append({
                    'antecedent': antecedent,
                    'consequent': consequent,
                    'support': support_union,
                    'confidence': confidence,
                    'lift': lift
                })

print(f"\n✓ Found {len(rules)} rules meeting all criteria")

# Sort rules by lift (descending)
rules.sort(key=lambda x: x['lift'], reverse=True)

# Display results
print("\n" + "=" * 80)
print("ASSOCIATION RULES")
print("=" * 80)

if len(rules) == 0:
    print("\n✗ No rules found meeting the specified criteria.")
    print("\nPossible reasons:")
    print(f"  • Support threshold too high (current: {MIN_SUPPORT * 100:.1f}% - try 0.1% or lower)")
    print(f"  • Confidence threshold too high (current: {MIN_CONFIDENCE * 100:.0f}% - try 30% or lower)")
    print("  • Dataset too small for 5-item combinations")
    print("  • Transactions don't have enough items (need at least 5 items per transaction)")
    print("\nTip: Lower the thresholds in the code:")
    print("  MIN_SUPPORT = 0.001      # 0.1%")
    print("  MIN_CONFIDENCE = 0.30    # 30%")
else:
    print(f"\n{'-' * 80}")
    print(f"{'Rule':<60} {'Support':<14} {'Confidence':<14} {'Lift':<10}")
    print(f"{'-' * 80}")
    
    for idx, rule in enumerate(rules, 1):
        # Format antecedent and consequent with item names
        ante_items = [idx_to_item[i] for i in rule['antecedent']]
        cons_items = [idx_to_item[i] for i in rule['consequent']]
        
        ante_str = '{' + ', '.join(ante_items) + '}'
        cons_str = '{' + ', '.join(cons_items) + '}'
        rule_str = f"{ante_str} -> {cons_str}"
        
        # Print rule with metrics
        print(f"{rule_str:<60} {rule['support']:.6f} ({rule['support']*100:5.2f}%)  "
              f"{rule['confidence']:.4f} ({rule['confidence']*100:5.2f}%)  "
              f"{rule['lift']:.4f}")
    
    print(f"{'-' * 80}")
    
    # Display best rule by lift
    print("\n" + "=" * 80)
    print("⭐ BEST RULE BY LIFT ⭐")
    print("=" * 80)
    
    best_rule = rules[0]
    ante_items = [idx_to_item[i] for i in best_rule['antecedent']]
    cons_items = [idx_to_item[i] for i in best_rule['consequent']]
    
    print(f"\nRule: {{{', '.join(ante_items)}}} -> {{{', '.join(cons_items)}}}")
    print(f"\n  Support:    {best_rule['support']:.6f} ({best_rule['support']*100:.3f}%)")
    print(f"  Confidence: {best_rule['confidence']:.4f} ({best_rule['confidence']*100:.2f}%)")
    print(f"  Lift:       {best_rule['lift']:.4f} ⭐ HIGHEST")
    
    print(f"\nInterpretation:")
    print(f"  • {best_rule['support']*100:.3f}% of all transactions contain all 5 items")
    print(f"  • When {{{', '.join(ante_items)}}} are purchased together,")
    print(f"    there's a {best_rule['confidence']*100:.2f}% chance that {{{', '.join(cons_items)}}} are also purchased")
    print(f"  • These items appear together {best_rule['lift']:.2f}x more often than expected by chance")
    
    # Additional insights
    print(f"\n  Business Insights:")
    print(f"    ➜ Cross-sell opportunity: Recommend {{{', '.join(cons_items)}}} to customers buying")
    print(f"      {{{', '.join(ante_items)}}}")
    print(f"    ➜ Product placement: Position these 5 items in proximity")
    print(f"    ➜ Bundle promotion: Create a 5-item package deal")
    print(f"    ➜ Marketing: Create targeted campaigns for customers buying the antecedent items")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    avg_support = np.mean([r['support'] for r in rules])
    avg_confidence = np.mean([r['confidence'] for r in rules])
    avg_lift = np.mean([r['lift'] for r in rules])
    
    max_support = max([r['support'] for r in rules])
    max_confidence = max([r['confidence'] for r in rules])
    max_lift = max([r['lift'] for r in rules])
    
    min_support = min([r['support'] for r in rules])
    min_confidence = min([r['confidence'] for r in rules])
    min_lift = min([r['lift'] for r in rules])
    
    print(f"\nTotal Rules Found: {len(rules)}")
    print(f"Frequent 1-itemsets: {len(frequent_1_items)}")
    print(f"Frequent 2-itemsets: {len(frequent_2_items)}")
    print(f"Frequent 3-itemsets: {len(frequent_3_items)}")
    print(f"Frequent 5-itemsets: {len(frequent_5_items)}")
    
    print(f"\nAverage Metrics:")
    print(f"  Support:    {avg_support:.6f} ({avg_support*100:.3f}%)")
    print(f"  Confidence: {avg_confidence:.4f} ({avg_confidence*100:.2f}%)")
    print(f"  Lift:       {avg_lift:.4f}")
    
    print(f"\nMaximum Metrics:")
    print(f"  Support:    {max_support:.6f} ({max_support*100:.3f}%)")
    print(f"  Confidence: {max_confidence:.4f} ({max_confidence*100:.2f}%)")
    print(f"  Lift:       {max_lift:.4f}")
    
    print(f"\nMinimum Metrics:")
    print(f"  Support:    {min_support:.6f} ({min_support*100:.3f}%)")
    print(f"  Confidence: {min_confidence:.4f} ({min_confidence*100:.2f}%)")
    print(f"  Lift:       {min_lift:.4f}")
    
    # Top rules by different metrics
    if len(rules) >= 5:
        print("\n" + "=" * 80)
        print("TOP 5 RULES BY DIFFERENT METRICS")
        print("=" * 80)
        
        print("\n--- Top 5 by Lift (Strongest Associations) ---")
        top_lift = sorted(rules, key=lambda x: x['lift'], reverse=True)[:5]
        for idx, rule in enumerate(top_lift, 1):
            ante = ', '.join([idx_to_item[i] for i in rule['antecedent']])
            cons = ', '.join([idx_to_item[i] for i in rule['consequent']])
            print(f"\n{idx}. {{{ante}}} -> {{{cons}}}")
            print(f"   Lift: {rule['lift']:.4f} | Confidence: {rule['confidence']:.4f} | Support: {rule['support']:.6f}")
        
        print("\n--- Top 5 by Confidence (Most Reliable) ---")
        top_conf = sorted(rules, key=lambda x: x['confidence'], reverse=True)[:5]
        for idx, rule in enumerate(top_conf, 1):
            ante = ', '.join([idx_to_item[i] for i in rule['antecedent']])
            cons = ', '.join([idx_to_item[i] for i in rule['consequent']])
            print(f"\n{idx}. {{{ante}}} -> {{{cons}}}")
            print(f"   Confidence: {rule['confidence']:.4f} ({rule['confidence']*100:.2f}%) | Lift: {rule['lift']:.4f}")
        
        print("\n--- Top 5 by Support (Most Frequent) ---")
        top_supp = sorted(rules, key=lambda x: x['support'], reverse=True)[:5]
        for idx, rule in enumerate(top_supp, 1):
            ante = ', '.join([idx_to_item[i] for i in rule['antecedent']])
            cons = ', '.join([idx_to_item[i] for i in rule['consequent']])
            print(f"\n{idx}. {{{ante}}} -> {{{cons}}}")
            print(f"   Support: {rule['support']:.6f} ({rule['support']*100:.3f}%) | Confidence: {rule['confidence']:.4f}")
    
    # Most common item combinations in antecedents
    print("\n" + "=" * 80)
    print("ITEM COMBINATION ANALYSIS")
    print("=" * 80)
    
    # Count item appearances in antecedents
    antecedent_item_counts = {}
    for rule in rules:
        for item in rule['antecedent']:
            antecedent_item_counts[item] = antecedent_item_counts.get(item, 0) + 1
    
    if antecedent_item_counts:
        print("\n--- Top 10 Items in Antecedents (Most Predictive) ---")
        top_ante = sorted(antecedent_item_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        for idx, (item_idx, count) in enumerate(top_ante, 1):
            item_name = idx_to_item[item_idx]
            print(f"{idx:2d}. {item_name:<30} Appears in {count} rules")
    
    # Count item appearances in consequents
    consequent_item_counts = {}
    for rule in rules:
        for item in rule['consequent']:
            consequent_item_counts[item] = consequent_item_counts.get(item, 0) + 1
    
    if consequent_item_counts:
        print("\n--- Top 10 Items in Consequents (Most Predicted) ---")
        top_cons = sorted(consequent_item_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        for idx, (item_idx, count) in enumerate(top_cons, 1):
            item_name = idx_to_item[item_idx]
            print(f"{idx:2d}. {item_name:<30} Predicted in {count} rules")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("Author: Yair Levi")
print("=" * 80)