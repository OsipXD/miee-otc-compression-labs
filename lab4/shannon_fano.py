def shannon_fano(probabilities):
    from collections import namedtuple
    Node = namedtuple('Node', 'symbol probability')
    branch = Branch([Node(symbol, probability)
                     for symbol, probability in probabilities])
    tree = divide_to_branches(branch)
    return tree_to_dict(tree)


def divide_to_branches(branch):
    if len(branch.leaves) == 1:
        code = '0' if len(branch.code) == 0 else branch.code
        return [(branch.leaves[0].symbol, code)]
    if len(branch.leaves) == 2:
        return [(branch.leaves[0].symbol, branch.code + '0'),
                (branch.leaves[1].symbol, branch.code + '1')]
    left = Branch([branch.leaves[0]], branch.code + '0')
    right = Branch(branch.leaves[1:], branch.code + '1')
    while(abs(sum_probs(left.leaves) - \
              sum_probs(right.leaves)) > \
          abs((sum_probs(left.leaves) + right.leaves[0].probability) - \
              (sum_probs(right.leaves) - right.leaves[0].probability))):
        left.leaves.append(right.leaves.pop(0))
    return [divide_to_branches(left), divide_to_branches(right)]


def sum_probs(leaves):
    return sum([probability for symbol, probability in leaves])


def tree_to_dict(branch, chain=[]):
    for item in branch:
        if type(item) == tuple:
            chain.append(item)
        if type(item) == list:
           tree_to_dict(item, chain)
    return dict(chain)


class Branch:
    def __init__(self, leaves, code=''):
        self.leaves = leaves
        self.code = code
