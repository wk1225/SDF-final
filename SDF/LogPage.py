import tkinter as tk
from datetime import datetime
from tkinter import PhotoImage, ttk
import pygame
import customtkinter as ctk

# ------------------ Log Page ------------------
class LogPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#EEEEEE")
        self.master = master
        self.exercise_log = []
        self.rickroll = pygame.mixer.Sound("audio/rickroll.MP3")

        # Ensure customtkinter theming is set up (if running the main app)
        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("blue")

        frame = tk.Frame(self,bg="#3838D5")
        frame.pack(side="top",fill="x")

        tk.Label(frame,text="Log",font=("Comic Sans MS",30,"bold"),bg="#3838D5",fg="black").pack(padx=10)

        self.activity_options = [
            "None", "Running", "Walking", "Cycling", "Swimming",
            "Weightlifting", "Yoga", "HIIT",
            "Arm", "Abs", "Leg", "Chest", "Back"
        ]
        self.log_tab(self)
        self.load_saved_logs()

    def play_sound_rickroll(self):
        self.rickroll.play()

    def _toggle_interaction(self, enable):
    # INTERNAL DIALOG METHODS (CUSTOMIZABLE POP-UPS WITH DYNAMIC CENTERING)
        state = "normal" if enable else "disabled"
        
        # Use 'readonly' state for Comboboxes when enabling, as this is their intended state
        combobox_state = 'readonly' if enable else 'disabled'
        
        self.selected_activity.config(state=combobox_state)
        self.hour_combo.config(state=combobox_state)
        self.minute_combo.config(state=combobox_state)
        
        # Intensity state is dynamic, but we can set the base state here
        if enable and self.selected_activity.get() != "None":
             self.selected_intensity.config(state='readonly')
        else:
            self.selected_intensity.config(state='disabled')

        # The delete button needs special handling based on log presence
        if enable and self.exercise_log:
             self.delete_btn.configure(state='normal')
        else:
             self.delete_btn.configure(state='disabled')
             
        # The record button needs special handling based on activity selection
        if enable and self.selected_activity.get() != "None":
            self.record_btn.configure(state='normal')
        else:
            self.record_btn.configure(state='disabled')

    def _create_transient_toplevel(self, title, body_text):
        # Disable the background widgets for the "blur" effect
        self._toggle_interaction(False)

        dialog = tk.Toplevel(self.master)
        dialog.transient(self.master) # Forces the dialog to follow the parent window
        dialog.title(title)
        dialog.config(bg="#EEEEEE")
        dialog.grab_set() # Make the dialog modal (captures all mouse/keyboard events)
        dialog.resizable(False, False) # Prevents resizing

        # Add the body text frame
        body_frame = tk.Frame(dialog, bg="#EEEEEE")
        body_frame.pack(padx=20, pady=20)
        
        # Change font of the prompt message
        tk.Label(
            body_frame, 
            text=body_text, 
            justify=tk.LEFT, 
            bg="#EEEEEE",
            font=("Arial", 11) # <--- FONT CHANGE HERE
        ).pack()
        
        # Add the button frame
        button_frame = tk.Frame(dialog, bg="#EEEEEE")
        button_frame.pack(pady=(0, 10))

        # Dynamic Centering Function (Makes the pop-up follow the main window)
        def _update_position():
            # Must update idletasks to calculate dialog size based on its content
            dialog.update_idletasks()
            
            # Get current dimensions of dialog and parent
            win_width = dialog.winfo_width()
            win_height = dialog.winfo_height()
            parent_x = self.master.winfo_rootx()
            parent_y = self.master.winfo_rooty()
            parent_width = self.master.winfo_width()
            parent_height = self.master.winfo_height()

            # Calculate the centered position
            x = parent_x + (parent_width // 2) - (win_width // 2)
            y = parent_y + (parent_height // 2) - (win_height // 2)
            
            # Set geometry (position only)
            dialog.geometry(f'+{x}+{y}') 

            # Rerun the function every millisecond if the dialog still exists
            if dialog.winfo_exists():
                dialog.after(1, _update_position) 

        # Start the dynamic positioning loop
        _update_position()
        
        # Handle closing: Re-enable all background interactions
        def on_close():
            self._toggle_interaction(True) # Re-enable the background controls
            dialog.destroy()

        # Ensures that closing the window via the 'X' button also runs on_close
        dialog.protocol("WM_DELETE_WINDOW", on_close) 
        
        return dialog, body_frame, button_frame, on_close

    def _prompt_for_record_selection(self, title, prompt_text):
        # Generate the list of available line numbers (1, 2, 3, ... len(self.exercise_log))
        log_count = len(self.exercise_log)
        if log_count == 0:
            self._show_info_error("Error", "No records available to delete.")
            return None
        
        available_lines = [str(i) for i in range(1, log_count + 1)]
        
        dialog, body_frame, button_frame, on_close = self._create_transient_toplevel(title, prompt_text)
        
        result = [None] # Use a list to hold the result reference
        
        def ok_handler():
            selection = combobox.get()
            if selection:
                result[0] = selection
            on_close()
            
        def cancel_handler():
            result[0] = None
            on_close()

        # SELECTION WIDGET
        combobox = ttk.Combobox(
            body_frame, 
            values=available_lines, 
            state="readonly", 
            width=7, 
            font=("Arial", 13)
        )
        combobox.set(available_lines[0]) # Default to the first entry
        combobox.pack(pady=5)
        combobox.focus_set()

        # BUTTONS - CUSTOMIZABLE 
        ctk.CTkButton(
            button_frame, 
            text="OK", 
            font=("Arial", 14, "bold"), 
            hover_color="#6767FF", 
            fg_color="#FFFFFF", 
            text_color="#000000", 
            border_color="#3838D5", 
            border_width=3, 
            width=90, 
            height=35, 
            command=ok_handler
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame, 
            text="Cancel", 
            font=("Arial", 14, "bold"), 
            hover_color="#FF6767", 
            fg_color="#FF0000", 
            text_color="#FFFFFF", 
            width=90, 
            height=35, 
            command=cancel_handler
        ).pack(side="right", padx=5)
        
        dialog.wait_window(dialog)
        return result[0]

    def _ask_yes_no(self, title, prompt_text):
        dialog, _, button_frame, on_close = self._create_transient_toplevel(title, prompt_text)
        
        result = [False] # Use a list to hold the result reference
        
        def yes_handler():
            result[0] = True
            on_close()
            
        def no_handler():
            result[0] = False
            on_close()

        # BUTTONS - CUSTOMIZABLE 
        ctk.CTkButton(
            button_frame, 
            text="Yes", 
            font=("Arial", 14, "bold"), 
            hover_color="#AAFFAA", 
            fg_color="#FFFFFF", 
            text_color="#000000", 
            border_color="#00FF00", 
            border_width=3, 
            width=90, 
            height=35, 
            command=yes_handler
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame, 
            text="No", 
            font=("Arial", 14, "bold"), 
            hover_color="#FF6767", 
            fg_color="#FF0000", 
            text_color="#FFFFFF", 
            width=90, 
            height=35, 
            command=no_handler
        ).pack(side="right", padx=5)

        dialog.wait_window(dialog)
        return result[0]

    def _show_info_error(self, title, message):
        dialog, _, button_frame, on_close = self._create_transient_toplevel(title, message)
        
        def ok_handler():
            on_close()
        
        # BUTTON - CUSTOMIZABLE 
        ctk.CTkButton(
            button_frame, 
            text="OK", 
            font=("Arial", 16, "bold"), 
            hover_color="#6767FF", 
            fg_color="#3838D5", 
            text_color="#FFFFFF", 
            width=95, 
            height=40, 
            command=ok_handler
        ).pack(padx=5)
        
        dialog.wait_window(dialog)

    def log_tab(self, frames):
        # Frame container
        self.report_frame = tk.Frame(frames, bg="#EEEEEE")
        self.report_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # -----Activity Type-----
        activity_frame = tk.Frame(self.report_frame, bg="#EEEEEE")
        activity_frame.pack(fill="x", pady=5)

        tk.Label(
            activity_frame, text="Activity Type:", bg="#EEEEEE", 
            font=("Consolas", 14, "bold"), width=15, anchor="w"
        ).pack(side="left")

        self.activity_options = [
            "None", "Running", "Walking", "Cycling", "Swimming",
            "Weightlifting", "Yoga", "HIIT",
            "Arm", "Abs", "Leg", "Chest", "Back"
        ]

        self.selected_activity = ttk.Combobox(
            activity_frame, values=self.activity_options, state="readonly", 
            width=20, font=("Arial", 13)
        )
        self.selected_activity.set("None")
        self.selected_activity.pack(side="left", padx=5)

        # -----Duration-----
        duration_frame = tk.Frame(self.report_frame, bg="#EEEEEE")
        duration_frame.pack(fill="x", pady=5)

        tk.Label(
            duration_frame, text="Duration     :", bg="#EEEEEE", 
            font=("Consolas", 14, "bold"), width=15, anchor="w"
        ).pack(side="left")

        self.hour_combo = ttk.Combobox(
            duration_frame, values=[f"{i:02d}" for i in range(24)],
            width=3, state="disabled", font=("Arial", 13)
        )
        self.hour_combo.set("00")
        self.hour_combo.pack(side="left", padx=(0,2))
        tk.Label(duration_frame, text="H", bg="#EEEEEE", font=("Arial", 13)).pack(side="left")

        self.minute_combo = ttk.Combobox(
            duration_frame, values=[f"{i:02d}" for i in range(0,60)],
            width=3, state="disabled", font=("Arial", 13)
        )
        self.minute_combo.set("00")
        self.minute_combo.pack(side="left", padx=(5,2))
        tk.Label(duration_frame, text="M", bg="#EEEEEE", font=("Arial", 13)).pack(side="left")

        # -----Intensity-----
        intensity_frame = tk.Frame(self.report_frame, bg="#EEEEEE")
        intensity_frame.pack(fill="x", pady=5)

        tk.Label(
            intensity_frame, text="Intensity    :", bg="#EEEEEE", 
            font=("Consolas", 14, "bold"), width=15, anchor="w"
        ).pack(side="left")

        self.standard_intensity = ["Low", "Medium", "High"]
        self.bodypart_intensity = ["Beginner", "Intermediate", "Advanced"]

        self.selected_intensity = ttk.Combobox(
            intensity_frame, values=[], state="disabled", width=20, font=("Arial", 13)
        )
        self.selected_intensity.pack(side="left", padx=5)

        # -----Record Button-----
        self.record_btn = ctk.CTkButton(
            self.report_frame, text="Record",hover_color="#6767FF", fg_color="#3838D5", text_color="#FFFFFF", 
            command=self.record_exercise, state="disabled", font=("Consolas", 20, "bold")
        )
        self.record_btn.pack(pady=10)

        # -----Log Display Frame and Controls (Master)-----
        log_display_controls_frame = tk.Frame(self.report_frame, bg="#EEEEEE")
        log_display_controls_frame.pack(fill="both", expand=True, pady=10)

        # FIX: New frame to hold Text and Scrollbar for proper vertical stacking with the button
        text_scroll_frame = tk.Frame(log_display_controls_frame, bg="#EEEEEE")
        text_scroll_frame.pack(fill="both", expand=True, pady=(0, 5)) 

        # Log Display - CORRECTED: Using 'bg' and 'fg', removed 'selectmode'
        self.report_display = tk.Text(
            text_scroll_frame, width=40, height=10, font=("Arial", 12), 
            bg="#FFFFFF", fg="#000000",
            selectbackground="#6767FF", selectforeground="white"
        )
        self.report_display.pack(side="left", fill="both", expand=True, padx=5)

        scrollbar = tk.Scrollbar(text_scroll_frame, command=self.report_display.yview)
        scrollbar.pack(side="right", fill="y")
        self.report_display.config(yscrollcommand=scrollbar.set)
        
        # New: Delete Button Frame (Packs vertically *after* the text area frame)
        delete_button_frame = tk.Frame(log_display_controls_frame, bg="#EEEEEE")
        delete_button_frame.pack(fill="x", pady=(5, 0))

        self.delete_btn = ctk.CTkButton(
            delete_button_frame, text="Delete?", hover_color="#FFAAAA", fg_color="#EEEEEE", text_color="#FF0000", 
            command=self.confirm_delete_record, state="disabled", font=("Consolas", 14, "bold", "underline")
        )
        self.delete_btn.pack(side="right", padx=5)

        # Storage
        self.exercise_log = []

        def update_intensity_options():
        #-----Functions for enabling/disabling inputs-----
            act = self.selected_activity.get()
            if act in ["Arm", "Abs", "Leg", "Chest", "Back"]:
                self.selected_intensity.config(values=self.bodypart_intensity, state="readonly")
                self.selected_intensity.set(self.bodypart_intensity[0])
            elif act == "None":
                self.selected_intensity.set("")
                self.selected_intensity.config(values=[], state="disabled")
            else:
                self.selected_intensity.config(values=self.standard_intensity, state="readonly")
                self.selected_intensity.set(self.standard_intensity[0])

        def update_duration_state():
            if self.selected_activity.get() == "None":
                self.hour_combo.config(state="disabled")
                self.minute_combo.config(state="disabled")
            else:
                self.hour_combo.config(state="readonly")
                self.minute_combo.config(state="readonly")

        def update_record_button():
            if self.selected_activity.get() == "None":
                self.record_btn.configure(state="disabled")
            else:
                self.record_btn.configure(state="normal")

        #Bind activity change
        self.selected_activity.bind(
            "<<ComboboxSelected>>", 
            lambda e: [
                update_intensity_options(),
                update_record_button(),
                update_duration_state()
            ]
        )

    def record_exercise(self):
            self.play_sound_rickroll()
            # Get selected activity and intensity
            activity = self.selected_activity.get()
            intensity = self.selected_intensity.get().lower()

            # Get hours and minutes
            hours = int(self.hour_combo.get())
            minutes = int(self.minute_combo.get())

            # Get time now
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save record in memory
            record = {
                "activity": activity,
                "hours": hours,
                "minutes": minutes,
                "intensity": intensity.title(),
                "date": timestamp  
            }
            self.exercise_log.append(record)

            #---- Write to text file WITH USERNAME + DATE/TIME ----
            current_user = self.master.current_user
            
            try:
                with open("workout_records.txt", "a", encoding="utf-8") as f:
                    # Format: USERNAME \t DATETIME \t ACTIVITY \t DURATION \t INTENSITY
                    f.write(
                        f"{current_user}\t{timestamp}\t{activity}\t{hours:02d}H {minutes:02d}M\t{intensity.title()}\n"
                    )
            except Exception as e:
                print("Error writing workout log:", e)

            # Update report on screen
            self.update_report_display()

    def confirm_delete_record(self):
        
        # Use the new custom Combobox selection dialog
        line_num_str = self._prompt_for_record_selection(
            "Delete Record", 
            "Select the row of the record you want to delete:" 
        )

        if not line_num_str:
            return # User cancelled or no records exist

        try:
            # Convert line number (1-based, as displayed) to list index (0-based)
            log_index_to_delete = int(line_num_str) - 1 
        except ValueError:
            # This should not happen with a Combobox, but is kept for safety
            self._show_info_error("Error", "Invalid selection. Please try again.") 
            return

        # Check if the calculated index is valid for the current log list
        if 0 <= log_index_to_delete < len(self.exercise_log):
            record = self.exercise_log[log_index_to_delete]
            
            # Use the custom confirmation dialog
            confirm = self._ask_yes_no(
                "Confirm Deletion", 
                f"Confirm deletion of record #{line_num_str}?\n\n"
                f"{line_num_str}. {record['activity']}   ({record['hours']:02d}H {record['minutes']:02d}M)   {record['intensity']}" # <--- Custom Confirmation Message
            )

            if confirm:
                # Proceed with deletion
                self.delete_record(log_index_to_delete)

    def delete_record(self, index_to_delete):
        if 0 <= index_to_delete < len(self.exercise_log):
            # Delete from memory
            del self.exercise_log[index_to_delete]
            
            # Rewrite the file with remaining logs
            self.save_logs_to_file()
            
            # Update display
            self.update_report_display()
            
            # Use the custom info dialog (Success)
            self._show_info_error("Success", "Record deleted forever.")
            
            # The button will be disabled if exercise_log is empty, which is handled by update_report_display.

    def update_report_display(self):
        self.report_display.config(state="normal")
        self.report_display.delete("1.0", "end")

        #Change font of all log records (Consolas, size -2)
        self.report_display.configure(font=("Consolas", 11))

        #Title
        title = "Workout Records"
        self.report_display.insert("end", f"{title:^35}", "title")
        self.report_display.insert("end", "_" * 40 + "\n")

        #Icons
        activity_icons = {
            "running": "🏃‍♂",
            "walking": "🚶‍♂",
            "cycling": "🚴‍♂",
            "swimming": "🏊‍♂",
            "weightlifting": "🏋‍♂",
            "yoga": "🧘‍♂",
            "hiit": "💪",
            "arm": "💪",
            "abs": "💥",
            "leg": "🦵",
            "chest": "🏋",
            "back": "🛡"
        }

        #Format logs in aligned columns
        for i, item in enumerate(self.exercise_log, start=1):
            icon = activity_icons.get(item['activity'].lower(), "⚡")
            line = (f"{i:>3}. " f"{item['activity']:<13}  " f"{item['hours']:02d}H {item['minutes']:02d}M  " f"{item['intensity']:<12}\n")
            self.report_display.insert("end", line)
        
        # Enable/Disable Delete Button based on log presence
        if self.exercise_log:
            self.delete_btn.configure(state="normal")
        else:
            self.delete_btn.configure(state="disabled")

        #Styling
        self.report_display.tag_config(
            "title",
            font=("Consolas", 15, "bold")
        )

        # Re-disable the widget to prevent user input
        self.report_display.config(state="disabled")

    def save_logs_to_file(self):
        current_user = self.master.current_user
        
        try:
            # Read all lines first to keep other users' logs
            all_lines = []
            try:
                with open("workout_records.txt", "r", encoding="utf-8") as f:
                    all_lines = f.readlines()
            except FileNotFoundError:
                pass

            # Filter out current user's old logs
            user_specific_lines = [
                line for line in all_lines 
                if not line.strip().startswith(current_user + "\t")
            ]

            # Append current user's updated logs
            for record in self.exercise_log:
                # Format: USERNAME \t DATETIME \t ACTIVITY \t DURATION \t INTENSITY
                log_line = (
                    f"{current_user}\t{record['date']}\t{record['activity']}\t"
                    f"{record['hours']:02d}H {record['minutes']:02d}M\t{record['intensity']}\n"
                )
                user_specific_lines.append(log_line)

            # Write all logs back to the file
            with open("workout_records.txt", "w", encoding="utf-8") as f:
                f.writelines(user_specific_lines)

        except Exception as e:
            print("Error saving workout log:", e)

    def load_saved_logs(self):
            self.exercise_log = [] # Clear existing logs in memory first
            current_user = self.master.current_user

            try:
                with open("workout_records.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue

                        # File format: Username \t Date \t Activity \t Duration \t Intensity
                        parts = [x.strip() for x in line.split("\t")]

                        # Only load if the Username (part[0]) matches the current user
                        if len(parts) >= 5 and parts[0] == current_user:
                            # parts[1] is datetime (Now we capture it for Report filtering)
                            date_str = parts[1] 
                            activity = parts[2]
                            duration = parts[3]
                            intensity = parts[4]

                            try:
                                # Parse "01H 30M"
                                hours = int(duration.split("H")[0])
                                minutes = int(duration.split("H")[1].replace("M", "").strip())
                                
                                self.exercise_log.append({
                                    "activity": activity, 
                                    "hours": hours, 
                                    "minutes": minutes, 
                                    "intensity": intensity,
                                    "date": date_str  # Store the date in memory
                                })
                            except:
                                pass # Skip badly formatted lines

                # Update the on-screen display after loading
                self.update_report_display()

            except FileNotFoundError:
                pass
