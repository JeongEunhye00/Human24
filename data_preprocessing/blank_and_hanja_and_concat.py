import hanja


def blank_and_hanja_and_concat(str1, concat_w):
    s = hanja.translate(str1, 'substitution')
    s = s.replace("(", " (").replace(")", ") ").replace("  (", " (").replace(")  ", ") ") \
        .replace("{", " {").replace("}", "} ").replace("[", " [").replace("]", "] ")\
        .replace(":", " :").replace("  :",  " :")
    s = s.replace("%uF98E", "연").replace("%uF9B5", "예")

    for c in concat_w:
        s = s.replace(c[0], c[1])
    s = s.strip()

    return s
