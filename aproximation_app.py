import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import warnings
warnings.filterwarnings("ignore", category=np.RankWarning)


points = []
plot_canvas = None
function_label = None
function_text = None

def add_point():
    x = float(x_entry.get())
    y = float(y_entry.get())

    points.append((x, y))

    point_label = tk.Label(points_frame, text=f"({x}, {y})", bg="light green", font=("Arial", 12, "bold"))
    point_label.pack()

    x_entry.delete(0, tk.END)
    y_entry.delete(0, tk.END)

def reset_points():
    global points, plot_canvas, function_label, function_text

    points = []
    for widget in points_frame.winfo_children():
        widget.destroy()

    if plot_canvas is not None:
        plot_canvas.get_tk_widget().destroy()
        plot_canvas = None

    if function_label is not None:
        function_label.destroy()
        function_label = None

    if function_text is not None:
        function_text.destroy()
        function_text = None

def plot_polynomial():
    x_values = np.array([point[0] for point in points])
    y_values = np.array([point[1] for point in points])

    degree = int(degree_entry.get())

    coeffs = np.polyfit(x_values, y_values, degree)
    p = np.poly1d(coeffs)

    x = np.linspace(min(x_values) - 1, max(x_values) + 1, 100)
    y = p(x)

    fig = plt.figure(figsize=(5, 5))
    plt.scatter(x_values, y_values, label='Training data')
    plt.plot(x, y, 'r', label='Approximation')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)

    # Rounding the coefficients to 3 decimal places
    rounded_coeffs = np.round(coeffs, 3)
    function_string = ' + '.join([f"{coeff} * x**{deg}" for deg, coeff in enumerate(rounded_coeffs[::-1])])

    global plot_canvas, function_label, function_text
    if plot_canvas is not None:
        plot_canvas.get_tk_widget().destroy()

    plot_canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    plot_canvas.draw()
    plot_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    if function_label is None:
        function_label = tk.Label(inputs_frame, text="Polynomial Function:", bg="light green", font=("Arial", 12, "bold"))
        function_label.pack()

    if function_text is not None:
        function_text.destroy()

    function_text = tk.Text(inputs_frame, height=40, width=50)
    function_text.insert(tk.END, function_string)
    function_text.configure(state='disabled', bg="light green")
    function_text.pack()



def close_window(event):
    window.destroy()
    window.quit()  # Exit the main loop

# Create the GUI window
window = tk.Tk()
window.title("Polynomial Approximation")
window.geometry("1000x500")
window.configure(bg="light green")

# Load the image
image_path = "placeholder_image.gif"
image = Image.open(image_path)
image = image.resize((700, 700), Image.Resampling.LANCZOS)
image = ImageTk.PhotoImage(image)

# Create input entry fields
inputs_frame = tk.Frame(window, bg="light green")
inputs_frame.pack(side=tk.RIGHT, padx=10)

x_label = tk.Label(inputs_frame, text="x:", bg="light green", font=("Arial", 12, "bold"))
x_label.pack()
x_entry = tk.Entry(inputs_frame, bg="light blue", justify="center", font=("Arial", 12))
x_entry.pack()

y_label = tk.Label(inputs_frame, text="y:", bg="light green", font=("Arial", 12, "bold"))
y_label.pack()
y_entry = tk.Entry(inputs_frame, bg="light blue", justify="center", font=("Arial", 12))
y_entry.pack()

add_button = tk.Button(inputs_frame, text="Add Point", command=add_point, width=12, height=2, bg="orange", fg="white", font=("Arial", 12, "bold"))
add_button.pack()

degree_label = tk.Label(inputs_frame, text="Degree:", bg="light green", font=("Arial", 12, "bold"))
degree_label.pack()
degree_entry = tk.Entry(inputs_frame, bg="light blue", justify="center", font=("Arial", 12))
degree_entry.pack()

# Create frame for displaying points
points_frame = tk.Frame(window, bg="light green")
points_frame.pack(side=tk.RIGHT, padx=10)

window.bind('<Shift-Return>', close_window)

# Create plot frame
plot_frame = tk.Frame(window, width=400, height=400)
plot_frame.pack(side=tk.LEFT, padx=10)

# Create label widget to display the image as the background
image_label = tk.Label(plot_frame, image=image)
image_label.place(x=0, y=0, relwidth=1, relheight=1)

plot_button = tk.Button(inputs_frame, text="Solve", command=plot_polynomial, width=12, height=2, bg="green", fg="white", font=("Arial", 12, "bold"))
plot_button.pack()

reset_button = tk.Button(inputs_frame, text="Reset", command=reset_points, width=12, height=2, bg="red", fg="white", font=("Arial", 12, "bold"))
reset_button.pack()

window.mainloop()


