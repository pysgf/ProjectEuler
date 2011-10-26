def fib(n):
    memo_dict = {0:1, 1:1}
    def __aux(n):
        if n not in memo_dict:
            memo_dict[n] = __aux(n - 1) + __aux(n - 2)
        return memo_dict[n]
    return __aux(n)

