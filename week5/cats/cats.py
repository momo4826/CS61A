"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    cnt = 0
    for item in paragraphs:
        if select(item):
            if cnt == k:
                return item
            cnt += 1
    return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether
    a paragraph contains one of the words in TOPIC.

    Arguments:
        topic: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def checker(para):
        para_list = remove_punctuation(para).split(' ')
        para_list = [lower(x) for x in para_list]
        topic_list = [lower(x) for x in topic]
        for word in para_list:
            if word in topic_list:
                return True
        return False
    return checker
    # END PROBLEM 2
# about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
# print(pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0))


def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of SOURCE that was typed.

    Arguments:
        typed: a string that may contain typos
        source: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    source_words = split(source)
    #print(source_words)
    # BEGIN PROBLEM 3
    if len(source_words) == 0 and len(typed_words) == 0:
        return 100.0
    elif len(source_words) == 0 and len(typed_words) != 0:
        return 0.0
    elif len(source_words) != 0 and len(typed_words) == 0:
        return 0.0
    # elif len(source_words) == 1 and len(typed_words) == 1:
    #     if source_words[0] == typed_words[0]:
    #         return 100.0
    #     else:
    #         return 0.0
    else:
        return correct_counter(typed_words, source_words) / len(typed_words) * 100.0

    # END PROBLEM 3

def correct_counter(typed_words, source_words):
    if len(source_words) == 0:
        return 0
    elif len(typed_words) == 0:
        return 0
    else:
        if source_words[0] == typed_words[0]:
            return 1 + correct_counter(typed_words[1:], source_words[1:])
        else:
            return correct_counter(typed_words[1:], source_words[1:])

# print(accuracy('Cute Dog. I say!', 'Cute Dog.'))

def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    return len(typed) / 5 * 60 / elapsed

# print(wpm('hello friend hello buddy hello', 15))

###########
# Phase 2 #
###########

def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD. Instead returns TYPED_WORD if that difference is greater
    than LIMIT.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    if typed_word in word_list:
        return typed_word
    else:
        tmp = [diff_function(typed_word, word, limit) for word in word_list]
        if min(tmp) <= limit:
            return word_list[tmp.index(min(tmp))]
        else:
            return typed_word

# ten_diff = lambda w1, w2, limit: 10 # Always returns 10
# print(autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20))

def feline_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths and returns the result.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> feline_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> feline_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> feline_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> feline_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> feline_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    if limit < 0:
        return 1
    if len(source) == 0 or len(typed) == 0:
        return max(len(typed), len(source))
    else:
        if typed[0] == source[0]:
            return feline_fixes(typed[1:], source[1:], limit)
        else:
            return 1 + feline_fixes(typed[1:], source[1:], limit - 1)
    
# big_limit = 10
# print(feline_fixes("roses", "arose", big_limit))
# limit = 4
# print(feline_fixes("rosesabcdefghijklm", "arosenopqrstuvwxyz", limit))

def minimum_mewtations(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL.
    This function takes in a string START, a string GOAL, and a number LIMIT.
    Arguments:
        start: a starting word
        goal: a goal word
        limit: a number representing an upper bound on the number of edits
    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    if limit < 0:
        return 1
    if len(goal) == 0 or len(start) == 0:
        return max(len(start), len(goal))
    elif start == goal:
        return 0
    else:
        if start[0] == goal[0]:
            return minimum_mewtations(start[1:], goal[1:], limit)
        else:
            return 1 + min(minimum_mewtations(start[1:], goal, limit - 1), minimum_mewtations(goal[0] + start, goal, limit - 1), minimum_mewtations(goal[0] + start[1:], goal, limit - 1))

#print(minimum_mewtations("gest", "gestate", 10))

# when limit set to 6
# Correction Speed: 144.78768608693352 wpm
# Correctly Corrected: 78 words
# Incorrectly Corrected: 20 words
# Uncorrected: 12 words

def final_diff(start, goal, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""
    
    if limit < 0:
        return 1
    if len(goal) == 0 or len(start) == 0:
        return max(len(start), len(goal))
    elif start == goal:
        return 0
    else:
        if start[0] == goal[0]:
            return minimum_mewtations(start[1:], goal[1:], limit)
        else:
            if len(start) > 1:
                return 1 + min(final_diff(start[1:], goal, limit - 1), final_diff(goal[0] + start, goal, limit - 1), final_diff(goal[0] + start[1:], goal, limit - 1), final_diff(start[1] + start[0] + start[2:], goal, limit - 1))
            else:
                return 1 + min(final_diff(start[1:], goal, limit - 1), final_diff(goal[0] + start, goal, limit - 1), final_diff(goal[0] + start[1:], goal, limit - 1))

FINAL_DIFF_LIMIT = 6  
# Correction Speed: 70.8338887863932 wpm
# Correctly Corrected: 43 words
# Incorrectly Corrected: 7 words
# Uncorrected: 4 words

###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        prompt: a list of the words in the typing prompt
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> prompt = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, prompt, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], prompt, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    if len(prompt) == 0:
        progress = 1.0
    elif len(typed) == 0:
        progress = 0.0
    else:
        progress = 0
        if typed[0] == prompt[0]:
            progress = (1 + report_progress(typed[1:], prompt[1:], user_id, lambda x: True) * (len(prompt)-1)) / len(prompt)
        else:
            progress = 0.0

    upload({'id': user_id, 'progress': progress})
    return progress

# print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
# typed = ['I', 'hve', 'begun', 'to', 'type']
# prompt = ['I', 'have', 'begun', 'to', 'type']
# report_progress(typed, prompt, 3, print_progress)


def time_per_word(words, times_per_player):
    """Given timing data, return a match dictionary, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> match["words"]
    ['collar', 'plush', 'blush', 'repute']
    >>> match["times"]
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    return match(words, [diff_helper(item) for item in times_per_player])

def diff_helper(times):
    res = []
    if len(times) < 2:
        return res
    for i in range(1, len(times)):
        res.append(times[i] - times[i-1])
    return res


def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match dictionary as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    # player_indices = range(len(get_all_times(match)))  # contains an *index* for each player
    # word_indices = range(len(get_all_words(match)))    # contains an *index* for each word
    player_num = len(get_all_times(match))
    word_num = len(get_all_words(match))

    times = [list(item) for item in zip(*get_all_times(match))]
    words = get_all_words(match)
    res = [[] for _ in range(player_num)]
    for i in range(word_num):
        min_player = times[i].index(min(times[i]))
        res[min_player].append(words[i])

    return res

def match(words, times):
    """A dictionary containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return {"words": words, "times": times}


def get_word(match, word_index):
    """A utility function that gets the word with index word_index"""
    assert 0 <= word_index < len(match["words"]), "word_index out of range of words"
    return match["words"][word_index]


def time(match, player_num, word_index):
    """A utility function for the time it took player_num to type the word at word_index"""
    assert word_index < len(match["words"]), "word_index out of range of words"
    assert player_num < len(match["times"]), "player_num out of range of players"
    return match["times"][player_num][word_index]


def get_all_words(match):
    """A selector function for all the words in the match"""
    return match["words"]


def get_all_times(match):
    """A selector function for all typing times for all players"""
    return match["times"]


def match_string(match):
    """A helper function that takes in a match dictionary and returns a string representation of it"""
    return f"match({match['words']}, {match['times']})"


enable_multiplayer = False  # Change to True when you're ready to race.


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, source))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
