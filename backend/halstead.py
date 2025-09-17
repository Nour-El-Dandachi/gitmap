# halstead.py
import sys, json, re, math

def halstead_metrics(code: str):
    operators = re.findall(r"[=+\-*/<>%!&|^]+|\b(if|else|for|while|return|def|class|import)\b", code)
    operands = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b|\b\d+\b", code)

    uniq_op = len(set(operators))
    uniq_opnd = len(set(operands))
    total_op = len(operators)
    total_opnd = len(operands)

    n = total_op + total_opnd
    vocab = uniq_op + uniq_opnd
    v = 0 if vocab == 0 else n * math.log2(vocab)
    l = n
    d = 0 if uniq_opnd == 0 else (uniq_op / 2) * (total_opnd / uniq_opnd)
    i = 0 if d == 0 else v / d
    e = d * v
    b = v / 3000 if v else 0
    t = e / 18 if e else 0

    return {
        "uniq_op": uniq_op,
        "uniq_opnd": uniq_opnd,
        "total_op": total_op,
        "total_opnd": total_opnd,
        "n": n,
        "v": v,
        "l": l,
        "d": d,
        "i": i,
        "e": e,
        "b": b,
        "t": t,
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python halstead.py <file>")
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    metrics = halstead_metrics(code)
    print(json.dumps(metrics))
