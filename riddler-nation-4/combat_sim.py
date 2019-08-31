import csv, sys, random

submissions = []

def load_submissions(filename):
    reader = csv.reader(open(filename, mode='r', newline=''), delimiter=',', quotechar='\"')
    for row in reader:
        val = parse_line(row)
        if val is None:
            continue
        submissions.append(val)
    print("submissions: ", len(submissions))

def parse_line(line):
    ret = []
    for i in range(10):
        if line[i].isdigit():
            ret.append(int(line[i]))
        else:
            return None
    if sum(ret) != 100:
        return None
    return ret

# return true if subject beats opponent.
def is_win(subject, opponent):
    score_subject = 0
    score_opponent = 0
    for i in range(len(subject)):
        if subject[i] > opponent[i]:
            score_subject += i + 1
        if subject[i] < opponent[i]:
            score_opponent += i + 1
        if subject[i] == opponent[i]:
            score_subject += (i + 1) / 2
            score_opponent += (i + 1) / 2
    return score_subject > score_opponent


def count_wins(subject):
    if subject is None:
        return 0
    count = 0
    for submission in submissions:
        if is_win(subject, submission):
            count += 1
    return count

def print_best_submission():
    best = []
    best_count = 0
    for submission in submissions:
        curr_count = count_wins(submission)
        if curr_count > best_count:
            best_count = curr_count
            best = submission
            print("curr best submission: {}, count: {}".format(submission, curr_count))

    print("Best submission: {}, wins: {}, total: {}, percent: {}".format(
        best, best_count, len(submissions), 100.0 * best_count / len(submissions)
    ))

def hillclimb(submission, iterations=100):
    curr_submission = submission
    curr_wins = count_wins(curr_submission)

    for i in range(iterations):
        print("Curr submission: {}, iteration: {}, count: {}".format(curr_submission, i, curr_wins))
        done = True
        for neighbor in get_neighbors(curr_submission):
            neighbor_wins = count_wins(neighbor)
            if neighbor_wins > curr_wins:
                curr_submission = neighbor
                curr_wins = neighbor_wins
                done = False
        if done:
            break
    return curr_submission

def get_neighbors(submission):
    neighbors = []
    for i in range(10):
        for d in range(10):
            if d == i:
                # avoid incrementing and decrementing same position.
                continue
            new_neighbor = submission.copy()
            if new_neighbor[d] == 0:
                continue
            if new_neighbor[i] == 100:
                continue
            new_neighbor[i] += 1
            new_neighbor[d] -= 1
            neighbors.append(new_neighbor)
    return neighbors

def gen_random_submission():
    submission = []
    total_points = 100
    for i in range(9):
        # val = random.randrange(0, min(3 * (i + 1), total_points))
        val = random.randrange(0, min(25, total_points))
        total_points -= val
        submission.append(val)
    submission.append(total_points)


    assert(sum(submission) == 100)
    return submission

def main():
    load_submissions(sys.argv[1])
    print_best_submission()
    if len(sys.argv) > 2:
        user_submission_str = sys.argv[2]
        user_submission = parse_line(user_submission_str.split(","))

        # count = count_wins(user_submission)
        # print("Submission {} won {} times out of {}, percent: {}".format(user_submission, count, len(submissions), 100.0 * count / len(submissions)))

        # Hill climb
        hillclimb_solution = hillclimb(user_submission)
        count = count_wins(hillclimb_solution)
        print("Submission {} won {} times out of {}, percent: {}".format(hillclimb_solution, count, len(submissions), 100.0 * count / len(submissions)))

    else:
        try:
            best_solution = []
            best_count = 0
            while True:
                curr_solution = hillclimb(gen_random_submission())
                curr_count = count_wins(curr_solution)
                if curr_count > best_count:
                    best_solution = curr_solution
                    best_count = curr_count
                print("curr best solution: {}, {}/{} {}%".format(best_solution, best_count, len(submissions), 100.0 * best_count / len(submissions)))
        except KeyboardInterrupt:
            print("curr best solution: {}, {}/{} {}%".format(best_solution, best_count, len(submissions), 100.0 * best_count / len(submissions)))

if __name__ == "__main__":
    main()