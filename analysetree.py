import re


def analysetree(tree: str):
    pattern = re.compile(r"^(?P<indent>(?:│   |    )*)([├└]── )(?P<name>.+)$")

    lines = tree.splitlines()
    stack = []
    result = []

    for line in lines:
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            indent = m.group("indent")
            name = m.group("name").strip()
            depth = len(indent) // 4 + 1
        else:
            depth = 0
            name = line.strip()
        while len(stack) > depth:
            stack.pop()
        if name.endswith(".cs"):
            if "TheGaulishEnigma" in stack:
                base_index = stack.index("TheGaulishEnigma")
                if len(stack) > base_index + 1:
                    full_path = "/".join(stack[base_index:] + [name])
                    result.append(full_path)
        else:
            stack.append(name)
    return result
