import fractions

def is_it_true(anything):
    if anything:
        print("yes, it's true")
    else:
        print("no, it's false")

is_it_true(1)
is_it_true(-1)
is_it_true(0)
is_it_true(0.1)
is_it_true(fractions.Fraction(1, 2))
is_it_true(fractions.Fraction(0, 1))