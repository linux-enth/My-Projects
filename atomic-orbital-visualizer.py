import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

from scipy.special import sph_harm_y, genlaguerre, factorial


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def radial_wavefunction(n, l, r):

    rho = 2 * r / n

    norm = np.sqrt(
        (2 / n) ** 3 *
        factorial(n - l - 1) /
        (2 * n * factorial(n + l))
    )

    laguerre = genlaguerre(
        n - l - 1,
        2 * l + 1
    )(rho)

    return norm * np.exp(-rho / 2) * rho**l * laguerre


def hydrogen_wavefunction(n, l, m, r, theta, phi):

    R = radial_wavefunction(n, l, r)

    Y = sph_harm_y(l, m, theta, phi)

    return R * Y


class OrbitalApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Hydrogen Orbital Visualizer")
        self.geometry("1200x800")

        self.control_frame = ctk.CTkFrame(
            self,
            width=250
        )
        self.control_frame.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )

        title = ctk.CTkLabel(
            self.control_frame,
            text="Atomic Orbital Visualizer",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=20)

        ctk.CTkLabel(
            self.control_frame,
            text="Principal Quantum Number (n)"
        ).pack(pady=(20, 5))

        self.n_slider = ctk.CTkSlider(
            self.control_frame,
            from_=1,
            to=5,
            number_of_steps=4
        )

        self.n_slider.set(1)
        self.n_slider.pack(padx=20)

        ctk.CTkLabel(
            self.control_frame,
            text="Azimuthal Quantum Number (l)"
        ).pack(pady=(20, 5))

        self.l_slider = ctk.CTkSlider(
            self.control_frame,
            from_=0,
            to=4,
            number_of_steps=4
        )

        self.l_slider.set(0)
        self.l_slider.pack(padx=20)

        ctk.CTkLabel(
            self.control_frame,
            text="Magnetic Quantum Number (m)"
        ).pack(pady=(20, 5))

        self.m_slider = ctk.CTkSlider(
            self.control_frame,
            from_=-4,
            to=4,
            number_of_steps=8
        )

        self.m_slider.set(0)
        self.m_slider.pack(padx=20)

        self.render_button = ctk.CTkButton(
            self.control_frame,
            text="Render Orbital",
            command=self.plot_orbital
        )

        self.render_button.pack(pady=40)

        self.status_label = ctk.CTkLabel(
            self.control_frame,
            text=""
        )

        self.status_label.pack()

        self.fig = plt.figure(figsize=(8, 8))

        self.ax = self.fig.add_subplot(
            111,
            projection='3d'
        )

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=self
        )

        self.canvas_widget = self.canvas.get_tk_widget()

        self.canvas_widget.pack(
            side="right",
            fill="both",
            expand=True
        )


        self.toolbar = NavigationToolbar2Tk(
            self.canvas,
            self
        )

        self.toolbar.update()


        self.canvas.mpl_connect(
            "scroll_event",
            self.on_scroll
        )

        self.plot_orbital()


    def on_scroll(self, event):

        scale_factor = 0.9 if event.button == 'up' else 1.1

        xlim = self.ax.get_xlim3d()
        ylim = self.ax.get_ylim3d()
        zlim = self.ax.get_zlim3d()

        x_center = np.mean(xlim)
        y_center = np.mean(ylim)
        z_center = np.mean(zlim)

        x_range = (xlim[1] - xlim[0]) * scale_factor
        y_range = (ylim[1] - ylim[0]) * scale_factor
        z_range = (zlim[1] - zlim[0]) * scale_factor

        self.ax.set_xlim3d([
            x_center - x_range / 2,
            x_center + x_range / 2
        ])

        self.ax.set_ylim3d([
            y_center - y_range / 2,
            y_center + y_range / 2
        ])

        self.ax.set_zlim3d([
            z_center - z_range / 2,
            z_center + z_range / 2
        ])

        self.canvas.draw_idle()


    def plot_orbital(self):

        n = int(round(self.n_slider.get()))
        l = int(round(self.l_slider.get()))
        m = int(round(self.m_slider.get()))

        if l >= n:

            self.status_label.configure(
                text="Invalid: l must be < n",
                text_color="red"
            )

            return

        if abs(m) > l:

            self.status_label.configure(
                text="Invalid: |m| ≤ l",
                text_color="red"
            )

            return

        self.status_label.configure(
            text=f"Rendering n={n}, l={l}, m={m}",
            text_color="lightgreen"
        )

        self.ax.clear()

        N = 120000

        limit = 12

        x = np.random.uniform(-limit, limit, N)
        y = np.random.uniform(-limit, limit, N)
        z = np.random.uniform(-limit, limit, N)

        r = np.sqrt(x**2 + y**2 + z**2)

        theta = np.arccos(
            np.clip(
                z / (r + 1e-12),
                -1,
                1
            )
        )

        phi = np.arctan2(y, x)

        phi = np.mod(phi, 2 * np.pi)

        psi = hydrogen_wavefunction(
            n,
            l,
            m,
            r,
            theta,
            phi
        )

        probability = np.abs(psi)**2

        probability /= probability.max()

        mask = probability > 0.05

        x_plot = x[mask]
        y_plot = y[mask]
        z_plot = z[mask]

        colors = probability[mask]

        self.ax.scatter(
            x_plot,
            y_plot,
            z_plot,
            c=colors,
            cmap='plasma',
            s=1,
            alpha=0.6
        )

        self.ax.set_title(
            f"Hydrogen Orbital (n={n}, l={l}, m={m})",
            color="white"
        )

        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_zlim(-10, 10)

        self.ax.set_facecolor("black")

        self.fig.patch.set_facecolor("#222222")

        self.ax.tick_params(colors='white')

        self.canvas.draw()


app = OrbitalApp()
app.mainloop()

