# Tutori

A minimal, privacy-focused spaced repetition CLI tool powered by the [FSRS](https://github.com/open-spaced-repetition/py-fsrs) algorithm. Contains no telemetry, no data will ever be gathered by Tutori.

## Installation

Requires Python 3.10+ and the following dependencies:

```bash
pip install click fsrs
```

Clone the repository and add the script to your PATH, or symlink it to a directory on your PATH.

## Usage

### View due items

```bash
tutori
```

Displays all items due today or overdue, sorted by due date.

### Commands

| Command                                          | Shorthand         | Description                                       |
| ------------------------------------------------ | ----------------- | ------------------------------------------------- |
| `tutori`                                         | —                 | View due and overdue items                        |
| `tutori all`                                     | `tutori la`       | View all items with due dates                     |
| `tutori upcoming [days]`                         | `tutori u [days]` | View items due within N days (default 7)          |
| `tutori add <nametag> <description> [answer]`    | `tutori a`        | Add an entry, answer is optional                  |
| `tutori rate <nametag> <1-4>`                    | `tutori r`        | Rate an entry                                     |
| `tutori show <nametag>`                          | `tutori s`        | Display the answer for an entry                   |
| `tutori edit <old> <new> [description] [answer]` | `tutori e`        | Edit an entry                                     |
| `tutori remove <nametag>`                        | `tutori rm`       | Remove an entry                                   |
| `tutori new`                                     | —                 | Initialize or clear card data                     |
| `tutori reset`                                   | —                 | Reset scheduler to default parameters             |
| `tutori optimize`                                | —                 | Optimize scheduler parameters from review history |
| `tutori scheduler`                               | —                 | Display current scheduler parameters              |
| `tutori clean`                                   | —                 | Remove entries scheduled more than one year out   |
| `tutori save <location>`                         | —                 | Backup data to a specified location               |

### Ratings

| Rating | Meaning                                   |
| ------ | ----------------------------------------- |
| 1      | Again — forgot completely                 |
| 2      | Hard — remembered with serious difficulty |
| 3      | Good — remembered after hesitation        |
| 4      | Easy — remembered easily                  |

### Example workflow

```bash
# Add a card
tutori add "python-list" "How do you create an empty list?" "my_list = []"

# View what's due today
tutori

# Review a card — answer is shown automatically if one exists
tutori r python-list 3

# See what's coming up in the next two weeks
tutori u 14
```

## Data format

All data is stored in `~/.config/tutori/tutori.json`. The file contains card data, review logs, and scheduler parameters. It can be backed up with `tutori save <location>` and is human readable JSON.

## FSRS Optimizer

Tutori stores a full review log for every card. Once you have accumulated sufficient review history, running `tutori optimize` will use the FSRS optimizer to compute scheduler parameters tuned to your personal memory patterns.

Note: the optimizer requires PyTorch. Install the CPU-only version:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## License

GPL-3.0
