import tkinter as tk
import random
# Removed: from tkinter import messagebox # We no longer need this import if messagebox.showinfo is removed

class VirtualPet:
    def __init__(self, master):
        self.master = master
        master.title("My Virtual Pet")
        master.geometry("400x380")
        master.resizable(False, False)

        self.pet_name = "Bunny"
        self.hunger = 50
        self.health = 100
        self.game_over = False

        self.create_game_widgets()
        self.update_pet_status()

    def create_game_widgets(self):
        self.pet_label = tk.Label(self.master, text=f"Hello, I'm {self.pet_name}!", font=("Arial", 16))
        self.pet_label.pack(pady=10)

        self.hunger_label = tk.Label(self.master, text=f"Hunger: {self.hunger}%")
        self.hunger_label.pack()

        self.health_label = tk.Label(self.master, text=f"Health: {self.health}%", fg="green")
        self.health_label.pack()

        self.feed_button = tk.Button(self.master, text="Feed Pet", command=self.feed_pet)
        self.feed_button.pack(pady=5)

        self.play_button = tk.Button(self.master, text="Play with Pet", command=self.play_with_pet)
        self.play_button.pack(pady=5)

        self.status_message = tk.Label(self.master, text="Your pet is doing well!", font=("Arial", 10))
        self.status_message.pack(pady=10)

    def feed_pet(self):
        if self.game_over: return
        food_amount = random.randint(15, 25)
        self.hunger = min(100, self.hunger + food_amount)
        self.status_message.config(text=f"{self.pet_name} enjoyed the meal!")
        self.update_pet_status()

    def play_with_pet(self):
        if self.game_over: return
        play_effect_hunger = random.randint(10, 20)
        self.hunger = max(0, self.hunger - play_effect_hunger)
        self.status_message.config(text=f"{self.pet_name} had a great time playing!")
        self.update_pet_status()

    def update_pet_status(self):
        self.hunger_label.config(text=f"Hunger: {self.hunger}%")
        self.health_label.config(text=f"Health: {self.health}%")

        # Update health label color
        if self.health > 75:
            self.health_label.config(fg="green")
        elif self.health > 40:
            self.health_label.config(fg="orange")
        else:
            self.health_label.config(fg="red")

        # Game over state (if already over, just ensure buttons are disabled)
        if self.game_over:
            self.status_message.config(text=f"{self.pet_name} has passed away.", fg="red")
            self.disable_buttons()
            return

        # Check for game over condition (when health first drops to 0 or below)
        if self.health <= 0 and not self.game_over:
            self.game_over = True
            self.status_message.config(text=f"Game Over! {self.pet_name} has passed away.", fg="red", font=("Arial", 12, "bold"))
            # THIS LINE IS REMOVED: messagebox.showinfo("Game Over", f"Oh no! {self.pet_name} ran out of health. Game Over!")
            self.disable_buttons()
            return # Stop further updates and decay if game is over

        # General status messages (only if game is NOT over)
        if not self.game_over:
            if self.hunger < 20:
                self.status_message.config(text=f"{self.pet_name} is very hungry!", fg="red")
            elif self.hunger > 80 and self.health > 80:
                self.status_message.config(text=f"{self.pet_name} is super happy and healthy!", fg="blue")
            else:
                self.status_message.config(text=f"Your pet is doing well!", fg="black")

        # Schedule next decay (only if game is NOT over)
        if not self.game_over:
            self.master.after(5000, self.decay_stats)

    def decay_stats(self):
        if self.game_over: return # Important: stop decay if game is already over

        self.hunger = max(0, self.hunger - random.randint(2, 5))

        # Health decay based on low hunger
        if self.hunger < 30:
            self.health = max(0, self.health - random.randint(3, 7))
        # Health increase if hunger is high
        if self.hunger > 70:
            self.health = min(100, self.health + random.randint(1, 3))

        self.update_pet_status()

    def disable_buttons(self):
        self.feed_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.DISABLED)

# Main part of the script
if __name__ == "__main__":
    root = tk.Tk()
    pet_game = VirtualPet(root)
    root.mainloop()