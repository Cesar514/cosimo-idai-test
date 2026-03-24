from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Sequence

MazeSize = tuple[int, int]
BACKEND_CHOICES = ("auto", "pybullet", "mujoco")
GUI_SETUP_MODE_ENV = "ROBOTICS_MAZE_GUI_SETUP_MODE"


@dataclass(frozen=True)
class GuiSetupConfig:
    planner: str
    episodes: int
    maze_size: MazeSize
    seed: int | None
    gui: bool
    physics_backend: str = "auto"
    robot_urdf: str | None = None
    gui_hold_seconds: float = 8.0


@dataclass(frozen=True)
class GuiSetupResult:
    config: GuiSetupConfig | None
    warning: str | None = None
    cancelled: bool = False


def _parse_positive_int(raw_value: str, field_name: str) -> int:
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an integer.") from exc
    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")
    return value


def _parse_nonnegative_float(raw_value: str, field_name: str) -> float:
    try:
        value = float(raw_value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a number.") from exc
    if value < 0:
        raise ValueError(f"{field_name} must be greater than or equal to zero.")
    return value


def _planner_choices(initial: str, planner_options: Sequence[str] | None) -> tuple[str, ...]:
    choices: list[str] = []
    if planner_options is not None:
        for option in planner_options:
            normalized = option.strip()
            if normalized and normalized not in choices:
                choices.append(normalized)
    if initial.strip() and initial not in choices:
        choices.insert(0, initial)
    return tuple(choices)


def launch_gui_setup(
    initial: GuiSetupConfig,
    *,
    planner_options: Sequence[str] | None = None,
) -> GuiSetupResult:
    setup_mode = os.environ.get(GUI_SETUP_MODE_ENV, "dialog").strip().lower()
    if setup_mode == "accept":
        return GuiSetupResult(config=initial, cancelled=False)
    if setup_mode == "cancel":
        return GuiSetupResult(config=None, cancelled=True)
    if setup_mode == "skip":
        return GuiSetupResult(
            config=None,
            warning=f"GUI setup skipped by {GUI_SETUP_MODE_ENV}=skip.",
        )
    if setup_mode not in {"", "dialog"}:
        return GuiSetupResult(
            config=None,
            warning=(
                f"Unknown {GUI_SETUP_MODE_ENV}={setup_mode!r}; expected one of "
                "'dialog', 'accept', 'cancel', or 'skip'."
            ),
        )

    try:
        import tkinter as tk
        from tkinter import messagebox, ttk
    except Exception as exc:
        return GuiSetupResult(config=None, warning=f"tkinter is unavailable: {exc}")

    try:
        root = tk.Tk()
    except Exception as exc:
        return GuiSetupResult(config=None, warning=f"display is unavailable: {exc}")

    root.title("Robotics Maze Setup")
    root.resizable(False, False)

    planner_var = tk.StringVar(value=initial.planner)
    episodes_var = tk.StringVar(value=str(initial.episodes))
    width_var = tk.StringVar(value=str(initial.maze_size[0]))
    height_var = tk.StringVar(value=str(initial.maze_size[1]))
    seed_var = tk.StringVar(value="" if initial.seed is None else str(initial.seed))
    gui_var = tk.BooleanVar(value=initial.gui)
    backend_var = tk.StringVar(value=initial.physics_backend)
    robot_urdf_var = tk.StringVar(value=initial.robot_urdf or "")
    hold_seconds_var = tk.StringVar(value=f"{initial.gui_hold_seconds:g}")
    choices = _planner_choices(initial.planner, planner_options)

    selected: GuiSetupConfig | None = None
    cancelled = True
    return_binding_armed = False

    def on_launch() -> None:
        nonlocal selected, cancelled
        planner_name = planner_var.get().strip()
        if not planner_name:
            messagebox.showerror(
                title="Invalid planner",
                message="Planner cannot be empty.",
                parent=root,
            )
            return

        try:
            episodes = _parse_positive_int(episodes_var.get().strip(), "Episodes")
            width = _parse_positive_int(width_var.get().strip(), "Maze width")
            height = _parse_positive_int(height_var.get().strip(), "Maze height")
            seed_text = seed_var.get().strip()
            seed = None if not seed_text else int(seed_text)
            backend = backend_var.get().strip().lower()
            if backend not in BACKEND_CHOICES:
                raise ValueError("Physics backend must be one of: auto, pybullet, mujoco.")
            hold_seconds = _parse_nonnegative_float(
                hold_seconds_var.get().strip(),
                "GUI hold seconds",
            )
            robot_urdf_text = robot_urdf_var.get().strip()
        except ValueError as exc:
            messagebox.showerror(
                title="Invalid input",
                message=str(exc),
                parent=root,
            )
            return

        selected = GuiSetupConfig(
            planner=planner_name,
            episodes=episodes,
            maze_size=(width, height),
            seed=seed,
            gui=gui_var.get(),
            physics_backend=backend,
            robot_urdf=robot_urdf_text or None,
            gui_hold_seconds=hold_seconds,
        )
        cancelled = False
        root.destroy()

    def on_cancel() -> None:
        root.destroy()

    def on_return(_event: object) -> None:
        if return_binding_armed:
            on_launch()

    def _arm_return_binding() -> None:
        nonlocal return_binding_armed
        return_binding_armed = True

    def _present_window() -> None:
        root.update_idletasks()
        width = root.winfo_reqwidth()
        height = root.winfo_reqheight()
        x = max((root.winfo_screenwidth() - width) // 2, 0)
        y = max((root.winfo_screenheight() - height) // 3, 0)
        root.geometry(f"+{x}+{y}")
        try:
            root.lift()
            root.attributes("-topmost", True)
            root.after(250, lambda: root.attributes("-topmost", False))
        except Exception:
            pass
        try:
            root.focus_force()
        except Exception:
            pass

    frame = ttk.Frame(root, padding=12)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(1, weight=1)

    ttk.Label(frame, text="Planner").grid(row=0, column=0, sticky="w", padx=6, pady=4)
    planner_combo = ttk.Combobox(
        frame,
        textvariable=planner_var,
        values=choices,
        state="normal",
        width=28,
    )
    planner_combo.grid(row=0, column=1, sticky="ew", padx=6, pady=4)

    ttk.Label(frame, text="Episodes").grid(row=1, column=0, sticky="w", padx=6, pady=4)
    ttk.Spinbox(
        frame,
        from_=1,
        to=1000000,
        textvariable=episodes_var,
        width=12,
    ).grid(row=1, column=1, sticky="w", padx=6, pady=4)

    ttk.Label(frame, text="Maze size").grid(row=2, column=0, sticky="w", padx=6, pady=4)
    size_frame = ttk.Frame(frame)
    size_frame.grid(row=2, column=1, sticky="w", padx=6, pady=4)
    ttk.Entry(size_frame, textvariable=width_var, width=8).grid(row=0, column=0, sticky="w")
    ttk.Label(size_frame, text="x").grid(row=0, column=1, sticky="w", padx=4)
    ttk.Entry(size_frame, textvariable=height_var, width=8).grid(row=0, column=2, sticky="w")

    ttk.Label(frame, text="Seed").grid(row=3, column=0, sticky="w", padx=6, pady=4)
    ttk.Entry(frame, textvariable=seed_var, width=18).grid(row=3, column=1, sticky="w", padx=6, pady=4)

    ttk.Checkbutton(
        frame,
        text="Enable simulator GUI mode",
        variable=gui_var,
    ).grid(row=4, column=0, columnspan=2, sticky="w", padx=6, pady=6)

    ttk.Label(frame, text="Physics backend").grid(row=5, column=0, sticky="w", padx=6, pady=4)
    ttk.Combobox(
        frame,
        textvariable=backend_var,
        values=BACKEND_CHOICES,
        state="readonly",
        width=16,
    ).grid(row=5, column=1, sticky="w", padx=6, pady=4)

    ttk.Label(frame, text="Robot URDF (optional)").grid(row=6, column=0, sticky="w", padx=6, pady=4)
    ttk.Entry(frame, textvariable=robot_urdf_var, width=28).grid(
        row=6,
        column=1,
        sticky="ew",
        padx=6,
        pady=4,
    )

    ttk.Label(frame, text="GUI hold (seconds)").grid(row=7, column=0, sticky="w", padx=6, pady=4)
    ttk.Entry(frame, textvariable=hold_seconds_var, width=12).grid(
        row=7,
        column=1,
        sticky="w",
        padx=6,
        pady=4,
    )

    button_frame = ttk.Frame(frame)
    button_frame.grid(row=8, column=0, columnspan=2, sticky="e", padx=6, pady=(10, 4))
    ttk.Button(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=0, padx=(0, 8))
    ttk.Button(button_frame, text="Launch", command=on_launch).grid(row=0, column=1)

    root.protocol("WM_DELETE_WINDOW", on_cancel)
    root.bind("<Escape>", lambda _event: on_cancel())
    root.bind("<Return>", on_return)

    planner_combo.focus_set()
    root.after_idle(_present_window)
    root.after(300, _arm_return_binding)
    root.mainloop()
    return GuiSetupResult(config=selected, cancelled=cancelled)
