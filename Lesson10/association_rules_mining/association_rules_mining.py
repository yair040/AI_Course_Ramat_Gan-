import numpy as np
from itertools import combinations

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
n_rows = 5000
n_features = 6
feature_names = ['a', 'b', 'c', 'd', 'e', 'f']
probabilities = [0.80, 0.60, 0.40, 0.30, 0.20, 0.10]

# Thresholds
min_support = 0.30
min_confidence = 0.70

print("=" * 80)
print("ASSOCIATION RULES MINING")
print("=" * 80)
print(f"\nDataset: {n_rows} rows, {n_features} features")
print(f"Features: {feature_names}")
print(f"Probabilities: {probabilities}")
print(f"\nThresholds:")
print(f"  Minimum Support: {min_support * 100}%")
print(f"  Minimum Confidence: {min_confidence * 100}%")
print("=" * 80)

# Create dataset with specified probabilities
dataset = np.zeros((n_rows, n_features), dtype=int)

for col_idx, prob in enumerate(probabilities):
    # Generate random values: 1 with probability 'prob', 0 otherwise
    dataset[:, col_idx] = np.random.choice([0, 1], size=n_rows, p=[1-prob, prob])

print(f"\nDataset created successfully!")
print(f"Dataset shape: {dataset.shape}")

# Verify actual percentages
print(f"\nActual percentages of 1s in each column:")
for idx, name in enumerate(feature_names):
    actual_pct = np.sum(dataset[:, idx]) / n_rows * 100
    print(f"  {name}: {actual_pct:.2f}% (target: {probabilities[idx]*100:.2f}%)")

# Function to calculate support for an itemset
def calculate_support(dataset, itemset):
    """
    Calculate support for an itemset.
    Support = count of transactions containing all items / total transactions
    """
    if len(itemset) == 0:
        return 0.0
    
    # Create mask for all items in itemset
    mask = np.ones(len(dataset), dtype=bool)
    for item_idx in itemset:
        mask &= (dataset[:, item_idx] == 1)
    
    count = np.sum(mask)
    support = count / len(dataset)
    return support

# Function to calculate confidence for a rule
def calculate_confidence(dataset, antecedent, consequent):
    """
    Calculate confidence for rule: antecedent -> consequent
    Confidence = support(antecedent + consequent) / support(antecedent)
    """
    # Support of antecedent + consequent (union)
    union_itemset = antecedent + consequent
    support_union = calculate_support(dataset, union_itemset)
    
    # Support of antecedent
    support_antecedent = calculate_support(dataset, antecedent)
    
    if support_antecedent == 0:
        return 0.0
    
    confidence = support_union / support_antecedent
    return confidence

# Function to calculate lift for a rule
def calculate_lift(dataset, antecedent, consequent):
    """
    Calculate lift for rule: antecedent -> consequent
    Lift = confidence(antecedent -> consequent) / support(consequent)
    Lift = support(antecedent + consequent) / (support(antecedent) * support(consequent))
    """
    # Support of union
    union_itemset = antecedent + consequent
    support_union = calculate_support(dataset, union_itemset)
    
    # Support of antecedent and consequent
    support_antecedent = calculate_support(dataset, antecedent)
    support_consequent = calculate_support(dataset, consequent)
    
    if support_antecedent == 0 or support_consequent == 0:
        return 0.0
    
    lift = support_union / (support_antecedent * support_consequent)
    return lift

# Generate all possible itemsets and rules
print("\n" + "=" * 80)
print("FINDING ASSOCIATION RULES")
print("=" * 80)

all_rules = []

# Generate itemsets of different sizes (1 to n_features)
for size in range(2, n_features + 1):
    # Get all combinations of features of this size
    for itemset in combinations(range(n_features), size):
        itemset = list(itemset)
        
        # Calculate support for this itemset
        support = calculate_support(dataset, itemset)
        
        # Only process if support meets minimum threshold
        if support >= min_support:
            # Generate all possible rules from this itemset
            # For each subset as antecedent, rest as consequent
            for ante_size in range(1, len(itemset)):
                for antecedent_indices in combinations(itemset, ante_size):
                    antecedent = list(antecedent_indices)
                    consequent = [x for x in itemset if x not in antecedent]
                    
                    # Calculate confidence
                    confidence = calculate_confidence(dataset, antecedent, consequent)
                    
                    # Check if confidence meets minimum threshold
                    if confidence >= min_confidence:
                        # Calculate lift
                        lift = calculate_lift(dataset, antecedent, consequent)
                        
                        # Store the rule
                        rule = {
                            'antecedent': antecedent,
                            'consequent': consequent,
                            'support': support,
                            'confidence': confidence,
                            'lift': lift
                        }
                        all_rules.append(rule)

# Sort rules by confidence (descending), then by support
all_rules.sort(key=lambda x: (x['confidence'], x['support']), reverse=True)

# Display results
print(f"\nTotal rules found: {len(all_rules)}")
print("\n" + "=" * 80)
print("ASSOCIATION RULES")
print("=" * 80)

if len(all_rules) == 0:
    print("\nNo rules found matching the criteria.")
else:
    print(f"\n{'Rule':<30} {'Support':<12} {'Confidence':<12} {'Lift':<10}")
    print("-" * 80)
    
    for idx, rule in enumerate(all_rules, 1):
        # Format antecedent and consequent
        ante_str = ','.join([feature_names[i] for i in rule['antecedent']])
        cons_str = ','.join([feature_names[i] for i in rule['consequent']])
        rule_str = f"{{{ante_str}}} -> {{{cons_str}}}"
        
        # Print rule with metrics
        print(f"{rule_str:<30} {rule['support']:.4f} ({rule['support']*100:5.2f}%)  "
              f"{rule['confidence']:.4f} ({rule['confidence']*100:5.2f}%)  "
              f"{rule['lift']:.4f}")

# Summary statistics
if len(all_rules) > 0:
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    avg_support = np.mean([r['support'] for r in all_rules])
    avg_confidence = np.mean([r['confidence'] for r in all_rules])
    avg_lift = np.mean([r['lift'] for r in all_rules])
    
    max_support = max([r['support'] for r in all_rules])
    max_confidence = max([r['confidence'] for r in all_rules])
    max_lift = max([r['lift'] for r in all_rules])
    
    print(f"\nAverage Support:    {avg_support:.4f} ({avg_support*100:.2f}%)")
    print(f"Average Confidence: {avg_confidence:.4f} ({avg_confidence*100:.2f}%)")
    print(f"Average Lift:       {avg_lift:.4f}")
    print(f"\nMaximum Support:    {max_support:.4f} ({max_support*100:.2f}%)")
    print(f"Maximum Confidence: {max_confidence:.4f} ({max_confidence*100:.2f}%)")
    print(f"Maximum Lift:       {max_lift:.4f}")
    
    # Show top 5 rules by different metrics
    print("\n" + "=" * 80)
    print("TOP 5 RULES BY CONFIDENCE")
    print("=" * 80)
    
    top_by_conf = sorted(all_rules, key=lambda x: x['confidence'], reverse=True)[:5]
    for idx, rule in enumerate(top_by_conf, 1):
        ante_str = ','.join([feature_names[i] for i in rule['antecedent']])
        cons_str = ','.join([feature_names[i] for i in rule['consequent']])
        print(f"\n{idx}. {{{ante_str}}} -> {{{cons_str}}}")
        print(f"   Support: {rule['support']:.4f} ({rule['support']*100:.2f}%)")
        print(f"   Confidence: {rule['confidence']:.4f} ({rule['confidence']*100:.2f}%)")
        print(f"   Lift: {rule['lift']:.4f}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)