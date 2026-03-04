def first():
    def second():
        def third():
            def fourth():
                return 3
            return fourth() * 4
        return third() + 5
    return second() * 2
print(first())
