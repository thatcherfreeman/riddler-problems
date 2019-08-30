### Banknote problem
# Solution by Thatcher
# Requires python 3.
from math import factorial, ceil

def main():
    best = (-1, -1)
    for i in range(0, 100):
        # Expected value for i fake bills is 0*(1-prob) + (winnings)*(prob)
        expected_value = ((i + 25) * 100) * calc_prob(i, 25, 0.05, 0.25)
        print("num fake bills: {} expected value: {}".format(i, expected_value))
        # Choose number of fake bills with the best expected value.
        if expected_value > best[1]:
            best = (i, expected_value)
    print("Best: {}".format(best))

def calc_prob(num_fake_bills, num_real_bills, sample_frac, detection_rate):
    num_sample_bills = ceil((num_fake_bills + num_real_bills) * sample_frac)
    num_total_bills = num_real_bills + num_fake_bills
    totalprob = 0
    # Sum probability that none of the fake bills is noticed in this set, for each possible number
    # of fake bills captured by the sample
    for i in range(0, num_sample_bills + 1):
        # Probability that *i* fake bills are in the sample
        # equals 
        # (number of ways to choose i of the fake bills) * (number of ways to choose (sample-i) of the real bills)
        # / (number of ways to sample all of the bills)
        prob = ncr(num_fake_bills, i) \
                * ncr(num_real_bills, num_sample_bills - i) \
                / ncr(num_total_bills, num_sample_bills)

        # Multiply by probability that none of the fake bills are noticed
        prob *= ((1 - detection_rate) ** i)

        # Add to running total, equals 
        # Pr(0 fake bills selected and detected) 
        # + Pr(1 fake bill selected and detected)
        # + Pr(2 fake bills selected and detected) 
        # + ...
        totalprob += prob
    return totalprob

def ncr(n, r):
    if r > n:
        return 0
    return factorial(n) / factorial(r) / factorial(n - r)

if __name__ == "__main__":
    main()