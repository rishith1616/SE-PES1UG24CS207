def feedback(code, guess):
    exact = 0
    unmatched_code = []
    unmatched_guess = []

    # First pass: Identify and count exact matches
    for c, g in zip(code, guess):
        if c == g:
            exact += 1
        else:
            unmatched_code.append(c)
            unmatched_guess.append(g)

    partial = 0
    # Second pass: Identify partial matches using only unmatched symbols
    for g in unmatched_guess:
        if g in unmatched_code:
            partial += 1
            unmatched_code.remove(g)  # Consume the code symbol

    return exact, partial