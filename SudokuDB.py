# imports
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
import sqlite3


console = Console()
data_dir = Path.home() / 'Dropbox' / 'Python' / 'Sudoku' / 'data' / 'output'


def main(args):
    """
    Handle database functions for Sudoku puzzles
    -- unsolved puzzles from physical magazines
    -- puzzle status from print and solve issues
    CLI arguments:
    function -- insert, query, update, delete
    book -- book identifier
    puzzle -- puzzle identifier
    status -- solved, unsolved for print and solve issues
    """

    # verify the arguments are populated
    if args.book is None:
        console.print("[bold red]Error: --book argument is required[/ bold red]")
        return
    if args.function != 'query' and args.puzzle is None:
        console.print("[bold red]Error: --puzzle argument is required for insert, update, and delete functions[/bold red]")
        return
    if args.function != 'query' and args.status is None:
        console.print("[bold red]Error: --status argument must be provided for Double Sudoku puzzles[/bold red]")
        return
    
    # create the connection
    # ensure output directory exists
    data_dir.parent.mkdir(parents=True, exist_ok=True)

    db_path = data_dir / 'SudokuPuzzles.db'
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # step through the database functions
            if args.function == 'insert':
                if 'Double' in args.book:
                    console.print(f'[dim]Inserting puzzle {args.puzzle} from book {args.book} with status {args.status}[/dim]', highlight=False)
                    cursor.execute('INSERT INTO DoubleSudoku (Book, PuzzleID, Status) VALUES (?, ?, ?)',
                        (args.book, args.puzzle, args.status)
                    )
                    conn.commit()
                    console.print('[bold green]Insert successful[/bold green]')
                else:
                    console.print(f'[dim]Inserting puzzle {args.puzzle} from book {args.book}[/dim]', highlight=False)
                    cursor.execute('INSERT INTO UnsolvedPuzzles (Book, PuzzleID) VALUES (?, ?)',
                        (args.book, args.puzzle)
                    )
                    conn.commit()
                    console.print('[bold green]Insert successful[/bold green]')
            
            elif args.function == 'query':
                console.print(f'[dim]Querying puzzles from book {args.book}[/dim]')
                if 'Double' in args.book:
                    cursor.execute('SELECT Book, PuzzleID, Status FROM DoubleSudoku ORDER BY PuzzleID DESC LIMIT 5')
                else:
                    cursor.execute('SELECT Book, PuzzleID FROM UnsolvedPuzzles ORDER BY PuzzleID ASC LIMIT 5')
                rows = cursor.fetchall()
                if rows:
                    table = Table(show_header=True, header_style="bold magenta")
                    # use the row keys (sqlite3.Row) as column names
                    cols = rows[0].keys()
                    for col in cols:
                        table.add_column(col)
                    for row in rows:
                        table.add_row(*(str(row[c]) for c in cols))
                    console.print(table)
                else:
                    console.print("[bold yellow]No rows returned[/bold yellow]")
 
            elif args.function == 'update':
                console.print(f'[dim]Updating puzzle {args.puzzle} from book {args.book} to status {args.status}[/dim]', highlight=False)
                cursor.execute(
                    'UPDATE DoubleSudoku SET Status = ? WHERE Book = ? AND PuzzleID = ?',
                    (args.status, args.book, args.puzzle)
                )
                conn.commit()
                console.print('[bold green]Update successful[/bold green]')
 
            elif args.function == 'delete':
                console.print(f'[dim]Deleting puzzle {args.puzzle} from book {args.book}[/dim]', highlight=False)
                if 'Double' in args.book:
                    cursor.execute(
                        'DELETE FROM DoubleSudoku WHERE Book = ? AND PuzzleID = ?',
                        (args.book, args.puzzle)
                    )
                else:
                    cursor.execute(
                        'DELETE FROM UnsolvedPuzzles WHERE Book = ? AND PuzzleID = ?',
                        (args.book, args.puzzle)
                    )
                conn.commit()
                console.print('[bold green]Delete successful[/bold green]')
    except sqlite3.Error as e:
        console.print(f'[bold red]Database error: {e}[/bold red]')
    except Exception as e:
        console.print(f'[bold red]Unexpected error: {e}[/bold red]')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=main.__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--book')
    parser.add_argument('--puzzle')
    parser.add_argument(
        '--status',
        choices = ['solved', 'unsolved']
    )
    parser.add_argument(
        '--function',
        choices = ['insert', 'query', 'update', 'delete']
    )
    args = parser.parse_args()
    main(args)
