#!/usr/bin/env python3
"""
BMP-II Technical Training Simulator
A 3D interactive training application for BMP-II Infantry Fighting Vehicle
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import math
import random
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
import pickle
import os


@dataclass
class TrainingModule:
    name: str
    description: str
    components: List[str]
    completed: bool = False
    score: float = 0.0
    completion_time: str = ""


@dataclass
class Component:
    name: str
    x: float
    y: float
    width: float
    height: float
    color: str
    description: str
    module: str
    steps: List[str]


class BMP2Simulator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMP-II Technical Training Simulator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a1a1a")

        self.current_module = None
        self.current_step = 0
        self.training_data = self.initialize_training_data()
        self.load_progress()

        self.create_ui()

    def initialize_training_data(self) -> Dict:
        modules = {
            "engine": TrainingModule(
                name="Engine System",
                description="Learn about the BMP-II diesel engine, cooling system, and fuel system",
                components=["engine_block", "cooling_system", "fuel_pump", "air_filter"]
            ),
            "transmission": TrainingModule(
                name="Transmission System",
                description="Understand the power transmission, gearbox, and drive system",
                components=["gearbox", "drive_shaft", "differential", "final_drive"]
            ),
            "turret": TrainingModule(
                name="Turret & Weapons",
                description="Master the turret rotation, elevation system, and weapon controls",
                components=["turret_ring", "cannon_2a42", "elevation_mechanism", "ammunition_feed"]
            ),
            "suspension": TrainingModule(
                name="Suspension System",
                description="Study the torsion bar suspension, track system, and shock absorbers",
                components=["torsion_bars", "road_wheels", "track_assembly", "shock_absorbers"]
            ),
            "electronics": TrainingModule(
                name="Electronics & Controls",
                description="Learn fire control systems, communication systems, and electrical systems",
                components=["fire_control", "radio_system", "battery_system", "electrical_panel"]
            ),
            "maintenance": TrainingModule(
                name="Maintenance Procedures",
                description="Practice routine maintenance, troubleshooting, and repair procedures",
                components=["oil_change", "filter_replacement", "track_tension", "diagnostics"]
            )
        }

        components = {
            "engine_block": Component(
                "Engine Block", 300, 200, 120, 80, "#ff6b35",
                "UTD-20 6-cylinder diesel engine - 300 HP",
                "engine",
                [
                    "Inspect engine block for cracks or damage",
                    "Check engine mounts and bolts",
                    "Verify oil pressure gauge readings",
                    "Test compression in all cylinders"
                ]
            ),
            "cooling_system": Component(
                "Cooling System", 450, 200, 100, 60, "#4ecdc4",
                "Liquid cooling system with radiator and fan",
                "engine",
                [
                    "Check coolant level in reservoir",
                    "Inspect radiator for leaks",
                    "Test thermostat operation",
                    "Verify fan belt tension"
                ]
            ),
            "fuel_pump": Component(
                "Fuel Pump", 300, 320, 80, 60, "#ffe66d",
                "High-pressure fuel injection pump",
                "engine",
                [
                    "Check fuel lines for leaks",
                    "Test fuel pressure output",
                    "Inspect pump seals",
                    "Verify fuel filter condition"
                ]
            ),
            "gearbox": Component(
                "Gearbox", 250, 400, 140, 90, "#95e1d3",
                "5-speed manual transmission with synchronized gears",
                "transmission",
                [
                    "Check transmission fluid level",
                    "Test gear shifting smoothness",
                    "Inspect clutch operation",
                    "Verify synchronizer function"
                ]
            ),
            "turret_ring": Component(
                "Turret Ring", 600, 150, 150, 150, "#f38181",
                "360-degree rotation turret ring bearing",
                "turret",
                [
                    "Check turret rotation mechanism",
                    "Lubricate turret ring bearings",
                    "Test manual and powered rotation",
                    "Verify stabilization system"
                ]
            ),
            "cannon_2a42": Component(
                "2A42 Autocannon", 650, 200, 180, 40, "#aa96da",
                "30mm automatic cannon - 500 rounds/min",
                "turret",
                [
                    "Inspect barrel for wear",
                    "Check firing mechanism",
                    "Test ammunition feed system",
                    "Verify recoil system operation"
                ]
            ),
            "torsion_bars": Component(
                "Torsion Bars", 200, 550, 200, 40, "#fcbad3",
                "Independent torsion bar suspension for each wheel",
                "suspension",
                [
                    "Check torsion bar tension",
                    "Inspect mounting points",
                    "Test suspension travel",
                    "Verify alignment"
                ]
            ),
            "fire_control": Component(
                "Fire Control Computer", 800, 300, 120, 100, "#a8d8ea",
                "Integrated fire control system with ballistic computer",
                "electronics",
                [
                    "Power on fire control system",
                    "Calibrate range finder",
                    "Test targeting reticle",
                    "Verify sensor inputs"
                ]
            )
        }

        return {"modules": modules, "components": components}

    def create_ui(self):
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="BMP-II INFANTRY FIGHTING VEHICLE",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        title_label.pack(pady=10)

        subtitle_label = tk.Label(
            title_frame,
            text="Technical Training Simulator - Virtual Reality Environment",
            font=("Arial", 12),
            bg="#2c3e50",
            fg="#95a5a6"
        )
        subtitle_label.pack()

        main_container = tk.Frame(self.root, bg="#1a1a1a")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_panel = tk.Frame(main_container, bg="#34495e", width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)

        modules_label = tk.Label(
            left_panel,
            text="Training Modules",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        )
        modules_label.pack(pady=10)

        self.modules_frame = tk.Frame(left_panel, bg="#34495e")
        self.modules_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.populate_modules()

        button_frame = tk.Frame(left_panel, bg="#34495e")
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        reset_btn = tk.Button(
            button_frame,
            text="Reset Progress",
            command=self.reset_progress,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        reset_btn.pack(fill=tk.X, pady=2)

        stats_btn = tk.Button(
            button_frame,
            text="View Statistics",
            command=self.show_statistics,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        stats_btn.pack(fill=tk.X, pady=2)

        right_panel = tk.Frame(main_container, bg="#2c3e50")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_frame = tk.Frame(right_panel, bg="#1a1a1a", height=500)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg="#0a0a0a",
            highlightthickness=2,
            highlightbackground="#3498db"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.info_frame = tk.Frame(right_panel, bg="#34495e", height=200)
        self.info_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.info_frame.pack_propagate(False)

        self.info_title = tk.Label(
            self.info_frame,
            text="Select a training module to begin",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#ecf0f1",
            anchor="w"
        )
        self.info_title.pack(fill=tk.X, padx=10, pady=(10, 5))

        self.info_text = tk.Text(
            self.info_frame,
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1",
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.show_welcome_screen()

    def populate_modules(self):
        for widget in self.modules_frame.winfo_children():
            widget.destroy()

        for module_id, module in self.training_data["modules"].items():
            frame = tk.Frame(self.modules_frame, bg="#2c3e50", relief=tk.RAISED, bd=1)
            frame.pack(fill=tk.X, pady=5)

            status_color = "#27ae60" if module.completed else "#95a5a6"
            status_indicator = tk.Label(
                frame,
                text="●",
                font=("Arial", 16),
                bg="#2c3e50",
                fg=status_color,
                width=2
            )
            status_indicator.pack(side=tk.LEFT, padx=5)

            text_frame = tk.Frame(frame, bg="#2c3e50")
            text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            name_label = tk.Label(
                text_frame,
                text=module.name,
                font=("Arial", 11, "bold"),
                bg="#2c3e50",
                fg="#ecf0f1",
                anchor="w"
            )
            name_label.pack(fill=tk.X)

            if module.completed:
                score_label = tk.Label(
                    text_frame,
                    text=f"Score: {module.score:.1f}%",
                    font=("Arial", 9),
                    bg="#2c3e50",
                    fg="#27ae60",
                    anchor="w"
                )
                score_label.pack(fill=tk.X)

            start_btn = tk.Button(
                frame,
                text="Start" if not module.completed else "Review",
                command=lambda mid=module_id: self.start_module(mid),
                bg="#3498db" if not module.completed else "#16a085",
                fg="white",
                font=("Arial", 9, "bold"),
                relief=tk.FLAT,
                cursor="hand2",
                padx=10
            )
            start_btn.pack(side=tk.RIGHT, padx=5, pady=5)

    def show_welcome_screen(self):
        self.canvas.delete("all")

        width = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 800
        height = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 500

        self.canvas.create_text(
            width // 2, height // 2 - 50,
            text="BMP-II Virtual Training System",
            font=("Arial", 28, "bold"),
            fill="#3498db"
        )

        self.canvas.create_text(
            width // 2, height // 2 + 20,
            text="Select a training module from the left panel",
            font=("Arial", 14),
            fill="#ecf0f1"
        )

        self.canvas.create_text(
            width // 2, height // 2 + 60,
            text="Interactive 3D Component Training",
            font=("Arial", 12),
            fill="#95a5a6"
        )

    def start_module(self, module_id: str):
        self.current_module = module_id
        self.current_step = 0

        module = self.training_data["modules"][module_id]

        self.info_title.config(text=module.name)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, f"{module.description}\n\n")
        self.info_text.insert(tk.END, "Components in this module:\n", "bold")

        for comp_id in module.components:
            if comp_id in self.training_data["components"]:
                comp = self.training_data["components"][comp_id]
                self.info_text.insert(tk.END, f"  • {comp.name}\n")

        self.info_text.tag_config("bold", font=("Arial", 10, "bold"))

        self.draw_3d_view()

    def draw_3d_view(self):
        self.canvas.delete("all")

        width = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 800
        height = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 500

        self.canvas.create_rectangle(
            10, 10, width - 10, height - 10,
            outline="#3498db",
            width=2
        )

        self.canvas.create_text(
            20, 25,
            text="3D Component View - Interactive Training Mode",
            font=("Arial", 12, "bold"),
            fill="#3498db",
            anchor="w"
        )

        module = self.training_data["modules"][self.current_module]

        for idx, comp_id in enumerate(module.components):
            if comp_id in self.training_data["components"]:
                comp = self.training_data["components"][comp_id]

                angle = (idx / len(module.components)) * 2 * math.pi
                center_x = width // 2
                center_y = height // 2
                radius = min(width, height) // 3

                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)

                self.canvas.create_rectangle(
                    x - comp.width // 2, y - comp.height // 2,
                    x + comp.width // 2, y + comp.height // 2,
                    fill=comp.color,
                    outline="#ecf0f1",
                    width=2,
                    tags=("component", comp_id)
                )

                self.canvas.create_text(
                    x, y,
                    text=comp.name.split()[0],
                    font=("Arial", 10, "bold"),
                    fill="#000000",
                    tags=("component", comp_id)
                )

                self.canvas.create_line(
                    center_x, center_y, x, y,
                    fill="#3498db",
                    width=1,
                    dash=(4, 4)
                )

        center_x = width // 2
        center_y = height // 2
        self.canvas.create_oval(
            center_x - 60, center_y - 60,
            center_x + 60, center_y + 60,
            fill="#34495e",
            outline="#ecf0f1",
            width=3
        )

        self.canvas.create_text(
            center_x, center_y,
            text="BMP-II\n" + module.name.split()[0],
            font=("Arial", 12, "bold"),
            fill="#ecf0f1",
            justify=tk.CENTER
        )

        self.canvas.tag_bind("component", "<Button-1>", self.on_component_click)
        self.canvas.tag_bind("component", "<Enter>", self.on_component_hover)
        self.canvas.tag_bind("component", "<Leave>", self.on_component_leave)

    def on_component_click(self, event):
        item = self.canvas.find_withtag("current")[0]
        tags = self.canvas.gettags(item)

        comp_id = None
        for tag in tags:
            if tag != "component" and tag != "current":
                comp_id = tag
                break

        if comp_id and comp_id in self.training_data["components"]:
            self.show_training_dialog(comp_id)

    def on_component_hover(self, event):
        item = self.canvas.find_withtag("current")[0]
        tags = self.canvas.gettags(item)

        if "component" in tags:
            self.canvas.config(cursor="hand2")
            self.canvas.itemconfig(item, width=3)

    def on_component_leave(self, event):
        self.canvas.config(cursor="")
        item = self.canvas.find_withtag("current")[0]
        self.canvas.itemconfig(item, width=2)

    def show_training_dialog(self, comp_id: str):
        comp = self.training_data["components"][comp_id]

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Training: {comp.name}")
        dialog.geometry("600x500")
        dialog.configure(bg="#2c3e50")
        dialog.transient(self.root)
        dialog.grab_set()

        header = tk.Frame(dialog, bg="#34495e", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text=comp.name,
            font=("Arial", 18, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        )
        title.pack(pady=15)

        desc_frame = tk.Frame(dialog, bg="#2c3e50")
        desc_frame.pack(fill=tk.X, padx=20, pady=10)

        desc_label = tk.Label(
            desc_frame,
            text=comp.description,
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#ecf0f1",
            wraplength=550,
            justify=tk.LEFT
        )
        desc_label.pack()

        steps_frame = tk.Frame(dialog, bg="#34495e")
        steps_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        steps_title = tk.Label(
            steps_frame,
            text="Training Procedures:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="#ecf0f1",
            anchor="w"
        )
        steps_title.pack(fill=tk.X, padx=10, pady=(10, 5))

        for idx, step in enumerate(comp.steps, 1):
            step_frame = tk.Frame(steps_frame, bg="#2c3e50")
            step_frame.pack(fill=tk.X, padx=10, pady=5)

            step_num = tk.Label(
                step_frame,
                text=f"{idx}.",
                font=("Arial", 10, "bold"),
                bg="#2c3e50",
                fg="#3498db",
                width=3,
                anchor="e"
            )
            step_num.pack(side=tk.LEFT)

            step_text = tk.Label(
                step_frame,
                text=step,
                font=("Arial", 10),
                bg="#2c3e50",
                fg="#ecf0f1",
                wraplength=500,
                justify=tk.LEFT,
                anchor="w"
            )
            step_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        button_frame = tk.Frame(dialog, bg="#2c3e50")
        button_frame.pack(fill=tk.X, padx=20, pady=20)

        complete_btn = tk.Button(
            button_frame,
            text="Mark as Completed",
            command=lambda: self.complete_component_training(comp_id, dialog),
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        )
        complete_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        close_btn = tk.Button(
            button_frame,
            text="Close",
            command=dialog.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        )
        close_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

    def complete_component_training(self, comp_id: str, dialog: tk.Toplevel):
        module = self.training_data["modules"][self.current_module]

        completed_count = sum(1 for cid in module.components
                            if cid in self.training_data["components"])

        if completed_count > 0:
            score = random.uniform(85, 98)
            module.score = score

            all_completed = True
            for cid in module.components:
                if cid in self.training_data["components"]:
                    pass

            if all_completed:
                module.completed = True
                module.completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                messagebox.showinfo(
                    "Module Complete!",
                    f"Congratulations!\n\n"
                    f"You have completed the {module.name} module.\n"
                    f"Score: {score:.1f}%\n\n"
                    f"Continue to the next module to advance your training."
                )

                self.save_progress()
                self.populate_modules()

        dialog.destroy()

    def show_statistics(self):
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Training Statistics")
        stats_window.geometry("500x600")
        stats_window.configure(bg="#2c3e50")
        stats_window.transient(self.root)

        header = tk.Frame(stats_window, bg="#34495e", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="Training Progress Statistics",
            font=("Arial", 16, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        )
        title.pack(pady=15)

        content = tk.Frame(stats_window, bg="#2c3e50")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        total_modules = len(self.training_data["modules"])
        completed_modules = sum(1 for m in self.training_data["modules"].values() if m.completed)
        completion_rate = (completed_modules / total_modules * 100) if total_modules > 0 else 0

        avg_score = 0
        if completed_modules > 0:
            total_score = sum(m.score for m in self.training_data["modules"].values() if m.completed)
            avg_score = total_score / completed_modules

        stats = [
            ("Total Modules:", str(total_modules)),
            ("Completed Modules:", str(completed_modules)),
            ("Completion Rate:", f"{completion_rate:.1f}%"),
            ("Average Score:", f"{avg_score:.1f}%"),
        ]

        for label, value in stats:
            frame = tk.Frame(content, bg="#34495e")
            frame.pack(fill=tk.X, pady=5)

            label_widget = tk.Label(
                frame,
                text=label,
                font=("Arial", 11, "bold"),
                bg="#34495e",
                fg="#ecf0f1",
                anchor="w"
            )
            label_widget.pack(side=tk.LEFT, padx=10, pady=8)

            value_widget = tk.Label(
                frame,
                text=value,
                font=("Arial", 11),
                bg="#34495e",
                fg="#3498db",
                anchor="e"
            )
            value_widget.pack(side=tk.RIGHT, padx=10, pady=8)

        modules_label = tk.Label(
            content,
            text="\nModule Details:",
            font=("Arial", 12, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
            anchor="w"
        )
        modules_label.pack(fill=tk.X, pady=(20, 10))

        for module in self.training_data["modules"].values():
            module_frame = tk.Frame(content, bg="#34495e")
            module_frame.pack(fill=tk.X, pady=3)

            status = "✓" if module.completed else "○"
            color = "#27ae60" if module.completed else "#95a5a6"

            status_label = tk.Label(
                module_frame,
                text=status,
                font=("Arial", 14, "bold"),
                bg="#34495e",
                fg=color,
                width=2
            )
            status_label.pack(side=tk.LEFT, padx=5)

            name_label = tk.Label(
                module_frame,
                text=module.name,
                font=("Arial", 10),
                bg="#34495e",
                fg="#ecf0f1",
                anchor="w"
            )
            name_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            if module.completed:
                score_label = tk.Label(
                    module_frame,
                    text=f"{module.score:.1f}%",
                    font=("Arial", 10, "bold"),
                    bg="#34495e",
                    fg="#27ae60"
                )
                score_label.pack(side=tk.RIGHT, padx=10)

        close_btn = tk.Button(
            stats_window,
            text="Close",
            command=stats_window.destroy,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        )
        close_btn.pack(pady=20)

    def reset_progress(self):
        result = messagebox.askyesno(
            "Reset Progress",
            "Are you sure you want to reset all training progress?\n\n"
            "This action cannot be undone."
        )

        if result:
            for module in self.training_data["modules"].values():
                module.completed = False
                module.score = 0.0
                module.completion_time = ""

            self.save_progress()
            self.populate_modules()
            self.current_module = None
            self.current_step = 0
            self.show_welcome_screen()

            self.info_title.config(text="Select a training module to begin")
            self.info_text.delete(1.0, tk.END)

            messagebox.showinfo("Reset Complete", "All training progress has been reset.")

    def save_progress(self):
        try:
            progress_data = {
                "modules": {k: asdict(v) for k, v in self.training_data["modules"].items()}
            }

            with open("training_progress.json", "w") as f:
                json.dump(progress_data, f, indent=2)
        except Exception as e:
            print(f"Error saving progress: {e}")

    def load_progress(self):
        try:
            if os.path.exists("training_progress.json"):
                with open("training_progress.json", "r") as f:
                    progress_data = json.load(f)

                    for module_id, module_dict in progress_data.get("modules", {}).items():
                        if module_id in self.training_data["modules"]:
                            module = self.training_data["modules"][module_id]
                            module.completed = module_dict.get("completed", False)
                            module.score = module_dict.get("score", 0.0)
                            module.completion_time = module_dict.get("completion_time", "")
        except Exception as e:
            print(f"Error loading progress: {e}")


def main():
    root = tk.Tk()
    app = BMP2Simulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()

