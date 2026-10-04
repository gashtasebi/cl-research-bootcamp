from pathlib import Path
import tkinter as tk
from tkinter import ttk

from nltk import CFG, Tree
from nltk.parse import ChartParser


grammar = CFG.fromstring("""
S -> NP VP

NP -> Det N
NP -> Pronoun
NP -> NP PP

VP -> V
VP -> V NP
VP -> VP PP

PP -> P NP

Det -> 'the' | 'a'
N -> 'student' | 'book' | 'man' | 'telescope'
Pronoun -> 'I'
V -> 'reads' | 'saw'
P -> 'with'
""")

parser = ChartParser(grammar)

data_path = Path("data/grammar_test.txt")
sentences = [
    line.strip().split()
    for line in data_path.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

all_trees = []

print("=== CFG PARSING EXPERIMENT ===")
print()

for sentence in sentences:
    trees = list(parser.parse(sentence))

    print("Sentence:", " ".join(sentence))
    print("Number of parses:", len(trees))

    if not trees:
        print("Result: REJECTED")
    else:
        print("Result: ACCEPTED")

        for index, tree in enumerate(trees, start=1):
            print(f"Parse {index}:")
            print(tree)
            all_trees.append((" ".join(sentence), index, tree))

    print("-" * 60)

if all_trees:
    print()
    print("Opening graphical parse tree viewer...")

    root = tk.Tk()
    root.title("CFG Parse Tree Viewer")
    root.geometry("900x650")

    selector_frame = ttk.Frame(root, padding=10)
    selector_frame.pack(fill="x")

    tree_names = [
        f"{sentence} — Parse {parse_number}"
        for sentence, parse_number, _tree in all_trees
    ]
    selected_tree = tk.StringVar(value=tree_names[0])
    selector = ttk.Combobox(
        selector_frame,
        textvariable=selected_tree,
        values=tree_names,
        state="readonly",
    )
    selector.pack(fill="x")

    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    canvas = tk.Canvas(tree_frame, background="#f8fafc")
    vertical_scrollbar = ttk.Scrollbar(
        tree_frame, orient="vertical", command=canvas.yview
    )
    horizontal_scrollbar = ttk.Scrollbar(
        tree_frame, orient="horizontal", command=canvas.xview
    )
    canvas.configure(
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set,
    )

    vertical_scrollbar.pack(side="right", fill="y")
    horizontal_scrollbar.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)

    def draw_selected_tree(_event=None):
        canvas.delete("all")
        selected_index = tree_names.index(selected_tree.get())
        _sentence, _parse_number, tree = all_trees[selected_index]

        node_positions = {}
        x_gap = 105
        y_gap = 90
        left_margin = 50
        top_margin = 45

        # Leaves determine horizontal order; each upper node is centered over its children.
        leaf_counter = [0]

        def assign_positions(node, depth=0):
            if isinstance(node, Tree):
                child_positions = [assign_positions(child, depth + 1) for child in node]
                x = sum(child_positions) / len(child_positions)
            else:
                x = left_margin + leaf_counter[0] * x_gap
                leaf_counter[0] += 1
            node_positions[id(node)] = (x, top_margin + depth * y_gap)
            return x

        assign_positions(tree)

        def render(node):
            x, y = node_positions[id(node)]
            if isinstance(node, Tree):
                for child in node:
                    child_x, child_y = node_positions[id(child)]
                    canvas.create_line(x, y + 15, child_x, child_y - 15, fill="#64748b", width=2)
                    render(child)
                label = str(node.label())
                fill = "#dbeafe"
            else:
                label = str(node)
                fill = "#dcfce7"

            width = max(48, len(label) * 10 + 18)
            canvas.create_rectangle(x - width / 2, y - 16, x + width / 2, y + 16,
                                    fill=fill, outline="#334155", width=1)
            canvas.create_text(
                x,
                y,
                text=label,
                font=("Arial", 11),
                fill="#111827",
            )

        render(tree)
        bounds = canvas.bbox("all")
        if bounds:
            canvas.configure(scrollregion=(bounds[0] - 30, bounds[1] - 30,
                                           bounds[2] + 30, bounds[3] + 30))

    selector.bind("<<ComboboxSelected>>", draw_selected_tree)
    draw_selected_tree()
    root.mainloop()
