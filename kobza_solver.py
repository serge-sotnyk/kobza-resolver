from pathlib import Path
import re
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Static
from textual.screen import Screen
from textual.containers import Vertical, ScrollableContainer

class KobzaSolverApp(App):
    """A Textual app for solving the Kobza game."""

    CSS = """
    Screen {
        align: center middle;
        background: $surface;
    }
    
    #solver-container {
        width: 80%;
        height: 80%;
        border: tall $background;
        padding: 2 4;
    }
    
    .input-label {
        color: $text-muted;
        margin-bottom: 1;
    }
    
    #results-container {
        height: 50%;
        border: tall $background-lighten-2;
        padding: 1;
        margin-top: 2;
        overflow-y: scroll;  /* Explicitly set scrollable */
    }
    
    Button {
        margin: 2 0;
    }
    """

    def __init__(self):
        super().__init__()
        # Load dictionary of words
        self.five_letters = Path("kobza_filtered_dict_words.txt").read_text(encoding="utf-8").splitlines()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Vertical(id="solver-container"):
            yield Static("Impossible Letters", classes="input-label")
            yield Input(placeholder="Enter letters to exclude", id="impossible-letters")
            
            yield Static("Possible Letters", classes="input-label")
            yield Input(placeholder="Enter letters that must be present", id="possible-letters")
            
            yield Static("Pattern (use . for unknown letters)", classes="input-label")
            yield Input(placeholder="Enter pattern (e.g., ...но)", id="pattern", value=".....")
            
            yield Button("Find Words", variant="primary", id="search-button")
            
            yield ScrollableContainer(
                Static(id="results-container")
            )
        
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press to search for words."""
        if event.button.id == "search-button":
            self.search_words()

    def search_words(self) -> None:
        """Search for words matching the criteria."""
        # Get input values
        impossible_letters = self.query_one("#impossible-letters", Input).value.lower()
        possible_letters = self.query_one("#possible-letters", Input).value.lower()
        pattern = self.query_one("#pattern", Input).value.lower()
        
        # Results container
        results_container = self.query_one("#results-container", Static)
        
        # Validate inputs
        if not all([impossible_letters, possible_letters, pattern]):
            results_container.update("Please fill in all fields.")
            return
        
        # Check that impossible letters are not in possible letters or pattern
        for letter in impossible_letters:
            if letter in possible_letters or letter in pattern.replace('.', ''):
                results_container.update(f"Error: Impossible letter '{letter}' found in possible letters or pattern.")
                return
        
        # Search logic
        found = []
        for word in self.five_letters:
            # Skip words with impossible letters
            if any(letter in word for letter in impossible_letters):
                continue
            
            # Check if all possible letters are present
            if not all(letter in word for letter in possible_letters):
                continue
            
            # Check pattern match
            if re.match(pattern, word):
                found.append(word)
        
        # Display results
        if found:
            results_text = f"Found {len(found)} words:\n\n" + "\n".join(found)
        else:
            results_text = "No words found matching the criteria."
        
        results_container.update(results_text)

def main():
    """Run the Kobza Solver app."""
    app = KobzaSolverApp()
    app.run()

if __name__ == "__main__":
    main()
    