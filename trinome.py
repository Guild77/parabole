try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ModuleNotFoundError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import ttk
import numpy as np
from tkinter import messagebox

def format_number(num):
    return f"{num:.2f}".rstrip('0').rstrip('.') if num % 1 != 0 else f"{int(num)}"

def render_latex_formula(formula, label):
    fig, ax = plt.subplots(figsize=(4, 0.5))  # Reduce height
    ax.text(0.5, 0.5, f"${formula}$", fontsize=12, ha='center', va='center')
    ax.axis('off')
    fig.tight_layout(pad=0)
    canvas = FigureCanvasTkAgg(fig, master=label)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    plt.close(fig)

def plot_trinome(a, b, c):
    x = np.linspace(-10, 10, 400)
    y = a * x**2 + b * x + c

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f'{a}x^2 + {b}x + {c}')
    
    # Calculate roots
    delta = b**2 - 4*a*c
    if delta >= 0:
        x1 = (-b - np.sqrt(delta)) / (2*a)
        x2 = (-b + np.sqrt(delta)) / (2*a)
        plt.scatter([x1, x2], [0, 0], color='red')  # Plot roots
        plt.text(x1, 0, f'x1={format_number(x1)}', fontsize=12, verticalalignment='bottom')
        plt.text(x2, 0, f'x2={format_number(x2)}', fontsize=12, verticalalignment='bottom')
    else:
        x1 = x2 = None
    
    # Calculate vertex
    alpha = -b / (2*a)
    beta = -delta / (4*a)
    plt.scatter([alpha], [beta], color='blue')  # Plot vertex
    plt.text(alpha, beta, f'({format_number(alpha)}, {format_number(beta)})', fontsize=12, verticalalignment='bottom')
    
    # Plot point 'c' (when x=0)
    plt.scatter([0], [c], color='green')
    plt.text(0, c, f'c={format_number(c)}', fontsize=12, verticalalignment='bottom')
    
    # Plot tangent at 'c' with slope 'b'
    tangent_x = np.linspace(-10, 10, 400)
    tangent_y = b * tangent_x + c
    plt.plot(tangent_x, tangent_y, linestyle='--', color='purple', label=f'Tangent: y={b}x + {c}')
    
    # Calculate focus and directrix
    focus_x = alpha
    focus_y = beta + 1 / (4 * a)
    directrix_y = beta - 1 / (4 * a)
    
    plt.scatter([focus_x], [focus_y], color='orange', label='Focus')
    plt.axhline(directrix_y, color='orange', linestyle='--', label='Directrix')
    
    # Calculate plot limits
    if x1 is not None and x2 is not None:
        x_min = min(x1, x2, alpha) - abs(x2 - x1) * 2
        x_max = max(x1, x2, alpha) + abs(x2 - x1) * 2
        y_min = min(0, beta, c, directrix_y) - abs(beta) * 2
        y_max = max(0, beta, c, focus_y) + abs(beta) * 2
    else:
        x_min, x_max = -10, 10
        y_min, y_max = min(y), max(y)
    
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.show()

def on_plot_button_click():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
        
        # Clear previous formulas
        for widget in label_delta.winfo_children():
            widget.destroy()
        for widget in label_roots.winfo_children():
            widget.destroy()
        for widget in label_vertex.winfo_children():
            widget.destroy()
        for widget in label_canonique.winfo_children():
            widget.destroy()
        for widget in label_expanded.winfo_children():
            widget.destroy()
        for widget in label_factored.winfo_children():
            widget.destroy()
        for widget in label_focus.winfo_children():
            widget.destroy()
        for widget in label_directrix.winfo_children():
            widget.destroy()
        
        # Calculate delta
        delta = b**2 - 4*a*c
        render_latex_formula(f"\\Delta = b^2 - 4ac = {format_number(delta)}", label_delta)
        
        # Calculate roots and display below input boxes
        if delta >= 0:
            x1 = (-b - np.sqrt(delta)) / (2*a)
            x2 = (-b + np.sqrt(delta)) / (2*a)
            render_latex_formula(f"x_1 = \\frac{{-b - \\sqrt{{\\Delta}}}}{{2a}} = {format_number(x1)},\\ x_2 = \\frac{{-b + \\sqrt{{\\Delta}}}}{{2a}} = {format_number(x2)}", label_roots)
        else:
            render_latex_formula("x_1 = \\text{No real root},\\ x_2 = \\text{No real root}", label_roots)
        
        # Calculate vertex and display below input boxes
        alpha = -b / (2*a)
        beta = -delta / (4*a)
        render_latex_formula(f"\\text{{Sommet}} = \\left(\\frac{{-b}}{{2a}}, \\frac{{-\\Delta}}{{4a}}\\right) = ({format_number(alpha)}, {format_number(beta)})", label_vertex)
        
        # Display canonique form
        render_latex_formula(f"\\text{{Canonique}}:\\ y = a(x - {format_number(alpha)})^2 + {format_number(beta)}", label_canonique)
        
        # Display expanded form
        render_latex_formula(f"\\text{{Développée}}:\\ y = {format_number(a)}x^2 + {format_number(b)}x + {format_number(c)}", label_expanded)
        
        # Display factored form
        if delta >= 0:
            render_latex_formula(f"\\text{{Factorisée}}:\\ y = a(x - {format_number(x1)})(x - {format_number(x2)})", label_factored)
        else:
            render_latex_formula(f"\\text{{Factorisée}}: \\text{{No real roots}}", label_factored)
        
        # Display focus and directrix formulas
        render_latex_formula(f"\\text{{Focale}}: \\left(\\alpha, \\beta + \\frac{{1}}{{4a}}\\right) = ({format_number(alpha)}, {format_number(beta + 1 / (4 * a))})", label_focus)
        render_latex_formula(f"\\text{{Directrice}}: y = \\beta - \\frac{{1}}{{4a}} = {format_number(beta - 1 / (4 * a))}", label_directrix)
        
        # Display input values
        label_inputs.config(text=f"a = {format_number(a)}, b = {format_number(b)}, c = {format_number(c)}")
        
        plot_trinome(a, b, c)
    except ValueError:
        tk.messagebox.showerror("Invalid input", "Please enter valid numbers for a, b, and c.")

# Create the main window
root = tk.Tk()
root.title("Trinome du Second Degré")

# Create and place the input fields and labels
frame_inputs = ttk.Frame(root)
frame_inputs.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

entry_a = ttk.Entry(frame_inputs, width=5)
entry_a.grid(row=0, column=0, padx=5)

ttk.Label(frame_inputs, text="x² +").grid(row=0, column=1, padx=5)
entry_b = ttk.Entry(frame_inputs, width=5)
entry_b.grid(row=0, column=2, padx=5)

ttk.Label(frame_inputs, text="x +").grid(row=0, column=3, padx=5)
entry_c = ttk.Entry(frame_inputs, width=5)
entry_c.grid(row=0, column=4, padx=5)

# Add label to display input values
label_inputs = tk.Label(root)
label_inputs.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Add label to display delta
label_delta = tk.Label(root)
label_delta.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Add label to display the roots
label_roots = tk.Label(root)
label_roots.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Add label to display the vertex
label_vertex = tk.Label(root)
label_vertex.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Add label to display the quadratic form
label_canonique = tk.Label(root)
label_canonique.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Add label to display the expanded form
label_expanded = tk.Label(root)
label_expanded.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Add label to display the factored form
label_factored = tk.Label(root)
label_factored.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Add label to display the focus
label_focus = tk.Label(root)
label_focus.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Add label to display the directrix
label_directrix = tk.Label(root)
label_directrix.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Create and place the plot button
plot_button = ttk.Button(root, text="Plot", command=on_plot_button_click)
plot_button.grid(row=10, column=0, columnspan=2, pady=20)

# Run the application
root.mainloop()
