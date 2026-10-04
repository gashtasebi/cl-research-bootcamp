from pathlib import Path
import re
import tkinter as tk


ALPHABET = {"a", "b"}

TRANSITIONS = {
    "q0": {"a": "q1", "b": "q0"},
    "q1": {"a": "q1", "b": "q2"},
    "q2": {"a": "q1", "b": "q0"},
}

START_STATE = "q0"
ACCEPTING_STATES = {"q2"}

# Any sequence of a/b symbols that ends in "ab".
REGEX_PATTERN = re.compile(r"[ab]*ab")


def run_dfa(text):
    """Return acceptance, visited states, and an optional invalid-symbol error."""
    state = START_STATE
    state_trace = [state]

    for symbol in text:
        if symbol not in ALPHABET:
            return False, state_trace, f"Invalid symbol: {symbol}"

        state = TRANSITIONS[state][symbol]
        state_trace.append(state)

    return state in ACCEPTING_STATES, state_trace, None


def show_automaton():
    """Draw the DFA transition diagram in a Tkinter window."""
    root = tk.Tk()
    root.title("DFA: Strings Ending in 'ab'")
    root.geometry("850x470")
    root.configure(background="#f8fafc")

    canvas = tk.Canvas(
        root,
        width=830,
        height=430,
        background="#f8fafc",
        highlightthickness=0,
    )
    canvas.pack(padx=10, pady=10)

    canvas.create_text(
        415,
        28,
        text="DFA for strings over {a, b} that end in 'ab'",
        font=("Arial", 16, "bold"),
        fill="#111827",
    )

    # State centers
    q0 = (150, 200)
    q1 = (415, 200)
    q2 = (680, 200)
    radius = 38

    # Start arrow into q0
    canvas.create_line(
        45, 200, q0[0] - radius, q0[1],
        arrow=tk.LAST,
        width=2,
        fill="#334155",
    )
    canvas.create_text(45, 178, text="start", font=("Arial", 10), fill="#334155")

    # q0 --a--> q1
    canvas.create_line(
        q0[0] + radius, 185, q1[0] - radius, 185,
        arrow=tk.LAST,
        width=2,
        fill="#2563eb",
    )
    canvas.create_text(282, 165, text="a", font=("Arial", 12, "bold"), fill="#1d4ed8")

    # q1 --b--> q2
    canvas.create_line(
        q1[0] + radius, 185, q2[0] - radius, 185,
        arrow=tk.LAST,
        width=2,
        fill="#2563eb",
    )
    canvas.create_text(547, 165, text="b", font=("Arial", 12, "bold"), fill="#1d4ed8")

    # q1 --a--> q0
    canvas.create_line(
        q1[0] - radius, 215, q0[0] + radius, 215,
        arrow=tk.LAST,
        width=2,
        fill="#64748b",
    )
    canvas.create_text(282, 235, text="b", font=("Arial", 12, "bold"), fill="#334155")

    # q2 --a--> q1
    canvas.create_line(
        q2[0] - radius, 215, q1[0] + radius, 215,
        arrow=tk.LAST,
        width=2,
        fill="#64748b",
    )
    canvas.create_text(547, 235, text="a", font=("Arial", 12, "bold"), fill="#334155")

    # q0 --b--> q0 loop
    canvas.create_arc(
        q0[0] - 28, q0[1] - 95, q0[0] + 28, q0[1] - 38,
        start=0, extent=300, style=tk.ARC,
        outline="#64748b", width=2,
    )
    canvas.create_text(q0[0], q0[1] - 91, text="b", font=("Arial", 12, "bold"), fill="#334155")

    # q1 --a--> q1 loop
    canvas.create_arc(
        q1[0] - 28, q1[1] - 95, q1[0] + 28, q1[1] - 38,
        start=0, extent=300, style=tk.ARC,
        outline="#64748b", width=2,
    )
    canvas.create_text(q1[0], q1[1] - 91, text="a", font=("Arial", 12, "bold"), fill="#334155")

    # q2 --b--> q0, routed below q1
    canvas.create_line(
        q2[0], q2[1] + radius,
        680, 340, 150, 340,
        q0[0], q0[1] + radius,
        smooth=True,
        arrow=tk.LAST,
        width=2,
        fill="#64748b",
        splinesteps=24,
    )
    canvas.create_text(415, 350, text="b", font=("Arial", 12, "bold"), fill="#334155")

    # Draw states after the arrows so state circles cover line endpoints.
    for state, (x, y) in (("q0", q0), ("q1", q1), ("q2", q2)):
        canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill="#dbeafe" if state != "q2" else "#dcfce7",
            outline="#1e3a8a",
            width=2,
        )
        canvas.create_text(
            x, y,
            text=state,
            font=("Arial", 13, "bold"),
            fill="#111827",
        )

    # Double circle marks the accepting state.
    canvas.create_oval(
        q2[0] - radius + 6, q2[1] - radius + 6,
        q2[0] + radius - 6, q2[1] + radius - 6,
        outline="#1e3a8a",
        width=2,
    )

    canvas.create_text(
        415,
        405,
        text="Accepting state: q2",
        font=("Arial", 11),
        fill="#166534",
    )

    root.mainloop()


data_path = Path("data/automata_test.txt")
test_strings = data_path.read_text(encoding="utf-8").splitlines()

accepted_count = 0
agreement_count = 0
disagreements = []

print("=== FINITE AUTOMATON AND REGEX COMPARISON ===")
print("Language: strings over {a, b} that end in 'ab'")
print()

for text in test_strings:
    dfa_accepted, state_trace, error = run_dfa(text)
    regex_accepted = REGEX_PATTERN.fullmatch(text) is not None
    display_text = text if text else "<empty string>"

    print("Input:", display_text)
    print("State trace:", " -> ".join(state_trace))
    print("DFA:", "ACCEPTED" if dfa_accepted else "REJECTED")
    print("Regex:", "ACCEPTED" if regex_accepted else "REJECTED")

    if error:
        print(error)

    if dfa_accepted:
        accepted_count += 1

    if dfa_accepted == regex_accepted:
        agreement_count += 1
        print("Agreement: YES")
    else:
        disagreements.append(display_text)
        print("Agreement: NO")

    print("-" * 50)

print()
print("=== SUMMARY ===")
print("Test strings:", len(test_strings))
print("Accepted by the DFA:", accepted_count)
print("DFA/regex agreements:", agreement_count)
print("DFA/regex disagreements:", len(disagreements))

if disagreements:
    print("Disagreement cases:", ", ".join(disagreements))

print()
print("Opening the DFA diagram...")
show_automaton()
