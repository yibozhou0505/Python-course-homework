import time
import sys

# 固定常量（严格按作业要求）
EXTRA_INSERTS = [
    250001, 250003, 250005, 250007, 250009,
    250011, 250013, 250015, 250017, 250019
]

# ------------------------------
# 1. 二叉搜索树 BST
# ------------------------------
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        print(f"BUILD BST INSERT {key}")
        if self.root is None:
            self.root = BSTNode(key)
            return
        curr = self.root
        while True:
            if key < curr.key:
                if curr.left is None:
                    curr.left = BSTNode(key)
                    break
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = BSTNode(key)
                    break
                curr = curr.right

    def search(self, key):
        steps = 0
        curr = self.root
        while curr is not None:
            steps += 1
            if key == curr.key:
                return True, steps
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        steps += 1
        return False, steps

    def delete(self, key):
        parent = None
        curr = self.root
        while curr is not None and curr.key != key:
            parent = curr
            curr = curr.left if key < curr.key else curr.right
        if curr is None:
            return

        # 叶子或单孩子
        if curr.left is None or curr.right is None:
            child = curr.left if curr.left is not None else curr.right
            if parent is None:
                self.root = child
            elif parent.left == curr:
                parent.left = child
            else:
                parent.right = child
        else:
            # 找后继
            succ_parent = curr
            succ = curr.right
            while succ.left is not None:
                succ_parent = succ
                succ = succ.left
            curr.key = succ.key
            if succ_parent == curr:
                succ_parent.right = succ.right
            else:
                succ_parent.left = succ.right

    def inorder(self, node, res):
        if node is not None:
            self.inorder(node.left, res)
            res.append(str(node.key))
            self.inorder(node.right, res)

    def get_inorder(self):
        res = []
        self.inorder(self.root, res)
        return res

# ------------------------------
# 2. AVL 树
# ------------------------------
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, key):
        print(f"BUILD AVL INSERT {key}")
        def _insert(node, k):
            if node is None:
                return AVLNode(k)
            if k < node.key:
                node.left = _insert(node.left, k)
            else:
                node.right = _insert(node.right, k)

            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
            bal = self.get_balance(node)

            # LL
            if bal > 1 and k < node.left.key:
                return self.right_rotate(node)
            # RR
            if bal < -1 and k > node.right.key:
                return self.left_rotate(node)
            # LR
            if bal > 1 and k > node.left.key:
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)
            # RL
            if bal < -1 and k < node.right.key:
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)
            return node
        self.root = _insert(self.root, key)

    def search(self, key):
        steps = 0
        curr = self.root
        while curr is not None:
            steps += 1
            if key == curr.key:
                return True, steps
            curr = curr.left if key < curr.key else curr.right
        steps += 1
        return False, steps

    def get_min_node(self, node):
        curr = node
        while curr.left is not None:
            curr = curr.left
        return curr

    def delete(self, key):
        def _delete(node, k):
            if node is None:
                return node
            if k < node.key:
                node.left = _delete(node.left, k)
            elif k > node.key:
                node.right = _delete(node.right, k)
            else:
                if node.left is None or node.right is None:
                    temp = node.left if node.left else node.right
                    node = temp
                else:
                    temp = self.get_min_node(node.right)
                    node.key = temp.key
                    node.right = _delete(node.right, temp.key)
            if node is None:
                return node
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
            bal = self.get_balance(node)
            if bal > 1 and self.get_balance(node.left) >= 0:
                return self.right_rotate(node)
            if bal > 1 and self.get_balance(node.left) < 0:
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)
            if bal < -1 and self.get_balance(node.right) <= 0:
                return self.left_rotate(node)
            if bal < -1 and self.get_balance(node.right) > 0:
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)
            return node
        self.root = _delete(self.root, key)

    def inorder(self, node, res):
        if node is not None:
            self.inorder(node.left, res)
            res.append(str(node.key))
            self.inorder(node.right, res)

    def get_inorder(self):
        res = []
        self.inorder(self.root, res)
        return res

# ------------------------------
# 3. 伸展树 Splay Tree
# ------------------------------
class SplayNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def splay(self, key):
        if self.root is None:
            return
        header = SplayNode(0)
        left = right = header
        root = self.root
        while True:
            if key < root.key:
                if root.left is None:
                    break
                if key < root.left.key:
                    root = self.right_rotate(root)
                    if root.left is None:
                        break
                right.left = root
                right = root
                root = root.left
            elif key > root.key:
                if root.right is None:
                    break
                if key > root.right.key:
                    root = self.left_rotate(root)
                    if root.right is None:
                        break
                left.right = root
                left = root
                root = root.right
            else:
                break
        left.right = root.left
        right.left = root.right
        root.left = header.right
        root.right = header.left
        self.root = root

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def insert(self, key):
        print(f"BUILD SPLAY INSERT {key}")
        if self.root is None:
            self.root = SplayNode(key)
            return
        self.splay(key)
        if self.root.key == key:
            return
        node = SplayNode(key)
        if key < self.root.key:
            node.right = self.root
            node.left = self.root.left
            self.root.left = None
        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right = None
        self.root = node

    def search(self, key):
        steps = 0
        if self.root is None:
            return False, steps + 1
        curr = self.root
        while curr is not None:
            steps += 1
            if key == curr.key:
                self.splay(key)
                return True, steps
            curr = curr.left if key < curr.key else curr.right
        steps += 1
        self.splay(key)
        return False, steps

    def delete(self, key):
        if self.root is None:
            return
        self.splay(key)
        if self.root.key != key:
            return
        if self.root.left is None:
            self.root = self.root.right
        else:
            temp = self.root.right
            self.root = self.root.left
            self.splay(key)
            self.root.right = temp

    def inorder(self, node, res):
        if node is not None:
            self.inorder(node.left, res)
            res.append(str(node.key))
            self.inorder(node.right, res)

    def get_inorder(self):
        res = []
        self.inorder(self.root, res)
        return res

# ------------------------------
# 4. (2,4) 树（Two-Four Tree）
# ------------------------------
class TFNode:
    def __init__(self):
        self.keys = []
        self.children = []

class TwoFourTree:
    def __init__(self):
        self.root = TFNode()

    def insert(self, key):
        print(f"BUILD TF INSERT {key}")
        def _insert(node, k):
            if not node.children:
                node.keys.append(k)
                node.keys.sort()
                if len(node.keys) == 4:
                    mid = node.keys[1]
                    left = TFNode()
                    left.keys = node.keys[:1]
                    right = TFNode()
                    right.keys = node.keys[2:]
                    return mid, left, right
                return None, None, None
            for i in range(len(node.keys)):
                if k < node.keys[i]:
                    mk, ml, mr = _insert(node.children[i], k)
                    if mk is not None:
                        node.keys.insert(i, mk)
                        node.children[i] = ml
                        node.children.insert(i+1, mr)
                        if len(node.keys) == 4:
                            nm = node.keys[1]
                            nl = TFNode()
                            nl.keys = node.keys[:1]
                            nl.children = node.children[:2]
                            nr = TFNode()
                            nr.keys = node.keys[2:]
                            nr.children = node.children[2:]
                            return nm, nl, nr
                    return None, None, None
            mk, ml, mr = _insert(node.children[-1], k)
            if mk is not None:
                node.keys.append(mk)
                node.children[-1] = ml
                node.children.append(mr)
                if len(node.keys) == 4:
                    nm = node.keys[1]
                    nl = TFNode()
                    nl.keys = node.keys[:1]
                    nl.children = node.children[:2]
                    nr = TFNode()
                    nr.keys = node.keys[2:]
                    nr.children = node.children[2:]
                    return nm, nl, nr
            return None, None, None
        mk, ml, mr = _insert(self.root, key)
        if mk is not None:
            nr = TFNode()
            nr.keys = [mk]
            nr.children = [ml, mr]
            self.root = nr

    def search(self, key):
        steps = 0
        node = self.root
        while node is not None:
            steps += 1
            found = False
            for k in node.keys:
                steps += 1
                if k == key:
                    return True, steps
                if k > key:
                    break
            if not node.children:
                break
            go = len(node.children) - 1
            for i in range(len(node.keys)):
                if key < node.keys[i]:
                    go = i
                    break
            node = node.children[go]
        steps += 1
        return False, steps

    def delete(self, key):
        def _del(n, k):
            i = 0
            while i < len(n.keys) and k > n.keys[i]:
                i += 1
            if i < len(n.keys) and n.keys[i] == k:
                if not n.children:
                    n.keys.pop(i)
                    return
                succ = n.children[i+1]
                while succ.children:
                    succ = succ.children[0]
                sk = succ.keys[0]
                n.keys[i] = sk
                _del(n.children[i+1], sk)
                return
            if n.children:
                _del(n.children[i], k)
        _del(self.root, key)

    def inorder(self, node, res):
        for i in range(len(node.keys)):
            if i < len(node.children):
                self.inorder(node.children[i], res)
            res.append(str(node.keys[i]))
        if len(node.children) > len(node.keys):
            self.inorder(node.children[-1], res)

    def get_inorder(self):
        res = []
        self.inorder(self.root, res)
        return res

# ------------------------------
# 主流程（严格按作业输入输出）
# ------------------------------
def main():
    data = list(map(int, sys.stdin.read().split()))
    ptr = 0
    n = data[ptr]
    ptr += 1
    numbers = data[ptr:ptr + n]
    ptr += n

    # 固定查询/删除序列
    SEARCH_VALUES = [
        numbers[0], numbers[123], numbers[4321], numbers[9999],
        0, 200001, 250001, 135791
    ]
    DELETE_VALUES = [
        numbers[0], numbers[9999], numbers[5000],
        EXTRA_INSERTS[3], EXTRA_INSERTS[7]
    ]

    # 四棵树
    trees = {
        "BST": BST(),
        "AVL": AVL(),
        "SPLAY": SplayTree(),
        "TF": TwoFourTree()
    }
    tim = {t: {"build": 0, "search": 0, "insert": 0, "delete": 0} for t in trees}

    # 1. 建树
    for name, tree in trees.items():
        t0 = time.perf_counter()
        for num in numbers:
            tree.insert(num)
        tim[name]["build"] = time.perf_counter() - t0

    # 2. 中序 BUILD
    for name, tree in trees.items():
        seq = tree.get_inorder()
        print(f"RESULT INORDER {name} BUILD {' '.join(seq)}")

    # 3. 查询
    for name, tree in trees.items():
        t0 = time.perf_counter()
        for k in SEARCH_VALUES:
            fnd, st = tree.search(k)
            tag = "FOUND" if fnd else "NOT_FOUND"
            print(f"RESULT SEARCH {name} {k} {tag} {st}")
        tim[name]["search"] = time.perf_counter() - t0

    # 4. 额外插入
    for name, tree in trees.items():
        t0 = time.perf_counter()
        for num in EXTRA_INSERTS:
            tree.insert(num)
        tim[name]["insert"] = time.perf_counter() - t0

    # 5. 中序 AFTER_INSERT
    for name, tree in trees.items():
        seq = tree.get_inorder()
        print(f"RESULT INORDER {name} AFTER_INSERT {' '.join(seq)}")

    # 6. 删除
    for name, tree in trees.items():
        t0 = time.perf_counter()
        for num in DELETE_VALUES:
            tree.delete(num)
        tim[name]["delete"] = time.perf_counter() - t0

    # 7. 中序 AFTER_DELETE
    for name, tree in trees.items():
        seq = tree.get_inorder()
        print(f"RESULT INORDER {name} AFTER_DELETE {' '.join(seq)}")

    # 8. 输出时间
    for name in trees:
        b = tim[name]["build"]
        s = tim[name]["search"]
        i = tim[name]["insert"]
        d = tim[name]["delete"]
        total = b + s + i + d
        print(f"RESULT TIME {name} BUILD {b:.9f} SEARCH {s:.9f} INSERT {i:.9f} DELETE {d:.9f} TOTAL {total:.9f}")

if __name__ == "__main__":
    main()