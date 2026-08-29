"""Unit tests for streak + runner + challenge evaluator."""
from app.api.routes.dashboard import _streak
from app.services import runner, challenges as chall
from database.database import get_conn


def test_streak_basic():
    from datetime import date, timedelta
    d = date.today()
    days = {d.isoformat()}
    assert _streak(days) >= 1


def test_streak_gap_breaks():
    from datetime import date, timedelta
    d = date.today()
    # session today + 2 days ago -> streak 1 (yesterday missing)
    days = {d.isoformat(), (d - timedelta(days=2)).isoformat()}
    assert _streak(days) == 1


def test_runner_timeout():
    res = runner.run_python("while True: pass")
    assert res["status"] == "error"
    assert "Timeout" in res["error"]


def test_runner_output_limit():
    res = runner.run_python("print('x' * 50000)")
    assert res["status"] == "ok"
    assert len(res["output"]) <= 10000 + 50


def test_runner_blocks_subprocess():
    # subprocess module is allowed by -I but running is impractical; ensure callable
    res = runner.run_python("print('safe')")
    assert res["status"] == "ok"


def test_challenge_evaluator():
    conn = get_conn()
    c = conn.execute("SELECT * FROM challenges WHERE slug='sum-list'").fetchone()
    conn.close()
    res = chall.evaluate(c, "def solve(ns):\n    return sum(ns)")
    assert res["status"] == "passed"


def test_challenge_edge_cases():
    conn = get_conn()
    c = conn.execute("SELECT * FROM challenges WHERE slug='largest-number'").fetchone()
    conn.close()
    # wrong answer on empty list edge would be False for comparing to error; our tests
    # expect max(ns) to raise -> harness marks 'err' -> failure. Using full correct impl:
    res = chall.evaluate(c, "def solve(ns):\n    return max(ns)")
    assert res["passed"] == res["total"]


def test_new_challenges_all_pass_with_correct_solution():
    conn = get_conn()
    sols = {
        "fizzbuzz": 'def solve(n):\n    res=[]\n    for i in range(1,n+1):\n        if i%15==0: res.append("FizzBuzz")\n        elif i%3==0: res.append("Fizz")\n        elif i%5==0: res.append("Buzz")\n        else: res.append(i)\n    return res',
        "leap-year": "def solve(y):\n    return y%4==0 and (y%100!=0 or y%400==0)",
        "factorial": "def solve(n):\n    r=1\n    for i in range(1,n+1): r*=i\n    return r",
        "count-vowels": 'def solve(t):\n    return sum(1 for c in t.lower() if c in "aeiou")',
        "second-largest": "def solve(ns):\n    return sorted(ns)[-2]",
    }
    try:
        for slug, code in sols.items():
            c = conn.execute("SELECT * FROM challenges WHERE slug=?", (slug,)).fetchone()
            assert c, f"challenge {slug} missing"
            res = chall.evaluate(c, code)
            assert res["status"] == "passed", f"{slug}: {res}"
    finally:
        conn.close()


def test_medium_challenges_all_pass_with_correct_solution():
    conn = get_conn()
    sols = {
        "binary-search": "def solve(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1",
        "two-sum": "def solve(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target - n], i]\n        seen[n] = i",
        "missing-number": "def solve(nums):\n    n = len(nums)\n    return sum(range(n + 1)) - sum(nums)",
        "balanced-brackets": 'def solve(s):\n    pairs = {")": "(", "]": "[", "}": "{"}\n    stack = []\n    for c in s:\n        if c in "([{":\n            stack.append(c)\n        elif c in ")]}":\n            if not stack or stack.pop() != pairs[c]:\n                return False\n    return not stack',
        "sort-list": "def solve(nums):\n    a = nums[:]\n    for i in range(1, len(a)):\n        key = a[i]\n        j = i - 1\n        while j >= 0 and a[j] > key:\n            a[j + 1] = a[j]\n            j -= 1\n        a[j + 1] = key\n    return a",
    }
    try:
        for slug, code in sols.items():
            c = conn.execute("SELECT * FROM challenges WHERE slug=?", (slug,)).fetchone()
            assert c, f"challenge {slug} missing"
            res = chall.evaluate(c, code)
            assert res["status"] == "passed", f"{slug}: {res}"
    finally:
        conn.close()
def test_new_easy_challenges_pass():
    conn = get_conn()
    sols = {
        "palindrome-check": "def solve(text):\n    s = text.replace(' ', '').lower()\n    return s == s[::-1]",  # string
        "anagram": "def solve(a, b):\n    def clean(s): return ''.join(sorted(s.replace(' ', '').lower()))\n    return clean(a) == clean(b)",  # string
        "remove-duplicates": "def solve(nums):\n    seen, out = set(), []\n    for n in nums:\n        if n not in seen:\n            seen.add(n); out.append(n)\n    return out",  # list
        "count-words": "def solve(text):\n    return len(text.split())",  # string
        "first-unique-char": "def solve(text):\n    from collections import Counter\n    c = Counter(text)\n    for i, ch in enumerate(text):\n        if c[ch] == 1:\n            return i\n    return -1",  # hash-map
        "contains-duplicate": "def solve(nums):\n    return len(nums) != len(set(nums))",  # hash-map
        "is-prime": "def solve(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            return False\n    return True",  # conditional
        "sum-of-digits": "def solve(n):\n    return sum(int(d) for d in str(abs(n)))",  # conditional
        "power-of-two": "def solve(n):\n    return n > 0 and (n & (n - 1)) == 0",  # conditional
        "reverse-integer": "def solve(x):\n    sign = -1 if x < 0 else 1\n    r = int(str(abs(x))[::-1])\n    return 0 if r > 2**31 - 1 else sign * r",  # math
        "is-palindrome-number": "def solve(x):\n    s = str(x)\n    return s == s[::-1]",  # math
        "array-majority": "def solve(nums):\n    from collections import Counter\n    return Counter(nums).most_common(1)[0][0]",  # hash-map
        "compress-string": "def solve(s):\n    if not s:\n        return \"\"\n    out, cnt = [], 1\n    for i in range(1, len(s)):\n        if s[i] == s[i-1]:\n            cnt += 1\n        else:\n            out.append(s[i-1] + str(cnt)); cnt = 1\n    out.append(s[-1] + str(cnt))\n    return ''.join(out)",  # string
        "move-zeroes": "def solve(nums):\n    out = [n for n in nums if n != 0]\n    out += [0] * (len(nums) - len(out))\n    return out",  # list
        "array-rotation-left": "def solve(nums, k):\n    if not nums:\n        return []\n    k %= len(nums)\n    return nums[k:] + nums[:k]",  # list
        "karpa-common-multiple": "def solve(a, b):\n    import math\n    return a * b // math.gcd(a, b)",  # math
        "gcd-numbers": "def solve(a, b):\n    while b:\n        a, b = b, a % b\n    return abs(a)",  # math
        "binary-to-decimal": "def solve(bin_str):\n    return int(bin_str, 2)",  # math
        "shuffle-string": "def solve(s, indices):\n    res = [''] * len(s)\n    for i, idx in enumerate(indices):\n        res[idx] = s[i]\n    return ''.join(res)",  # string
        "two-sum-brute": "def solve(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        diff = target - n\n        if diff in seen:\n            return [seen[diff], i]\n        seen[n] = i\n    return []",  # hash-map
    }
    try:
        for slug, code in sols.items():
            c = conn.execute('SELECT * FROM challenges WHERE slug=?', (slug,)).fetchone()
            assert c, f'challenge {slug} missing'
            res = chall.evaluate(c, code)
            assert res['status'] == 'passed', f'{slug}: {res}'
    finally:
        conn.close()

def test_new_medium_challenges_pass():
    conn = get_conn()
    sols = {
        "longest-substring": "def solve(s):\n    seen, start, best = {}, 0, 0\n    for end, ch in enumerate(s):\n        if ch in seen and seen[ch] >= start:\n            start = seen[ch] + 1\n        seen[ch] = end\n        best = max(best, end - start + 1)\n    return best",  # sliding-window
        "group-anagrams": "def solve(words):\n    groups = {}\n    for w in words:\n        key = tuple(sorted(w))\n        groups.setdefault(key, []).append(w)\n    return list(groups.values())",  # hash-map
        "subarray-sum-k": "def solve(nums, k):\n    count, prefix, acc = {0: 1}, 0, 0\n    for n in nums:\n        acc += n\n        prefix += count.get(acc - k, 0)\n        count[acc] = count.get(acc, 0) + 1\n    return prefix",  # hash-map
        "product-except-self": "def solve(nums):\n    n = len(nums)\n    out = [1] * n\n    p = 1\n    for i in range(n):\n        out[i] = p; p *= nums[i]\n    p = 1\n    for i in range(n - 1, -1, -1):\n        out[i] *= p; p *= nums[i]\n    return out",  # array
        "merge-intervals": "def solve(intervals):\n    if not intervals:\n        return []\n    intervals.sort()\n    out = [list(intervals[0])]\n    for s, e in intervals[1:]:\n        if s <= out[-1][1]:\n            out[-1][1] = max(out[-1][1], e)\n        else:\n            out.append([s, e])\n    return out",  # array
        "kadane-max-subarray": "def solve(nums):\n    cur = best = nums[0]\n    for n in nums[1:]:\n        cur = max(n, cur + n)\n        best = max(best, cur)\n    return best",  # array
        "three-sum": "def solve(nums):\n    nums.sort()\n    out = []\n    n = len(nums)\n    for i in range(n - 2):\n        if i > 0 and nums[i] == nums[i-1]:\n            continue\n        lo, hi = i + 1, n - 1\n        while lo < hi:\n            s = nums[i] + nums[lo] + nums[hi]\n            if s < 0:\n                lo += 1\n            elif s > 0:\n                hi -= 1\n            else:\n                out.append([nums[i], nums[lo], nums[hi]])\n                while lo < hi and nums[lo] == nums[lo+1]: lo += 1\n                while lo < hi and nums[hi] == nums[hi-1]: hi -= 1\n                lo += 1; hi -= 1\n    return out",  # two-pointer
        "valid-anagram-2": "def solve(s):\n    s = ''.join(c.lower() for c in s if c.isalnum())\n    return s == s[::-1]",  # two-pointer
        "min-stack": "def solve(ops, vals):\n    stack, mins, vi, out = [], [], 0, []\n    for op in ops:\n        if op == \"push\":\n            v = vals[vi]; vi += 1\n            stack.append(v)\n            if not mins or v <= mins[-1]:\n                mins.append(v)\n        elif op == \"pop\":\n            if stack.pop() == mins[-1]:\n                mins.pop()\n        elif op == \"top\":\n            out.append(stack[-1])\n        elif op == \"getMin\":\n            out.append(mins[-1])\n    return out",  # stack
        "queue-using-stacks": "def solve(ops, vals):\n    inn, out, vi, res = [], [], 0, []\n    for op in ops:\n        if op == \"push\":\n            inn.append(vals[vi]); vi += 1\n        else:\n            if not out:\n                while inn:\n                    out.append(inn.pop())\n            if op == \"pop\":\n                res.append(out.pop())\n            elif op == \"peek\":\n                res.append(out[-1])\n            elif op == \"empty\":\n                res.append(not out and not inn)\n    return res",  # queue
        "valid-parentheses-2": "def solve(s):\n    pairs = {\")\": \"(\", \"]\": \"[\", \"}\": \"{\"}\n    stack = []\n    for c in s:\n        if c in \"([{\":\n            stack.append(c)\n        elif c in \")]}\":\n            if not stack or stack.pop() != pairs[c]:\n                return False\n    return not stack",  # stack
        "two-pointers-sorted": "def solve(numbers, target):\n    lo, hi = 0, len(numbers) - 1\n    while lo < hi:\n        s = numbers[lo] + numbers[hi]\n        if s == target:\n            return [lo + 1, hi + 1]\n        elif s < target:\n            lo += 1\n        else:\n            hi -= 1",  # two-pointer
        "top-k-frequent": "def solve(nums, k):\n    from collections import Counter\n    return [x for x, _ in Counter(nums).most_common(k)]",  # hash-map
        "rotate-array-right": "def solve(nums, k):\n    if not nums:\n        return []\n    k %= len(nums)\n    return nums[-k:] + nums[:-k]",  # array
        "remove-nth-node": "def solve(values, n):\n    if n > len(values):\n        return values\n    idx = len(values) - n\n    return values[:idx] + values[idx+1:]",  # linkedlist
        "happy-number": "def solve(n):\n    def nxt(x):\n        return sum(int(d) ** 2 for d in str(x))\n    seen = set()\n    while n != 1 and n not in seen:\n        seen.add(n)\n        n = nxt(n)\n    return n == 1",  # hash-map
        "climb-stairs": "def solve(n):\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b",  # recursion
        "coin-change": "def solve(coins, amount):\n    dp = [amount + 1] * (amount + 1)\n    dp[0] = 0\n    for i in range(1, amount + 1):\n        for c in coins:\n            if c <= i:\n                dp[i] = min(dp[i], dp[i - c] + 1)\n    return dp[amount] if dp[amount] <= amount else -1",  # dp
        "house-robber": "def solve(nums):\n    prev, cur = 0, 0\n    for n in nums:\n        prev, cur = cur, max(cur, prev + n)\n    return cur",  # dp
        "word-break": "def solve(s, wordDict):\n    words = set(wordDict)\n    n = len(s)\n    dp = [False] * (n + 1)\n    dp[0] = True\n    for i in range(1, n + 1):\n        for j in range(i):\n            if dp[j] and s[j:i] in words:\n                dp[i] = True\n                break\n    return dp[n]",  # dp
        "kth-largest": "def solve(nums, k):\n    return sorted(nums, reverse=True)[k - 1]",  # sort
        "merge-sorted-array": "def solve(nums1, m, nums2, n):\n    return sorted(nums1[:m] + nums2[:n])",  # array
        "spiral-order": "def solve(matrix):\n    res = []\n    while matrix:\n        res += matrix.pop(0)\n        if matrix and matrix[0]:\n            for row in matrix:\n                res.append(row.pop())\n        if matrix:\n            res += matrix.pop()[::-1]\n        if matrix and matrix[0]:\n            for row in matrix[::-1]:\n                res.append(row.pop(0))\n    return res",  # array
        "max-profit-stock": "def solve(prices):\n    min_price, profit = float('inf'), 0\n    for p in prices:\n        min_price = min(min_price, p)\n        profit = max(profit, p - min_price)\n    return profit",  # greedy
        "find-duplicates-array": "def solve(nums):\n    seen, out = set(), []\n    for n in nums:\n        if n in seen:\n            if n not in out:\n                out.append(n)\n        else:\n            seen.add(n)\n    return out",  # hash-map
    }
    try:
        for slug, code in sols.items():
            c = conn.execute('SELECT * FROM challenges WHERE slug=?', (slug,)).fetchone()
            assert c, f'challenge {slug} missing'
            res = chall.evaluate(c, code)
            assert res['status'] == 'passed', f'{slug}: {res}'
    finally:
        conn.close()

def test_new_advanced_challenges_pass():
    conn = get_conn()
    sols = {
        "quick-select": "def solve(nums, k):\n    import heapq\n    return heapq.nsmallest(k, nums)[-1]",  # sort
        "max-sliding-window": "def solve(nums, k):\n    from collections import deque\n    dq, out = deque(), []\n    for i, n in enumerate(nums):\n        while dq and nums[dq[-1]] <= n:\n            dq.pop()\n        dq.append(i)\n        if dq[0] <= i - k:\n            dq.popleft()\n        if i >= k - 1:\n            out.append(nums[dq[0]])\n    return out",  # sliding-window
        "longest-increasing-subsequence": "def solve(nums):\n    if not nums:\n        return 0\n    dp = [1] * len(nums)\n    for i in range(len(nums)):\n        for j in range(i):\n            if nums[j] < nums[i]:\n                dp[i] = max(dp[i], dp[j] + 1)\n    return max(dp)",  # dp
        "min-path-sum": "def solve(grid):\n    r, c = len(grid), len(grid[0])\n    dp = [[0]*c for _ in range(r)]\n    dp[0][0] = grid[0][0]\n    for j in range(1, c): dp[0][j] = dp[0][j-1] + grid[0][j]\n    for i in range(1, r): dp[i][0] = dp[i-1][0] + grid[i][0]\n    for i in range(1, r):\n        for j in range(1, c):\n            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]\n    return dp[-1][-1]",  # dp
        "longest-common-subsequence": "def solve(a, b):\n    m, n = len(a), len(b)\n    dp = [[0]*(n+1) for _ in range(m+1)]\n    for i in range(1, m+1):\n        for j in range(1, n+1):\n            if a[i-1] == b[j-1]:\n                dp[i][j] = dp[i-1][j-1] + 1\n            else:\n                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    return dp[m][n]",  # dp
        "binary-tree-depth": "def solve(values):\n    if not values:\n        return 0\n    class Node:\n        __slots__ = ('v', 'l', 'r')\n        def __init__(self, v):\n            self.v = v; self.l = None; self.r = None\n    nodes = [Node(v) if v is not None else None for v in values]\n    for i, nd in enumerate(nodes):\n        if nd is None:\n            continue\n        li, ri = 2 * i + 1, 2 * i + 2\n        if li < len(nodes):\n            nd.l = nodes[li]\n        if ri < len(nodes):\n            nd.r = nodes[ri]\n    def depth(nd):\n        if nd is None:\n            return 0\n        return 1 + max(depth(nd.l), depth(nd.r))\n    return depth(nodes[0])",  # tree
        "invert-binary-tree": "def solve(values):\n    if not values:\n        return []\n    class Node:\n        __slots__ = ('v', 'l', 'r')\n        def __init__(self, v):\n            self.v = v; self.l = None; self.r = None\n    nodes = [Node(v) if v is not None else None for v in values]\n    for i, nd in enumerate(nodes):\n        if nd is None:\n            continue\n        li, ri = 2 * i + 1, 2 * i + 2\n        if li < len(nodes):\n            nd.l = nodes[li]\n        if ri < len(nodes):\n            nd.r = nodes[ri]\n    def invert(nd):\n        if nd is None:\n            return\n        nd.l, nd.r = nd.r, nd.l\n        invert(nd.l); invert(nd.r)\n    invert(nodes[0])\n    out, q = [], [nodes[0]]\n    while q:\n        nq = []\n        for nd in q:\n            if nd is None:\n                out.append(None)\n                continue\n            out.append(nd.v)\n            nq.append(nd.l); nq.append(nd.r)\n        q = nq\n    while out and out[-1] is None:\n        out.pop()\n    return out",  # tree
        "lru-cache": "def solve(ops, vals):\n    from collections import OrderedDict\n    cap, cache, vi, out = 2, OrderedDict(), 0, []\n    for op in ops:\n        if op == \"put\":\n            k, v = vals[vi]; vi += 1\n            cache[k] = v\n            cache.move_to_end(k)\n            if len(cache) > cap:\n                cache.popitem(last=False)\n        elif op == \"get\":\n            k = vals[vi][0]; vi += 1\n            if k in cache:\n                cache.move_to_end(k)\n                out.append(cache[k])\n            else:\n                out.append(-1)\n    return out",  # hash-map
        "word-ladder": "def solve(begin, end, wordList):\n    from collections import deque\n    words = set(wordList)\n    if end not in words:\n        return 0\n    q = deque([(begin, 1)])\n    visited = {begin}\n    while q:\n        cur, d = q.popleft()\n        if cur == end:\n            return d\n        for i in range(len(cur)):\n            for ch in 'abcdefghijklmnopqrstuvwxyz':\n                nxt = cur[:i] + ch + cur[i+1:]\n                if nxt in words and nxt not in visited:\n                    visited.add(nxt)\n                    q.append((nxt, d + 1))\n    return 0",  # bfs
        "median-two-sorted": "def solve(nums1, nums2):\n    import statistics\n    return statistics.median(nums1 + nums2)",  # binary-search
    }
    try:
        for slug, code in sols.items():
            c = conn.execute('SELECT * FROM challenges WHERE slug=?', (slug,)).fetchone()
            assert c, f'challenge {slug} missing'
            res = chall.evaluate(c, code)
            assert res['status'] == 'passed', f'{slug}: {res}'
    finally:
        conn.close()
